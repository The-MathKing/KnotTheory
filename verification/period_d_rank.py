"""
How many of the k+1 coefficients can a period-d symbol actually control?

For period-d weights the singularity condition of the Fourier block M_l is
det M_l = 0.  That determinant is a reciprocal Laurent polynomial in
zeta = e^{2 pi i l/m} spanning zeta^{-(k+1)} .. zeta^{k+1}, so it is a
polynomial G of degree k+1 in sigma = zeta + 1/zeta.  The nullity is
2 * (number of roots of G lying in Gamma_m, interior), so attaining 2k+2
requires prescribing all k+1 roots -- that is, hitting a specific G.

The question is therefore: what is the DIMENSION of the set of G reachable by
the 5d weights?  Period 1 famously reaches only a 3-dimensional slice of the
(k+1)-dimensional space of monic degree-(k+1) polynomials, which is why it
fails for k >= 6.  This script computes the rank of the Jacobian of

    (5d weights)  ->  (k+1 coefficients of the monic G)

at random points.  Rank k+1 means the map is a submersion, so every nearby G
is reachable and prescribing all k+1 roots is possible; rank < k+1 means a
genuine obstruction that more parameters of this kind cannot remove.
"""
import sys
import numpy as np

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from period_d_blocks import blocks, unpack


def G_coeffs(w, n, k, d, npts=None):
    """Monic coefficients of G(sigma), by evaluating det M(zeta) on a set of
    sigma values and interpolating."""
    deg = k + 1
    if npts is None:
        npts = deg + 1
    # sample sigma = 2cos(theta) at generic angles (not the grid)
    thetas = np.linspace(0.13, np.pi - 0.11, npts)
    sig = 2 * np.cos(thetas)
    vals = []
    for th in thetas:
        z = np.exp(1j * th)
        M = _block_at(w, n, k, d, z)
        vals.append(np.real(np.linalg.det(M)))
    # fit degree-(k+1) polynomial in sigma
    V = np.vander(sig, deg + 1)
    coef, *_ = np.linalg.lstsq(V, np.array(vals), rcond=None)
    if abs(coef[0]) < 1e-14:
        return None
    return coef / coef[0]                    # monic; drop the leading 1


def _block_at(w, n, k, d, z):
    b, c, e, aO, aI = unpack(w, d)
    U = np.zeros((d, d), dtype=complex)
    V = np.zeros((d, d), dtype=complex)
    for r in range(d):
        U[r, r] = aO[r]; V[r, r] = aI[r]
        rp, delta = (r + 1) % d, (r + 1) // d
        U[r, rp] += b[r] * z ** delta
        U[rp, r] += b[r] * np.conj(z) ** delta
        rq, dk = (r + k) % d, (r + k) // d
        V[r, rq] += e[r] * z ** dk
        V[rq, r] += e[r] * np.conj(z) ** dk
    C = np.diag(c.astype(complex))
    return np.block([[U, C], [C, V]])


def jac_rank(n, k, d, trials=6, seed=0, tol=1e-7):
    rng = np.random.default_rng(seed)
    P = 5 * d
    ranks = []
    for _ in range(trials):
        w = rng.standard_normal(P)
        w[:3 * d] += 1.2 * np.sign(w[:3 * d])          # keep edges away from 0
        g0 = G_coeffs(w, n, k, d)
        if g0 is None:
            continue
        J = np.zeros((k + 1, P))
        h = 1e-6
        for j in range(P):
            wp = w.copy(); wp[j] += h
            wm = w.copy(); wm[j] -= h
            gp, gm = G_coeffs(wp, n, k, d), G_coeffs(wm, n, k, d)
            if gp is None or gm is None:
                break
            J[:, j] = (gp[1:] - gm[1:]) / (2 * h)
        sv = np.linalg.svd(J, compute_uv=False)
        ranks.append(int(np.sum(sv > tol * max(sv[0], 1.0))))
    return ranks


if __name__ == "__main__":
    print("Dimension of the reachable set of symbols G(sigma), by period d")
    print("(target: rank k+1 means every G is locally reachable)\n")
    print(f"{'k':>3} {'d':>3} {'params 5d':>10} {'k+1':>5} {'Jacobian rank':>14}"
          f"  verdict")
    for k in (3, 4, 5, 6, 7, 8):
        for d in (1, 2, 3, 4):
            n = d * (2 * k + 8)                 # any n with d | n and m large
            if 2 * k >= n:
                continue
            ranks = jac_rank(n, k, d)
            if not ranks:
                continue
            rk = max(ranks)
            full = (rk == k + 1)
            print(f"{k:>3} {d:>3} {5*d:>10} {k+1:>5} {rk:>14}  "
                  f"{'FULL - every G reachable' if full else 'deficient'}",
                  flush=True)
