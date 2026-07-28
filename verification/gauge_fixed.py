"""Fully gauge-fixed search for a nullity-(2k+2) matrix on P(n,k).

Positive diagonal conjugation A -> D A D has 2n parameters and preserves
symmetry, the pattern and the nullity.  Spend them all:

  * the n inner d's set every SPOKE to 1   (d_{n+i} = 1/(d_i c_i));
  * the n outer d's set every OUTER edge to +-1, since b_i -> d_i d_{i+1} b_i
    and u_i + u_{i+1} = -log|b_i| is uniquely solvable for n odd.  The signs
    are not free: the product of the signs of the b_i around the cycle is a
    gauge invariant, so there are exactly two slices, all b_i = +1 and all +1
    but one -1.  Both are tried.

What is left is 2n diagonal entries and n inner edge weights: 3n unknowns with
NO residual gauge, so the Jacobian is generically of full rank and the solution
variety of A K = 0 has dimension

    [3n + (2n - r) r] - [(2n - r) r + C(r+1,2)] = 3n - (k+1)(2k+3),

nonnegative exactly when n >= (k+1)(2k+3)/3.  That is the honest threshold:
7, 12, 19, 26, 35, 46, 57 for k = 2..8.  Searching below it cannot succeed.

Removing the outer-edge freedom also removes the degenerate stratum that
defeated the earlier searches (all outer weights -> 0); only the inner edges
still need a homotopy holding them away from zero.
"""
import sys

import numpy as np


def cells_fixed(n, k, sign=+1):
    """Free slots: n outer diagonals, n inner diagonals, n inner edges, and for
    EVEN n one outer edge as well.

    On an odd cycle u_i + u_{i+1} = -log|b_i| is uniquely solvable, so every
    outer weight can be driven to +-1.  On an even cycle the system is singular:
    it is solvable only when the alternating product of the |b_i| is 1, so one
    outer weight must be left free and one gauge direction survives.  The extra
    unknown and the surviving gauge cancel, and the solution variety still has
    dimension 3n - C(r+1,2)."""
    cells = [("a", [(i, i)]) for i in range(n)]
    cells += [("d", [(n + i, n + i)]) for i in range(n)]
    cells += [("e", [(n + i, n + (i + k) % n), (n + (i + k) % n, n + i)])
              for i in range(n)]
    if n % 2 == 0:
        cells += [("b0", [(0, 1 % n), (1 % n, 0)])]
    S = np.zeros((2 * n, 2 * n))
    for i in range(n):
        S[i, n + i] = S[n + i, i] = 1.0                 # spokes
        j = (i + 1) % n
        if n % 2 == 0 and i == 0:
            continue                                    # b_0 is a free unknown
        S[i, j] = S[j, i] = sign if i == 0 else 1.0     # outer edges at +-1
    return cells, S


def assemble(w, cells, S):
    A = S.copy()
    for wj, (_, cl) in zip(w, cells):
        for (i, j) in cl:
            A[i, j] = wj
    return A


def resample(w_prev, n_prev, n_new):
    """Carry a solution at n_prev to a starting point at n_new by resampling the
    three weight sequences (outer diagonal, inner diagonal, inner edge) in the
    position index.  Nothing about this is canonical -- it only has to land in
    the basin of the Newton step, which is all stage 1 is for."""
    import numpy as _np
    blocks = [w_prev[:n_prev], w_prev[n_prev:2*n_prev], w_prev[2*n_prev:3*n_prev]]
    xs_new = _np.linspace(0.0, 1.0, n_new, endpoint=False)
    xs_old = _np.linspace(0.0, 1.0, n_prev, endpoint=False)
    out = []
    for blk in blocks:
        ext = _np.concatenate([blk, blk[:1]])
        xo = _np.concatenate([xs_old, [1.0]])
        out.append(_np.interp(xs_new, xo, ext))
    w = _np.concatenate(out)
    if n_new % 2 == 0:                     # even n carries a free outer weight
        w = _np.concatenate([w, [1.0]])
    return w


def solve(n, k, sign=+1, tries=60, iters=500, seed=0, ladder=True, w0=None):
    """Continuation in the target nullity: reaching 2k+2 directly is hard, so
    aim for 2, then 4, ..., then 2k+2, warm-starting the weights each time.
    Each step of the ladder is a small perturbation of the last."""
    if w0 is not None:
        # warm start: skip the ladder, go straight for the full target
        return _run(n, k, sign, 2 * k + 2, iters, seed, w0=w0)
    if ladder:
        best = None
        for t in range(tries):
            w = None
            for rr in range(2, 2 * k + 3, 2):
                obj, me, w = _run(n, k, sign, rr, iters, seed + 991 * t, w0=w)
                if not np.all(np.isfinite(w)):
                    break
            if np.all(np.isfinite(w)):
                cand = (obj, me, w.copy())
                if best is None or cand[0] < best[0]:
                    best = cand
        if best is None:
            cells, S = cells_fixed(n, k, sign)
            return (np.inf, 0.0, np.zeros(len(cells)))
        return best
    return _run(n, k, sign, 2 * k + 2, iters, seed)


def _run(n, k, sign, r, iters, seed, w0=None):
    cells, S = cells_fixed(n, k, sign)
    N, P = 2 * n, len(cells)
    rows = np.concatenate([[c[0] for c in cl] for _, cl in cells])
    cols = np.concatenate([[c[1] for c in cl] for _, cl in cells])
    jidx = np.concatenate([[j] * len(cl) for j, (_, cl) in enumerate(cells)])
    ne = n                                              # the n inner edges
    e0 = 2 * n                                          # where they start
    rng = np.random.default_rng(seed)
    best = None
    for t in range(1):
        if w0 is None:
            w = rng.standard_normal(P)
            w[e0:e0 + ne] = np.sign(rng.standard_normal(ne))
        else:
            w = w0.copy()
        A = assemble(w, cells, S)
        K = np.linalg.svd(A)[2][-r:].T
        sv = None
        for it in range(iters):
            lam = 0.5 * (0.97 ** it) + 1e-10
            T = np.zeros((P, N, r))
            np.add.at(T, (jidx, rows), K[cols])
            M = T.reshape(P, N * r).T
            Mh = np.zeros((ne, P))
            Mh[np.arange(ne), e0 + np.arange(ne)] = 1.0
            tgt = np.sign(w[e0:e0 + ne]); tgt[tgt == 0] = 1.0
            try:
                wn, *_ = np.linalg.lstsq(
                    np.vstack([M, np.sqrt(lam) * Mh]),
                    np.concatenate([-(S @ K).ravel(), np.sqrt(lam) * tgt]),
                    rcond=None)
            except np.linalg.LinAlgError:
                break
            if not np.all(np.isfinite(wn)) or np.abs(wn).max() > 1e8:
                break                       # diverged; this restart is dead
            w = wn
            A = assemble(w, cells, S)
            try:
                U, sv, Vt = np.linalg.svd(A)
            except np.linalg.LinAlgError:
                break
            K = Vt[-r:].T
        if sv is None or not np.all(np.isfinite(w)):
            continue
        sc = np.abs(A).max()
        if not np.isfinite(sc) or sc == 0:
            continue
        cand = (sv[-r] / sc, np.abs(w[e0:e0 + ne]).min() / sc, w.copy())
        if best is None or cand[0] < best[0]:
            best = cand
    if best is None:
        return (np.inf, 0.0, np.zeros(P))
    return best


def is_prime(m):
    return m > 1 and all(m % d for d in range(2, int(m ** 0.5) + 1))


if __name__ == "__main__":
    k = int(sys.argv[1]); ns = [int(x) for x in sys.argv[2:]]
    r = 2 * k + 2
    thr = (k + 1) * (2 * k + 3) / 3
    print(f"k = {k}   nullity target {r}   threshold n >= {thr:.1f}")
    print("    n  prime  3n - C(r+1,2)  sign   r-th sv/scale  min|inner|  nullity")
    for n in ns:
        for sign in (+1, -1):
            obj, me, w = solve(n, k, sign=sign)
            cells, S = cells_fixed(n, k, sign)
            A = assemble(w, cells, S)
            sv = np.linalg.svd(A, compute_uv=False)
            nul = int(np.sum(sv < 1e-9 * sv.max()))
            np.save(f"/Volumes/2TB/scifair/results/zero_forcing/"
                    f"wg_{n}_{k}_{'p' if sign > 0 else 'm'}.npy", w)
            print(f" {n:4d}   {'yes' if is_prime(n) else ' no'}"
                  f"{int(3*n-(k+1)*(2*k+3)):13d}  {sign:+d}   {obj:14.3e}"
                  f"{me:12.4f}{nul:9d}   {'CEILING' if nul >= r else ''}")
