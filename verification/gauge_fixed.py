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

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
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


if __name__ == "__main__" and sys.argv[1:2] != ["verify"]:
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
            np.save(f"{_REPO}/results/zero_forcing/"
                    f"wg_{n}_{k}_{'p' if sign > 0 else 'm'}.npy", w)
            print(f" {n:4d}   {'yes' if is_prime(n) else ' no'}"
                  f"{int(3*n-(k+1)*(2*k+3)):13d}  {sign:+d}   {obj:14.3e}"
                  f"{me:12.4f}{nul:9d}   {'CEILING' if nul >= r else ''}")


def verify_slice(k=3, ns=(17, 18, 19, 20, 21, 22), seed=5):
    """Check Lemma (a complete slice): every symmetric matrix on the pattern is
    gauge-equivalent to one with all spokes +1 and all |outer| = 1, except that
    for even n one outer weight is left free.  Positive diagonal conjugation
    cannot change a spoke's sign (d_i d_{n+i} > 0), so the sign diagonal is
    needed as well; and the cyclic system u_i + u_{i+1} = -log|b_i| is invertible
    for odd n but has corank 1 for even n, which is why one weight survives."""
    import numpy as _np
    sys.path.insert(0, f"{_REPO}/verification")
    from certify_general import pattern_cells, assemble
    rng = _np.random.default_rng(seed)
    rows = []
    for n in ns:
        w = rng.standard_normal(5 * n)
        w[2*n:5*n] += 1.5 * _np.sign(w[2*n:5*n])
        b, c = w[2*n:3*n], w[3*n:4*n]
        idx = list(range(n)) if n % 2 else list(range(1, n))
        M = _np.zeros((len(idx), n)); rhs = []
        for r_, i in enumerate(idx):
            M[r_, i] = 1; M[r_, (i + 1) % n] = 1
            rhs.append(-_np.log(abs(b[i])))
        u, *_ = _np.linalg.lstsq(M, _np.array(rhs), rcond=None)
        du = _np.exp(u); dv = 1.0 / (du * _np.abs(c))
        D = _np.concatenate([du, dv])
        A = assemble(w, pattern_cells(n, k), 2 * n)
        A2 = _np.diag(D) @ A @ _np.diag(D)
        s = _np.ones(2 * n)
        for i in range(n):
            if A2[i, n + i] < 0:
                s[n + i] = -1
        A3 = _np.diag(s) @ A2 @ _np.diag(s)
        sp = _np.array([A3[i, n + i] for i in range(n)])
        ob = _np.array([A3[i, (i + 1) % n] for i in range(n)])
        rows.append((n, bool(_np.allclose(sp, 1.0)),
                     float(_np.abs(_np.abs(ob[idx]) - 1).max()),
                     float(ob[0]),
                     _np.linalg.matrix_rank(A) == _np.linalg.matrix_rank(A3)))
    return rows


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "verify":
    print("Lemma (a complete slice): spokes -> +1, |outer| -> 1 (one free when "
          "n is even)")
    print("   n  parity  spokes=+1   max||b_i|-1|   b_0        nullity kept")
    for n, spok, dev, b0, rk in verify_slice():
        print(f" {n:3d}  {'odd ' if n % 2 else 'even'}    {str(spok):5s}"
              f"      {dev:.2e}      {b0:+.4f}    {rk}")
