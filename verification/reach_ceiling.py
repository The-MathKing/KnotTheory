"""Reach nullity 2k+2 on P(n,k) via the bilinear system A(w) K = 0.

Far cheaper than optimising T = I: with K fixed the system is affine in w (a
linear solve), and with w fixed the best K is an SVD.  Two devices keep it off
the degenerate strata:

  * All spokes are fixed to 1.  This is WLOG -- positive diagonal conjugation
    D A D scales the spoke A[i,n+i] by d_i d_{n+i}, so d_{n+i} = 1/(d_i c_i)
    normalises every spoke while preserving symmetry, pattern and nullity.  It
    also makes the w-system AFFINE rather than homogeneous, so w cannot collapse
    to zero.
  * A homotopy on the remaining edge weights: minimise
    ||A(w)K||^2 + lam * sum (|w_edge| - 1)^2 with lam decreasing to ~0.  At
    large lam the edges are held near +-1; as lam falls the iterate slides onto
    the true variety while staying off the all-edges-zero stratum, which
    otherwise attracts (with spokes 1 and all edges 0 the matrix splits into
    2x2 blocks [[d_i,1],[1,D_i]] and any 2k+2 of them can be made singular).
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import sys

import numpy as np


def cells_spoke1(n, k):
    """Free weight slots (a, d, b, e); spokes are fixed to 1."""
    cells = [("a", [(i, i)]) for i in range(n)]
    cells += [("d", [(n + i, n + i)]) for i in range(n)]
    cells += [("b", [(i, (i + 1) % n), ((i + 1) % n, i)]) for i in range(n)]
    cells += [("e", [(n + i, n + (i + k) % n), (n + (i + k) % n, n + i)])
              for i in range(n)]
    S = np.zeros((2 * n, 2 * n))
    for i in range(n):
        S[i, n + i] = S[n + i, i] = 1.0
    return cells, S


def assemble(w, cells, S):
    A = S.copy()
    for wj, (_, cl) in zip(w, cells):
        for (i, j) in cl:
            A[i, j] = wj
    return A


def solve(n, k, tries=40, iters=300, seed=0):
    r = 2 * k + 2
    cells, S = cells_spoke1(n, k)
    N, P = 2 * n, len(cells)
    nedge = 2 * n                      # the b and e blocks
    rows = np.concatenate([[c[0] for c in cl] for _, cl in cells])
    cols = np.concatenate([[c[1] for c in cl] for _, cl in cells])
    jidx = np.concatenate([[j] * len(cl) for j, (_, cl) in enumerate(cells)])
    rng = np.random.default_rng(seed)
    best = None
    for t in range(tries):
        w = rng.standard_normal(P)
        w[2 * n:] = np.sign(rng.standard_normal(nedge))      # edges at +-1
        A = assemble(w, cells, S)
        K = np.linalg.svd(A)[2][-r:].T
        for it in range(iters):
            lam = 1.0 * (0.94 ** it) + 1e-9
            T = np.zeros((P, N, r))
            np.add.at(T, (jidx, rows), K[cols])
            M = T.reshape(P, N * r).T
            rhs = -(S @ K).ravel()
            # homotopy rows: sqrt(lam) * (w_edge - sign(w_edge))
            Mh = np.zeros((nedge, P)); Mh[np.arange(nedge), 2 * n + np.arange(nedge)] = 1.0
            tgt = np.sign(w[2 * n:]); tgt[tgt == 0] = 1.0
            Mfull = np.vstack([M, np.sqrt(lam) * Mh])
            rfull = np.concatenate([rhs, np.sqrt(lam) * tgt])
            w, *_ = np.linalg.lstsq(Mfull, rfull, rcond=None)
            A = assemble(w, cells, S)
            sv = np.linalg.svd(A, compute_uv=False)
            K = np.linalg.svd(A)[2][-r:].T
        sc = np.abs(A).max()
        obj = sv[-r] / sc
        me = np.abs(w[2 * n:]).min() / sc
        cand = (obj, -me, w.copy())
        if best is None or cand[0] < best[0]:
            best = cand
    w = best[2]
    A = assemble(w, cells, S)
    sv = np.linalg.svd(A, compute_uv=False)
    sc = np.abs(A).max()
    return int(np.sum(sv < 1e-9 * sc)), sv[-r] / sc, np.abs(w[2*n:]).min() / sc, sv, w


def is_prime(m):
    return m > 1 and all(m % d for d in range(2, int(m ** 0.5) + 1))


if __name__ == "__main__":
    k = int(sys.argv[1]); ns = [int(x) for x in sys.argv[2:]]
    r = 2 * k + 2
    print(f"k = {k}   target nullity 2k+2 = {r}   "
          f"(codim count: 4n >= {(k+1)*(2*k+3)}  =>  n >= "
          f"{int(np.ceil((k+1)*(2*k+3)/4))})")
    print("    n  prime   r-th sv / scale   min|edge|/scale   nullity   verdict")
    for n in ns:
        if 2 * k >= n:
            print(f" {n:4d}   (needs n > 2k)"); continue
        nul, obj, me, sv, w = solve(n, k)
        np.save(f"{_REPO}/results/zero_forcing/ws1_{n}_{k}.npy", w)
        print(f" {n:4d}   {'yes' if is_prime(n) else ' no'}{obj:18.3e}"
              f"{me:18.4f}{nul:10d}   {'CEILING' if nul >= r else 'no'}")
