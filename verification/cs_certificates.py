"""
Combinatorially symmetric (not necessarily symmetric) nullity certificates.

The inequality behind every matrix lower bound on Z does not need symmetry.

LEMMA.  Let A be a real matrix indexed by V(G) with A_{uv} != 0 iff
uv in E(G), for u != v; the diagonal is arbitrary and A need NOT be
symmetric.  If S is a zero forcing set and Ax = 0 with x|_S = 0, then
x = 0.  Proof: suppose x vanishes on B and u in B has exactly one
neighbour w outside B.  Row u of Ax = 0 reads
A_{uu}x_u + sum_{v ~ u} A_{uv} x_v = 0; every term vanishes except
A_{uw}x_w, and A_{uw} != 0 because uw is an edge, so x_w = 0.  Induct
along the forcing process to get x = 0 on cl(S) = V.  Hence
x -> x|_S is injective on ker A and

        nullity(A) <= |S|,    so    nullity(A) <= Z(G).

So with  M_cs(G) = max nullity over this class,   M(G) <= M_cs(G) <= Z(G),
and a certificate in the larger class is just as rigorous a lower bound on
Z as a symmetric one.  For P(n,k) the class has 8n free parameters
(two per edge plus one per vertex) against 5n in the symmetric case, while
the structural ceiling is unchanged: eliminating y from

    (O_i)  b'_{i-1} x_{i-1} + a_i x_i + b_i x_{i+1} + c_i y_i = 0
    (I_i)  e'_{i-k} y_{i-k} + d_i y_i + e_i y_{i+k} + c'_i x_i = 0

still leaves one scalar recurrence of order 2k+2, so nullity <= 2k+2 here
too (see verification/recurrence_order.py).
"""
import numpy as np
from scipy.optimize import least_squares


def pattern_matrices(n, k, symmetric=False):
    """Generators for the pattern class of P(n,k).

    symmetric=True  -> one generator per edge (E_{pq} + E_{qp}), 5n total.
    symmetric=False -> two generators per edge, 8n total.
    Returns (generators, labels); labels[j][0] == 'diag' marks a diagonal.
    """
    N = 2 * n
    mats, labels = [], []
    edges = ([(i, (i + 1) % n, "b", i) for i in range(n)]
             + [(i, n + i, "c", i) for i in range(n)]
             + [(n + i, n + (i + k) % n, "e", i) for i in range(n)])
    for (p, q, tag, i) in edges:
        if symmetric:
            E = np.zeros((N, N)); E[p, q] = E[q, p] = 1.0
            mats.append(E); labels.append((tag, i, "sym"))
        else:
            E = np.zeros((N, N)); E[p, q] = 1.0
            mats.append(E); labels.append((tag, i, "fwd"))
            E = np.zeros((N, N)); E[q, p] = 1.0
            mats.append(E); labels.append((tag, i, "bwd"))
    for v in range(N):
        E = np.zeros((N, N)); E[v, v] = 1.0
        mats.append(E); labels.append(("diag", v, ""))
    return np.array(mats), labels


def assemble(w, mats):
    return np.tensordot(w, mats, axes=(0, 0))


def _safe_svd(M, full_matrices=True):
    """numpy's LAPACK driver occasionally fails to converge on the badly
    scaled iterates this search produces; fall back to the eigendecomposition
    of M^T M, which is slower but robust."""
    try:
        return np.linalg.svd(M, full_matrices=full_matrices)
    except np.linalg.LinAlgError:
        G = M.T @ M
        lam, Vt = np.linalg.eigh(G)
        order = np.argsort(lam)[::-1]
        sv = np.sqrt(np.clip(lam[order], 0.0, None))
        V = Vt[:, order]
        return None, sv, V.T


def X_from_w(w, mats, r):
    """Right null space candidate: right singular vectors of the r smallest
    singular values (A is not symmetric, so use the SVD, not eigh)."""
    A = assemble(w, mats)
    _, sv, Vt = _safe_svd(A)
    return Vt[-r:].T


def w_from_X(X, mats):
    M = np.stack([(E @ X).ravel() for E in mats], axis=1)
    _, sv, Vt = _safe_svd(M, full_matrices=False)
    return Vt[-1], sv[-1]


def _res_jac(z, mats, N, r, nz_idx, tau, P):
    w = z[:P]
    X = z[P:].reshape(N, r)
    A = assemble(w, mats)
    G = X.T @ X - np.eye(r)
    iu = np.triu_indices(r)
    act = np.maximum(0.0, tau - np.abs(w[nz_idx]))
    res = np.concatenate([(A @ X).ravel(), G[iu], [w @ w - P], act])

    nr = N * r
    ng = len(iu[0])
    J = np.zeros((nr + ng + 1 + len(nz_idx), P + N * r))
    for j, E in enumerate(mats):
        J[:nr, j] = (E @ X).ravel()
    J[:nr, P:] = np.kron(A, np.eye(r))
    for t, (aa, bb) in enumerate(zip(*iu)):
        D = np.zeros((N, r)); D[:, aa] += X[:, bb]; D[:, bb] += X[:, aa]
        J[nr + t, P:] = D.ravel()
    J[nr + ng, :P] = 2.0 * w
    for t, j in enumerate(nz_idx):
        if act[t] > 0:
            J[nr + ng + 1 + t, j] = -np.sign(w[j])
    return res, J


def quality(w, mats, r, nz_idx):
    A = assemble(w, mats)
    sv = np.sort(_safe_svd(A)[1])
    scale = np.abs(A).max()
    return sv[r - 1] / scale, sv[r] / scale, np.abs(w[nz_idx]).min() / scale, sv


def embed_sym(w_sym, n, k):
    """Map a symmetric weight vector (5n) into the cs parametrisation (8n)
    by duplicating each edge weight into its two directed entries."""
    _, lab_s = pattern_matrices(n, k, symmetric=True)
    _, lab_c = pattern_matrices(n, k, symmetric=False)
    val = {(t, i): w_sym[j] for j, (t, i, _) in enumerate(lab_s)
           if t != "diag"}
    dia = {i: w_sym[j] for j, (t, i, _) in enumerate(lab_s) if t == "diag"}
    out = np.zeros(len(lab_c))
    for j, (t, i, side) in enumerate(lab_c):
        out[j] = dia[i] if t == "diag" else val[(t, i)]
    return out


def search(n, k, r=None, tries=30, seed=0, tau=0.12, alt=50,
           symmetric=False, verbose=True, w_init=None, jitter=0.25,
           max_nfev=400):
    """If w_init is given, every start is a jittered copy of it instead of
    a fresh random point."""
    if r is None:
        r = 2 * k + 2
    mats, labels = pattern_matrices(n, k, symmetric=symmetric)
    N, P = 2 * n, len(mats)
    nz_idx = np.array([j for j, L in enumerate(labels) if L[0] != "diag"])
    rng = np.random.default_rng(seed)
    best, plateaus = None, []
    for t in range(tries):
        if w_init is None:
            w = rng.standard_normal(P)
        else:
            w = w_init + (0.0 if t == 0 else jitter) * rng.standard_normal(P)
        w *= np.sqrt(P) / np.linalg.norm(w)
        for _ in range(0 if w_init is not None else alt):
            if not np.all(np.isfinite(w)):
                break
            X = X_from_w(w, mats, r)
            wn, _ = w_from_X(X, mats)
            if not np.all(np.isfinite(wn)):
                break
            if wn @ w < 0:
                wn = -wn
            w = wn * np.sqrt(P)          # keep the scale fixed each step
        X = X_from_w(w, mats, r)
        z0 = np.concatenate([w, X.ravel()])
        sol = least_squares(lambda z: _res_jac(z, mats, N, r, nz_idx, tau, P)[0],
                            z0,
                            jac=lambda z: _res_jac(z, mats, N, r, nz_idx, tau, P)[1],
                            method="trf", xtol=1e-15, ftol=1e-15, gtol=1e-15,
                            max_nfev=max_nfev)
        w = sol.x[:P]
        small, gap, minnz, sv = quality(w, mats, r, nz_idx)
        plateaus.append(small)
        ok = small < 1e-9 and gap > 1e-3 and minnz > 1e-2
        if verbose:
            print(f"  try {t:3d}  sv_{r}/scale={small:.2e}  sv_{r+1}/scale={gap:.2e}"
                  f"  min|req|/scale={minnz:.4f}  {'ADMISSIBLE' if ok else ''}",
                  flush=True)
        if ok and (best is None or minnz > best[2]):
            best = (w.copy(), gap, minnz, sv)
    return best, mats, labels, np.array(plateaus)


if __name__ == "__main__":
    import sys
    n, k = int(sys.argv[1]), int(sys.argv[2])
    r = int(sys.argv[3]) if len(sys.argv) > 3 else 2 * k + 2
    tries = int(sys.argv[4]) if len(sys.argv) > 4 else 12
    sym = len(sys.argv) > 5 and sys.argv[5] == "sym"
    print(f"P({n},{k}) target nullity r={r} (2k+2={2*k+2}), "
          f"{'symmetric' if sym else 'combinatorially symmetric'} class",
          flush=True)
    best, mats, labels, plat = search(n, k, r=r, tries=tries, symmetric=sym)
    if best is None:
        print("  RESULT: none found")
    else:
        w, gap, minnz, sv = best
        print(f"  RESULT: ADMISSIBLE certificate of nullity {r}; "
              f"sv gap {gap:.2e}, min required |entry|/scale {minnz:.4f}")
        print(f"  singular values (smallest {r+3}): "
              f"{np.array2string(np.sort(sv)[:r+3], precision=3)}")
        np.save(f"/private/tmp/claude-501/-Volumes-2TB-scifair/"
                f"9a5c5e2b-1fe0-482d-ace4-6f9c0ccaccd9/scratchpad/"
                f"cs_{n}_{k}_{r}.npy", w)
