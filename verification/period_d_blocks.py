"""
Period-d certificates via Fourier blocks -- the fast and principled version.

For weights of period d | n, put m = n/d and index outer vertices as
i = r + d q with r in [0,d), q in [0,m).  Fourier over q with zeta = e^{2 pi i l/m}
splits A into m Hermitian blocks of size 2d,

    M_l = [ U_l   C  ]       U_l : d x d, outer cycle within a cell, the
          [ C     V_l]             wrap r = d-1 -> 0 carrying zeta
                                 V_l : d x d, r -> (r+k) mod d carrying
                                       zeta^{floor((r+k)/d)}
                                 C   : diag(c_0..c_{d-1})

and  nullity(A) = sum over l of nullity(M_l).

This costs m eigendecompositions of size 2d instead of one of size 2n, which
is what makes larger n affordable: for n = 120, d = 2 it is 60 blocks of size
4 rather than a single 240 x 240 problem.

Period 1 is the special case d = 1, where each block is the 2x2
[[a + s_l, c], [c, d + e t_l]] of the symbol analysis.
"""
import sys
import numpy as np
from scipy.optimize import minimize

KINDS = ("outer", "spoke", "inner", "diagO", "diagI")


def unpack(w, d):
    """w is 5d long, ordered by kind then residue."""
    b, c, e, aO, aI = (w[j * d:(j + 1) * d] for j in range(5))
    return b, c, e, aO, aI


def blocks(w, n, k, d):
    m = n // d
    b, c, e, aO, aI = unpack(w, d)
    out = []
    for l in range(m):
        z = np.exp(2j * np.pi * l / m)
        U = np.zeros((d, d), dtype=complex)
        V = np.zeros((d, d), dtype=complex)
        for r in range(d):
            U[r, r] = aO[r]
            V[r, r] = aI[r]
            # outer edge r -> r+1 (wrapping into the next cell carries zeta)
            rp, delta = (r + 1) % d, (r + 1) // d
            U[r, rp] += b[r] * z ** delta
            U[rp, r] += b[r] * np.conj(z) ** delta
            # inner edge r -> r+k
            rq, dk = (r + k) % d, (r + k) // d
            V[r, rq] += e[r] * z ** dk
            V[rq, r] += e[r] * np.conj(z) ** dk
        C = np.diag(c.astype(complex))
        out.append(np.block([[U, C], [C, V]]))
    return out


def block_data(w, n, k, d):
    """Eigen-decomposition of every block, plus the (r,r',delta) layout of
    each parameter so gradients can be assembled analytically."""
    out = []
    for l, M in enumerate(blocks(w, n, k, d)):
        lam, V = np.linalg.eigh(M)
        out.append((l, lam, V))
    return out


def slot_arrays(n, k, d):
    """Flat (row, col, delta, is_diag) arrays -- one entry per parameter, in
    the same order as w.  Lets the gradient be one vectorised expression per
    selected eigenvalue instead of a Python loop over parameters."""
    rows, cols, dels, diag = [], [], [], []
    for r in range(d):                                   # outer edges
        rows.append(r); cols.append((r + 1) % d)
        dels.append((r + 1) // d); diag.append(False)
    for r in range(d):                                   # spokes
        rows.append(r); cols.append(d + r); dels.append(0); diag.append(False)
    for r in range(d):                                   # inner edges
        rows.append(d + r); cols.append(d + (r + k) % d)
        dels.append((r + k) // d); diag.append(False)
    for r in range(d):                                   # outer diagonals
        rows.append(r); cols.append(r); dels.append(0); diag.append(True)
    for r in range(d):                                   # inner diagonals
        rows.append(d + r); cols.append(d + r); dels.append(0); diag.append(True)
    return (np.array(rows), np.array(cols), np.array(dels),
            np.array(diag, dtype=bool))


def param_slots(n, k, d):
    """For each of the 5d parameters, the list of (row, col, phase_exponent)
    it contributes to inside a block.  Phase exponent is the power of zeta."""
    slots = []
    for r in range(d):                                   # outer edges b_r
        rp, delta = (r + 1) % d, (r + 1) // d
        slots.append([(r, rp, delta)])
    for r in range(d):                                   # spokes c_r
        slots.append([(r, d + r, 0)])
    for r in range(d):                                   # inner edges e_r
        rq, dk = (r + k) % d, (r + k) // d
        slots.append([(d + r, d + rq, dk)])
    for r in range(d):                                   # outer diagonals
        slots.append([(r, r, None)])
    for r in range(d):                                   # inner diagonals
        slots.append([(d + r, d + r, None)])
    return slots


def nullity_profile(w, n, k, d):
    vals = np.sort(np.abs(np.concatenate(
        [np.linalg.eigvalsh(M) for M in blocks(w, n, k, d)])))
    return vals, max(np.abs(w).max(), 1e-12)


def objective(w, n, k, d, r, tau, mu, slots=None, m=None):
    """f = sum of squares of the r eigenvalues closest to zero, plus a barrier
    keeping required-nonzero weights away from 0 and a scale penalty.

    Gradients are analytic: for a Hermitian block M with unit eigenvector v and
    eigenvalue lam, d(lam)/dw_j = v* (dM/dw_j) v, and dM/dw_j is one conjugate
    pair of entries carrying a known power of zeta.  Finite differences fail
    here because the objective is only piecewise smooth where eigenvalues
    cross -- which is exactly where the solutions live."""
    if slots is None:
        slots = slot_arrays(n, k, d)
    if m is None:
        m = n // d
    rr, cc, dd, isdiag = slots
    P = len(w)
    lams, vecs, phases = [], [], []
    for l, M in enumerate(blocks(w, n, k, d)):
        lam, V = np.linalg.eigh(M)
        lams.append(lam)
        vecs.append(V)
        phases.append(np.exp(2j * np.pi * l / m))
    allv = np.concatenate(lams)
    order = np.argsort(np.abs(allv))[:r]
    f = float(np.sum(allv[order] ** 2))
    g = np.zeros(P)
    nb = 2 * d
    for t in order:
        l, col = divmod(int(t), nb)
        v = vecs[l][:, col]
        ph = phases[l] ** dd
        contrib = 2.0 * np.real(np.conj(v[rr]) * v[cc] * ph)
        contrib = np.where(isdiag, np.real(np.conj(v[rr]) * v[rr]), contrib)
        g += 2.0 * allv[t] * contrib
    nz = w[:3 * d]
    viol = np.maximum(0.0, tau - np.abs(nz))
    f += mu * float(np.sum(viol ** 2))
    g[:3 * d] += -2.0 * mu * viol * np.sign(nz)
    pen = w @ w / P - 1.0
    f += pen ** 2
    g += 4.0 * pen * w / P
    return f, g


def signed_smallest(w, n, k, d, r):
    """The r eigenvalues closest to zero, with sign, as a residual vector."""
    vals = np.concatenate([np.linalg.eigvalsh(M) for M in blocks(w, n, k, d)])
    return vals[np.argsort(np.abs(vals))[:r]]


def polish(w, n, k, d, r, tau=0.06):
    """Quadratic clean-up.  L-BFGS-B on the squared-eigenvalue objective
    stalls near 1e-9 because it is only piecewise smooth at eigenvalue
    crossings; driving the r smallest eigenvalues to zero as a least-squares
    residual converges to machine precision once we are close."""
    from scipy.optimize import least_squares

    def res(v):
        scale = max(np.abs(v).max(), 1e-12)
        out = signed_smallest(v, n, k, d, r) / scale
        nz = v[:3 * d]
        bar = np.maximum(0.0, tau - np.abs(nz) / scale)
        return np.concatenate([out, bar, [v @ v / len(v) - 1.0]])

    sol = least_squares(res, w, method="trf",
                        xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=200)
    return sol.x


def search(n, k, d, r, tries=200, seed=0, tau=0.06, mu=40.0, maxiter=800,
           n_polish=8):
    """Two stages: many cheap L-BFGS starts with analytic gradients, then a
    least-squares polish of only the most promising few.  Polishing every start
    is what made an earlier version unusably slow -- the polish costs orders of
    magnitude more per call than a start does."""
    P = 5 * d
    slots = slot_arrays(n, k, d)
    rng = np.random.default_rng(seed)
    cands = []
    for t in range(tries):
        w0 = rng.standard_normal(P)
        w0 *= np.sqrt(P) / np.linalg.norm(w0)
        res = minimize(objective, w0, jac=True, method="L-BFGS-B",
                       args=(n, k, d, r, tau, mu, slots, n // d),
                       options=dict(maxiter=maxiter, ftol=1e-18, gtol=1e-14))
        vals, scale = nullity_profile(res.x, n, k, d)
        cands.append((vals[r - 1] / scale, res.x.copy()))
    cands.sort(key=lambda z: z[0])
    best = None
    for (_, w) in cands[:n_polish]:
        wp = polish(w, n, k, d, r, tau=tau)
        vals, scale = nullity_profile(wp, n, k, d)
        small = vals[r - 1] / scale
        gap = vals[r] / scale if r < len(vals) else np.inf
        minnz = np.abs(wp[:3 * d]).min() / scale
        if best is None or small < best[1]:
            best = (wp.copy(), small, gap, minnz)
    return best


if __name__ == "__main__":
    k = int(sys.argv[1])
    ds = [int(v) for v in sys.argv[2].split(",")]
    ns = [int(v) for v in sys.argv[3].split(",")]
    tries = int(sys.argv[4]) if len(sys.argv) > 4 else 200
    r = 2 * k + 2
    print(f"period-d block search, k={k}, target nullity r={r} (= 2k+2)")
    print(f"{'n':>5} {'d':>3} {'m=n/d':>6} {'params':>7} {'ratios':>7} "
          f"{'lam_r/scale':>13} {'gap':>10} {'min|wt|':>9}  verdict", flush=True)
    for n in ns:
        for d in ds:
            if n % d or 2 * k >= n:
                continue
            m = n // d
            # Gamma_m has floor(m/2)+1 distinct values, of which the
            # interior ones (|s| < 2) number ceil(m/2) - 1.  Attaining 2k+2
            # needs k+1 DISTINCT INTERIOR roots, so m >= 2k+4.
            if (m + 1) // 2 - 1 < k + 1:
                print(f"{n:>5} {d:>3} {m:>6} {5*d:>7} {5*d-1:>7} "
                      f"{'-':>13} {'-':>10} {'-':>9}  "
                      f"grid too small (need m >= {2*k+4})")
                continue
            w, small, gap, minnz = search(n, k, d, r, tries=tries)
            ok = small < 1e-9 and gap > 1e-3 and minnz > 1e-2
            print(f"{n:>5} {d:>3} {m:>6} {5*d:>7} {5*d-1:>7} {small:>13.2e} "
                  f"{gap:>10.2e} {minnz:>9.4f}  "
                  f"{'CERTIFICATE' if ok else 'none'}", flush=True)
