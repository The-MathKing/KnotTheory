"""
Fast search for high-nullity matrices with the pattern of P(n,k).

Both matrix classes give rigorous lower bounds on Z (lemma at the top of
verification/cs_certificates.py):
  sym : real symmetric, A_{uv} != 0 iff uv in E(G), free diagonal   (5n params)
  cs  : combinatorially symmetric, symmetry not required            (8n params)
and verification/recurrence_order.py shows both are capped at nullity 2k+2.

Formulation.  Instead of the bilinear system A(w)X = 0, X^T X = I (which needs
a Jacobian with 2nr rows), minimise directly

    f(w) = sum of the r smallest lambda_j(A(w))^2      [sym]
    f(w) = sum of the r smallest sigma_j(A(w))^2       [cs]

subject to ||w||^2 = P, with a barrier keeping the required-nonzero entries
away from 0.  The gradients are analytic and cheap:
    d(lambda^2)/dw_j = 2 lambda  q^T E_j q,
    d(sigma^2)/dw_j  = 2 sigma   u^T E_j v,
and each generator E_j has one or two nonzero entries, so every quadratic
form is O(1).  One function evaluation is a single 2n x 2n eigendecomposition
(or SVD), which makes thousands of random starts affordable -- necessary,
because the question being asked is whether a solution exists at all.
"""
import numpy as np
from scipy.optimize import minimize


def generators(n, k, symmetric):
    """Each generator is a list of (row, col) positions carrying weight 1.
    Returns (gens, is_required_nonzero)."""
    gens, req = [], []
    edges = ([(i, (i + 1) % n) for i in range(n)]
             + [(i, n + i) for i in range(n)]
             + [(n + i, n + (i + k) % n) for i in range(n)])
    for (p, q) in edges:
        if symmetric:
            gens.append([(p, q), (q, p)]); req.append(True)
        else:
            gens.append([(p, q)]); req.append(True)
            gens.append([(q, p)]); req.append(True)
    for v in range(2 * n):
        gens.append([(v, v)]); req.append(False)
    return gens, np.array(req)


def _flat(gens, n):
    N = 2 * n
    rows = np.concatenate([[p for (p, q) in g] for g in gens])
    cols = np.concatenate([[q for (p, q) in g] for g in gens])
    owner = np.concatenate([[j] * len(g) for j, g in enumerate(gens)])
    return rows, cols, owner, N


def assemble(w, rows, cols, owner, N):
    A = np.zeros((N, N))
    np.add.at(A, (rows, cols), w[owner])
    return A


def objective(w, rows, cols, owner, N, r, req, tau, mu, symmetric):
    A = assemble(w, rows, cols, owner, N)
    P = len(req)
    if symmetric:
        lam, Q = np.linalg.eigh(A)
        idx = np.argsort(np.abs(lam))[:r]
        vals, L, R = lam[idx], Q[:, idx], Q[:, idx]
    else:
        Uu, sv, Vt = np.linalg.svd(A)
        idx = np.argsort(sv)[:r]
        vals, L, R = sv[idx], Uu[:, idx], Vt[idx].T
    scale = max(np.abs(A).max(), 1e-12)
    f = float(np.sum((vals / scale) ** 2))
    # d(val^2)/dw_j = 2 val * sum_{(p,q) in E_j} L[p,t] R[q,t]
    contrib = 2.0 * (vals / scale ** 2)[None, :] * (L[rows, :] * R[cols, :])
    g = np.zeros(P)
    np.add.at(g, owner, contrib.sum(axis=1))
    # barrier on the required-nonzero entries, and the scale constraint
    wr = w[req]
    viol = np.maximum(0.0, tau - np.abs(wr) / scale)
    f += mu * float(np.sum(viol ** 2))
    gb = np.zeros(P)
    gb[req] = -2.0 * mu * viol * np.sign(wr) / scale
    f += 1e-3 * (w @ w / P - 1.0) ** 2
    g += gb + 1e-3 * 2.0 * (w @ w / P - 1.0) * 2.0 * w / P
    return f, g


def report(w, rows, cols, owner, N, r, req, symmetric):
    A = assemble(w, rows, cols, owner, N)
    scale = np.abs(A).max()
    vals = (np.sort(np.abs(np.linalg.eigvalsh(A))) if symmetric
            else np.sort(np.linalg.svd(A, compute_uv=False)))
    return vals[r - 1] / scale, vals[r] / scale, np.abs(w[req]).min() / scale, vals


def polish(w, n, k, r, symmetric, rows, cols, owner, N, req, tau=0.05,
           max_nfev=400):
    """Quadratically convergent clean-up of a near-solution.

    L-BFGS-B on the eigenvalue objective stalls near 1e-8 because the
    objective is only piecewise smooth at eigenvalue crossings.  Switching to
    the bilinear system  A(w) X = 0,  X^T X = I  with an analytic Jacobian
    converges to machine precision, so the two-stage scheme is: filter cheaply
    over many random starts, then polish the best candidates here."""
    from scipy.optimize import least_squares
    P = len(req)
    A = assemble(w, rows, cols, owner, N)
    if symmetric:
        lam, Q = np.linalg.eigh(A)
        X = Q[:, np.argsort(np.abs(lam))[:r]]
    else:
        X = np.linalg.svd(A)[2][-r:].T
    iu = np.triu_indices(r)
    nzi = np.where(req)[0]

    def res_jac(z):
        ww, XX = z[:P], z[P:].reshape(N, r)
        AA = assemble(ww, rows, cols, owner, N)
        act = np.maximum(0.0, tau - np.abs(ww[nzi]))
        G = XX.T @ XX - np.eye(r)
        res = np.concatenate([(AA @ XX).ravel(), G[iu], [ww @ ww - P], act])
        nr, ng = N * r, len(iu[0])
        J = np.zeros((nr + ng + 1 + len(nzi), P + N * r))
        # d vec(A X)/dw: generator j contributes X[q,:] into rows p*r..p*r+r
        np.add.at(J, (np.add.outer(rows * r, np.arange(r)).ravel(),
                      np.repeat(owner, r)), XX[cols, :].ravel())
        J[:nr, P:] = np.kron(AA, np.eye(r))
        for t, (aa, bb) in enumerate(zip(*iu)):
            D = np.zeros((N, r)); D[:, aa] += XX[:, bb]; D[:, bb] += XX[:, aa]
            J[nr + t, P:] = D.ravel()
        J[nr + ng, :P] = 2.0 * ww
        for t, j in enumerate(nzi):
            if act[t] > 0:
                J[nr + ng + 1 + t, j] = -np.sign(ww[j])
        return res, J

    sol = least_squares(lambda z: res_jac(z)[0], np.concatenate([w, X.ravel()]),
                        jac=lambda z: res_jac(z)[1], method="trf",
                        xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=max_nfev)
    return sol.x[:P]


def search(n, k, r, symmetric=True, tries=300, seed=0, tau=0.05, mu=30.0,
           w_init=None, jitter=0.3, n_polish=12):
    gens, req = generators(n, k, symmetric)
    rows, cols, owner, N = _flat(gens, n)
    P = len(gens)
    rng = np.random.default_rng(seed)
    best, plateaus, cands = None, [], []
    for t in range(tries):
        w0 = (rng.standard_normal(P) if w_init is None
              else w_init + (0.0 if t == 0 else jitter) * rng.standard_normal(P))
        w0 *= np.sqrt(P) / np.linalg.norm(w0)
        res = minimize(objective, w0, jac=True, method="L-BFGS-B",
                       args=(rows, cols, owner, N, r, req, tau, mu, symmetric),
                       options=dict(maxiter=3000, ftol=1e-18, gtol=1e-14))
        small, gap, minnz, vals = report(res.x, rows, cols, owner, N, r, req,
                                         symmetric)
        plateaus.append(small)
        cands.append((small, res.x.copy()))
    # polish the most promising candidates
    cands.sort(key=lambda t: t[0])
    polished = []
    for (_, w) in cands[:n_polish]:
        wp = polish(w, n, k, r, symmetric, rows, cols, owner, N, req, tau=tau)
        small, gap, minnz, vals = report(wp, rows, cols, owner, N, r, req,
                                        symmetric)
        polished.append(small)
        if small < 1e-9 and gap > 1e-3 and minnz > 1e-2:
            if best is None or minnz > best[2]:
                best = (wp.copy(), gap, minnz, vals)
    return best, np.array(plateaus), np.array(polished)


if __name__ == "__main__":
    import sys, time
    n, k, r = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    tries = int(sys.argv[4]) if len(sys.argv) > 4 else 200
    sym = not (len(sys.argv) > 5 and sys.argv[5] == "cs")
    t0 = time.time()
    best, plat, pol = search(n, k, r, symmetric=sym, tries=tries)
    print(f"P({n},{k}) r={r} ({'sym' if sym else 'cs'}) 2k+2={2*k+2}  "
          f"{tries} starts in {time.time()-t0:.1f}s")
    print(f"  pre-polish plateau  min {plat.min():.2e}  median {np.median(plat):.2e}")
    print(f"  post-polish plateau min {pol.min():.2e}  median {np.median(pol):.2e}")
    print("  RESULT:", "ADMISSIBLE CERTIFICATE "
          f"(gap {best[1]:.1e}, min required |entry|/scale {best[2]:.3f})"
          if best else "none found")
