"""A2, second half: is the nullity-(n+1) witness real, and can it be certified?

verification/k4_max_nullity.py reports that on the K4 gap family the search
reaches nullity n+1 at n=4 (sigma_{n+1}/sigma_max about 7e-9) while failing at
n+2 (about 6e-4, nowhere near zero). If that is right it improves
thm:k4rankone's lower bound from n to n+1, and since Z = n+2 it pins
Z - M <= 1.

It must not be written down on the strength of 7e-9. This project has twice
been misled by exactly that: a strict gap at P(10,2) that did not exist, and a
false negative recorded as evidence for a conjecture later refuted. A converged
optimum and a rank deficiency are different claims.

So this module does three things, in increasing strength:

  1. Re-find the witness and KEEP IT, with the full singular spectrum, so the
     gap between sigma_{n+1} and sigma_n is visible rather than asserted.
  2. Read its structure: which principal blocks have dropped rank, and whether
     the extra dimension beyond the rank-one construction comes from the
     triangle fibres or the fibre over vertex 2.
  3. Try to make it exact -- snap the weights to nearby rationals and test the
     rank over Q. If that succeeds the bound is certified; if it fails, the
     finding is reported as NUMERICAL and nothing goes in the paper but a
     labelled open item.

Run: python3 verification/k4_nplus1.py
"""

import os
import sys
from fractions import Fraction as F

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sympy as sp

from certify_general import assemble
from verification.cover_maxnull import cover_cells
from verification.cubic_gap_family import K4_BASE

from scipy.optimize import least_squares

TRIANGLE = (0, 1, 3)
CROSS = 2


def search_witness(n, r, tries=400, seed=5, sign_sweep=20, tmax=2.5):
    """Same instrument as cover_maxnull.max_nullity, but it returns the matrix."""
    be, nV = K4_BASE
    N = nV * n
    cells, nd = cover_cells(be, nV, n)
    ne = len(cells) - nd
    rng = np.random.default_rng(seed)
    best = (np.inf, None, None)
    for st in range(sign_sweep):
        signs = np.ones(ne) if st == 0 else rng.choice([-1.0, 1.0], ne)
        for _ in range(max(1, tries // sign_sweep)):
            z0 = np.concatenate([rng.standard_normal(nd),
                                 rng.standard_normal(ne) * 0.5])

            def res(z):
                w = np.concatenate([z[:nd], signs * np.exp(z[nd:])])
                A = assemble(w, cells, N)
                sv = np.linalg.svd(A, compute_uv=False)
                return sv[-r:] / (sv.max() + 1e-300)

            lo = np.concatenate([np.full(nd, -np.inf), np.full(ne, -tmax)])
            hi = np.concatenate([np.full(nd, np.inf), np.full(ne, tmax)])
            z0 = np.clip(z0, lo + 1e-9, hi - 1e-9)
            out = least_squares(res, z0, method="trf", bounds=(lo, hi),
                                max_nfev=3000, xtol=1e-15, ftol=1e-15,
                                gtol=1e-15)
            w = np.concatenate([out.x[:nd], signs * np.exp(out.x[nd:])])
            A = assemble(w, cells, N)
            sv = np.linalg.svd(A, compute_uv=False)
            score = sv[-r] / sv.max()
            if score < best[0]:
                best = (score, w.copy(), A.copy())
    return best[0], best[1], best[2], cells, nd


def describe(n, A, r):
    N = A.shape[0]
    sv = np.linalg.svd(A, compute_uv=False)
    print(f"    singular spectrum (smallest {r + 3}):")
    print("      " + "  ".join(f"{s/sv.max():.3e}" for s in sv[-(r + 3):]))
    gap = sv[-r] / sv[-r - 1]
    print(f"    sigma_{r}/sigma_{r+1} = {gap:.3e}   (a rank drop needs this tiny)")

    # triangle fibres and the fibre over vertex 2
    tri = [v * n + i for i in range(n) for v in TRIANGLE]
    cross = [CROSS * n + i for i in range(n)]
    for name, idx in (("triangle fibres A[S]", tri), ("fibre over 2 A[S^c]", cross)):
        B = A[np.ix_(idx, idx)]
        s = np.linalg.svd(B, compute_uv=False)
        rk = int((s > s.max() * 1e-9).sum())
        print(f"    {name}: {len(idx)}x{len(idx)}, numerical rank {rk}")
    # per-triangle rank: the rank-one construction has every triangle rank 1
    ranks = []
    for i in range(n):
        idx = [v * n + i for v in TRIANGLE]
        B = A[np.ix_(idx, idx)]
        s = np.linalg.svd(B, compute_uv=False)
        ranks.append(int((s > s.max() * 1e-9).sum()))
    print(f"    rank of each triangle block: {ranks}"
          f"   (rank-one construction gives {[1]*n})")
    return gap


def try_rational(A, r, denoms=(1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64)):
    """Snap to rationals and test the rank exactly. Returns (ok, denom, nullity)."""
    N = A.shape[0]
    scale = np.abs(A[A != 0]).max()
    for q in denoms:
        M = sp.zeros(N, N)
        ok_support = True
        for i in range(N):
            for j in range(N):
                if A[i, j] == 0:
                    continue
                val = sp.Rational(int(round(A[i, j] / scale * q)), q)
                if val == 0 and i != j:
                    ok_support = False
                M[i, j] = val
        if not ok_support:
            continue
        if M.T != M:
            M = (M + M.T) / 2
        nul = N - M.rank()
        if nul >= r:
            return True, q, nul
    return False, None, None


def main():
    print("A2 (second half): the nullity-(n+1) witness on the K4 family")
    print("=" * 66)
    rows = []
    for n in (4, 5, 6):
        r = n + 1
        print(f"\n=== n={n}  target nullity r={r}  (rank-one gives {n}, Z={n+2}) ===",
              flush=True)
        score, w, A, cells, nd = search_witness(n, r)
        print(f"    best sigma_{r}/sigma_max = {score:.3e}")
        if score > 1e-7:
            print("    NOT ACHIEVED -- reported as a search failure, nothing more")
            rows.append((n, r, score, None, None, None))
            continue
        gap = describe(n, A, r)
        ok, q, nul = try_rational(A, r)
        if ok:
            print(f"    EXACT: snapped to denominator {q}, exact nullity over Q = {nul}")
        else:
            print("    exact snapping FAILED -- the witness stays NUMERICAL")
        rows.append((n, r, score, gap, q, nul))

    print("\n" + "=" * 66)
    print(f"{'n':>3} {'r':>3} {'sigma_r':>11} {'gap':>11} {'exact?':>8} {'nullity':>8}")
    for n, r, s, g, q, nul in rows:
        print(f"{n:>3} {r:>3} {s:>11.3e} "
              f"{'-' if g is None else format(g, '.3e'):>11} "
              f"{'no' if q is None else 'q=' + str(q):>8} "
              f"{'-' if nul is None else nul:>8}")
    print("\nAnything not marked exact is a numerical finding and must be")
    print("labelled as such in the paper, not claimed.")
    return rows


if __name__ == '__main__':
    main()
