"""
The general lower bound:  Z(B^n) >= D(B), for any cyclic cover.

Combining two facts already established:
  * M(G) <= Z(G) for every matrix whose off-diagonal support is exactly E(G);
  * on a cyclic cover B^n, prescribing D/2 interior grid values and solving for
    the weights produces a matrix of nullity exactly D, where D is the degree
    span of det M(zeta) -- a quantity read off the base graph's voltages alone.

Therefore Z(B^n) >= D(B).  This is a statement about ALL cyclic covers, with
P(n,k) (base: two loops of voltages 1 and k, one edge of voltage 0, D = 2k+2)
as the special case.

This script checks it against exhaustively computed zero forcing numbers on
small covers, which is the only way to know the bound is not vacuous.
"""
import sys
from itertools import combinations

import numpy as np

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from cyclic_covers import derived_graph


def zero_forcing_number(nbrs, N, cap=None):
    """Exact Z by exhaustive search over subsets, with bitmask closure."""
    full = (1 << N) - 1
    masks = [0] * N
    for u in range(N):
        for v in nbrs[u]:
            masks[u] |= (1 << v)

    def closure(S):
        cur = S
        changed = True
        while changed:
            changed = False
            rem = cur
            while rem:
                u = (rem & -rem).bit_length() - 1
                rem &= rem - 1
                w = masks[u] & ~cur
                if w and (w & (w - 1)) == 0:
                    cur |= w
                    changed = True
        return cur

    lim = cap if cap else N
    for size in range(1, lim + 1):
        for comb in combinations(range(N), size):
            S = 0
            for c in comb:
                S |= (1 << c)
            if closure(S) == full:
                return size
    return None


def cover_nbrs(be, nV, n):
    edges, N = derived_graph(be, nV, n)
    nbrs = {u: set() for u in range(N)}
    for (p, q) in edges:
        if p != q:
            nbrs[p].add(q); nbrs[q].add(p)
    return nbrs, N


if __name__ == "__main__":
    cases = [
        ("P(n,2) base", [(0, 0, 1), (1, 1, 2), (0, 1, 0)], 2, 6, [7, 8, 9]),
        ("theta 0,1,3", [(0, 1, 0), (0, 1, 1), (0, 1, 3)], 2, 6, [7, 8, 9, 10]),
        ("theta 0,1,2", [(0, 1, 0), (0, 1, 1), (0, 1, 2)], 2, 4, [7, 8, 9, 10]),
    ]
    print(f"{'cover':>14} {'n':>3} {'|V|':>4} {'D (from voltages)':>18} "
          f"{'Z (exhaustive)':>15} {'Z >= D ?':>9}")
    bad = 0
    for (nm, be, nV, D, ns) in cases:
        for n in ns:
            nbrs, N = cover_nbrs(be, nV, n)
            if any(len(v) != 3 for v in nbrs.values()):
                print(f"{nm:>14} {n:>3} {N:>4} {'not cubic (voltage clash)':>34}")
                continue
            Z = zero_forcing_number(nbrs, N, cap=min(N, D + 3))
            ok = (Z is not None and Z >= D)
            bad += (not ok)
            print(f"{nm:>14} {n:>3} {N:>4} {D:>18} {str(Z):>15} "
                  f"{str(ok):>9}", flush=True)
    print(f"\nZ(B^n) >= D(B) on every cover tested: "
          f"{'HOLDS' if bad == 0 else f'{bad} VIOLATIONS'}")
