"""A2: pin down M(B^n) on the K4 gap family for n = 4, 5, 6.

Theorem thm:k4rankone gives M(B^n) >= n by the rank-one triangle construction,
and Z(B^n) = n + 2 by CP-SAT with optimality proved, so

        n  <=  M(B^n)  <=  n + 2

and the paper records "whether M(B^n) is n, n+1 or n+2 we have not determined".
This module tries to determine it for the three smallest members.

Method. Search for a matrix of nullity r over the FULL pattern (not the
equivariant subclass -- that is the point, since the equivariant maximum is
pinned at 6 and the whole question is whether the unrestricted maximum is
larger). We use cover_maxnull.max_nullity, which parametrises every edge weight
as s*exp(t) so the degenerate stratum is not in the parameter space, bounds the
spread so the optimiser cannot fake rank deficiency by inflating one weight,
and accepts a nullity only on a spectral GAP rather than an absolute cutoff.
That instrument exists because four earlier searches on this exact question
failed their controls.

Direction of the search matters. We test r = n + 2 first and walk DOWN. A
success at r is conclusive for a lower bound; a failure is not conclusive for
an upper bound -- a failed search measures effort spent, not impossibility,
which is the error this project has walked into before. So the output is
reported as: largest r ACHIEVED (a certified lower bound once the witness is
checked exactly), and the r values where the search FAILED, labelled as search
failures and nothing more.

Run: python3 verification/k4_max_nullity.py
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from verification.cover_maxnull import cover_cells, max_nullity
from verification.cubic_gap_family import K4_BASE


def assemble(w, cells, N):
    A = np.zeros((N, N))
    for wi, (_kind, pos) in zip(w, cells):
        for (p, q) in pos:
            A[p, q] += wi
    return A


def run(ns=(4, 5, 6), tries=240, sign_sweep=16, seed=11):
    be, nV = K4_BASE
    rows = []
    for n in ns:
        N = nV * n
        Z = n + 2
        print(f"\n=== n={n}  |V|={N}  Z={Z}  rank-one bound M>={n} ===",
              flush=True)
        achieved, failed = None, []
        for r in range(n + 2, n - 1, -1):
            ok, best = max_nullity(be, nV, n, r, tries=tries, seed=seed,
                                   sign_sweep=sign_sweep)
            tag = "ACHIEVED" if ok else "search failed"
            print(f"  r={r:2d}: {tag:<14s} best sigma_r/sigma_max = {best:.3e}",
                  flush=True)
            if ok:
                achieved = r
                break
            failed.append((r, best))
        rows.append(dict(n=n, N=N, Z=Z, lower_rank_one=n,
                         achieved=achieved, failed=failed))
    return rows


def main():
    print("A2: M(B^n) on the K4 gap family, n = 4, 5, 6")
    print("=" * 64)
    rows = run()

    print("\n" + "=" * 64)
    print(f"{'n':>3} {'|V|':>4} {'Z':>3} {'M>=(rank-1)':>12} "
          f"{'largest r found':>16} {'conclusion':>22}")
    for row in rows:
        a = row['achieved']
        if a is None:
            concl = "no improvement on n"
        elif a == row['Z']:
            concl = f"M = Z = {a} exactly"
        else:
            concl = f"M >= {a}, <= {row['Z']}"
        print(f"{row['n']:>3} {row['N']:>4} {row['Z']:>3} "
              f"{row['lower_rank_one']:>12} {str(a):>16} {concl:>22}")

    print("\nA search failure at r is NOT an upper bound. Any r where the")
    print("search failed is reported as a failed search, not as impossibility.")
    return rows


if __name__ == '__main__':
    main()
