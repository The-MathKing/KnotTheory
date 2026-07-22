"""
General (non-equivariant) maximum-nullity certificates for P(n,k).

Structural background (verified in verification/recurrence_order.py):
for A in S(P(n,k)) the kernel equations at u_i and v_i are

    (O_i)  b_{i-1} x_{i-1} + a_i x_i + b_i x_{i+1} + c_i y_i = 0
    (I_i)  e_{i-k} y_{i-k} + d_i y_i + e_i y_{i+k} + c_i x_i = 0.

Every spoke weight c_i is nonzero, so (O_i) solves for y_i, and
substituting into (I_i) leaves one scalar linear recurrence in x supported
on the 2k+3 consecutive indices i-k-1,...,i+k+1 with both end
coefficients nonzero.  Therefore

    nullity(A) = dim ker(T - I) <= 2k+2,

T being the monodromy of that order-(2k+2) recurrence, with equality iff
T = I.  A rho-equivariant A forces T = T_1^n, whose fixed space is cut out
by a 3-parameter family of degree-(k+1) symbols; that is exactly why the
equivariant constructions stall at 6 (period 1) and 8 (period 2).  This
module drops equivariance entirely and searches the full 5n-dimensional
weight space for T = I.

The search solves  A(w) X = 0,  X^T X = I  in the weights w and a
2n x r kernel basis X, by alternating exact sub-solves (w from the
smallest singular vector of the linear map X -> A(w)X; X from the
invariant subspace of A(w)) followed by Gauss-Newton with an analytic
Jacobian.
"""
import numpy as np
from scipy.optimize import least_squares


def pattern_matrices(n, k):
    """Symmetric pattern generators for S(P(n,k)), with labels.

    Order: b_0..b_{n-1} (outer edges), c_0..c_{n-1} (spokes),
    e_0..e_{n-1} (inner edges), a_0..a_{n-1}, d_0..d_{n-1} (diagonals).
    """
    N = 2 * n
    mats, labels = [], []

    def sym(p, q):
        E = np.zeros((N, N)); E[p, q] = E[q, p] = 1.0
        return E

    for i in range(n):
        mats.append(sym(i, (i + 1) % n)); labels.append(("b", i))
    for i in range(n):
        mats.append(sym(i, n + i)); labels.append(("c", i))
    for i in range(n):
        mats.append(sym(n + i, n + (i + k) % n)); labels.append(("e", i))
    for i in range(n):
        E = np.zeros((N, N)); E[i, i] = 1.0
        mats.append(E); labels.append(("a", i))
    for i in range(n):
        E = np.zeros((N, N)); E[n + i, n + i] = 1.0
        mats.append(E); labels.append(("d", i))
    return np.array(mats), labels


def assemble(w, mats):
    return np.tensordot(w, mats, axes=(0, 0))


def w_from_X(X, mats):
    """Exact sub-solve: the unit w minimising ||A(w)X||_F, plus the two
    smallest singular values of that linear map (the second reports how
    far the minimiser is from being unique)."""
    M = np.stack([(E @ X).ravel() for E in mats], axis=1)
    U, sv, Vt = np.linalg.svd(M, full_matrices=False)
    return Vt[-1], sv[-1], (sv[-2] if len(sv) > 1 else np.inf)


def X_from_w(w, mats, r):
    A = assemble(w, mats)
    lam, Q = np.linalg.eigh(A)
    idx = np.argsort(np.abs(lam))[:r]
    return Q[:, idx]


def _res_jac(z, mats, n, r, nz_idx, tau, P):
    N = 2 * n
    w = z[:P]
    X = z[P:].reshape(N, r)
    A = assemble(w, mats)
    AX = A @ X
    G = X.T @ X - np.eye(r)
    iu = np.triu_indices(r)
    act = np.maximum(0.0, tau - np.abs(w[nz_idx]))
    res = np.concatenate([AX.ravel(), G[iu], [w @ w - P], act])

    nr = N * r
    ng = len(iu[0])
    nz = len(nz_idx)
    J = np.zeros((nr + ng + 1 + nz, P + N * r))
    # d vec(A X) / dw_j = vec(E_j X)
    for j, E in enumerate(mats):
        J[:nr, j] = (E @ X).ravel()
    # d vec(A X) / d vec(X) = kron(A, I_r)   (row-major flattening)
    J[:nr, P:] = np.kron(A, np.eye(r))
    # d (X^T X)_{ab} / dX[m,q] = delta_{qa} X[m,b] + delta_{qb} X[m,a]
    for t, (aa, bb) in enumerate(zip(*iu)):
        D = np.zeros((N, r))
        D[:, aa] += X[:, bb]
        D[:, bb] += X[:, aa]
        J[nr + t, P:] = D.ravel()
    J[nr + ng, :P] = 2.0 * w
    for t, j in enumerate(nz_idx):
        if act[t] > 0:
            J[nr + ng + 1 + t, j] = -np.sign(w[j])
    return res, J


def refine(w, X, mats, n, r, nz_idx, tau):
    P = len(mats)
    z0 = np.concatenate([w, X.ravel()])
    sol = least_squares(lambda z: _res_jac(z, mats, n, r, nz_idx, tau, P)[0], z0,
                        jac=lambda z: _res_jac(z, mats, n, r, nz_idx, tau, P)[1],
                        method="trf", xtol=1e-15, ftol=1e-15, gtol=1e-15,
                        max_nfev=300)
    return sol.x[:P], sol.x[P:].reshape(2 * n, r), sol.cost


def quality(w, mats, n, r, nz_idx):
    A = assemble(w, mats)
    ev = np.sort(np.abs(np.linalg.eigvalsh(A)))
    scale = np.abs(A).max()
    small = ev[r - 1] / scale
    gap = ev[r] / scale
    minnz = np.abs(w[nz_idx]).min() / scale
    return small, gap, minnz, ev


def search(n, k, r=None, tries=30, seed=0, tau=0.15, alt=60, verbose=True):
    if r is None:
        r = 2 * k + 2
    mats, labels = pattern_matrices(n, k)
    P = len(mats)
    nz_idx = np.array([j for j, (t, _) in enumerate(labels) if t in ("b", "c", "e")])
    rng = np.random.default_rng(seed)
    best = None
    for t in range(tries):
        w = rng.standard_normal(P)
        w /= np.linalg.norm(w) / np.sqrt(P)
        for _ in range(alt):                      # alternating exact sub-solves
            X = X_from_w(w, mats, r)
            wn, s1, s2 = w_from_X(X, mats)
            if wn @ w < 0:
                wn = -wn
            w = wn * np.sqrt(P)
        X = X_from_w(w, mats, r)
        w, X, cost = refine(w, X, mats, n, r, nz_idx, tau)
        small, gap, minnz, ev = quality(w, mats, n, r, nz_idx)
        ok = small < 1e-9 and gap > 1e-3 and minnz > 1e-2
        if verbose:
            print(f"  try {t:3d}  |lam_{r}|/scale={small:.2e}  "
                  f"|lam_{r+1}|/scale={gap:.2e}  min|req.wt|/scale={minnz:.4f}"
                  f"  {'ADMISSIBLE' if ok else ''}", flush=True)
        if ok and (best is None or minnz > best[2]):
            best = (w.copy(), gap, minnz, ev)
    return best, mats, labels


if __name__ == "__main__":
    import sys
    n, k = int(sys.argv[1]), int(sys.argv[2])
    tries = int(sys.argv[3]) if len(sys.argv) > 3 else 15
    r = int(sys.argv[4]) if len(sys.argv) > 4 else 2 * k + 2
    print(f"P({n},{k}): searching for A in S(P(n,k)) of nullity r={r} "
          f"(2k+2 = {2*k+2})", flush=True)
    best, mats, labels = search(n, k, r=r, tries=tries)
    if best is None:
        print("  RESULT: no admissible certificate of that nullity found")
    else:
        w, gap, minnz, ev = best
        print(f"  RESULT: admissible certificate found. spectral gap "
              f"{gap:.2e}, min required |weight|/scale {minnz:.4f}")
        print(f"  |eigenvalues| (smallest {r+3}): "
              f"{np.array2string(ev[:r+3], precision=3)}")
        np.save(f"/private/tmp/claude-501/-Volumes-2TB-scifair/"
                f"9a5c5e2b-1fe0-482d-ace4-6f9c0ccaccd9/scratchpad/"
                f"cert_{n}_{k}_{r}.npy", w)
