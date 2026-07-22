"""
Largest nullity actually attainable in S(P(n,k)) with FULLY GENERAL weights.

For each (n,k) this walks r downward from the structural ceiling 2k+2
(verification/recurrence_order.py) and reports the largest r for which the
bilinear search of verification/monodromy_certificates.py finds an
admissible certificate: one whose r-th smallest |eigenvalue| is at machine
level relative to the matrix scale, whose (r+1)-st is not, and all of whose
required-nonzero weights are a non-negligible fraction of that scale.

The number reported is a LOWER bound on M(P(n,k)) certified numerically,
and the failure at r+1 is evidence -- not proof -- that M(P(n,k)) = r.
Since M(G) <= Z(G) always, a gap between this number and Z(P(n,k)) is a
gap between the maximum nullity and the zero forcing number, i.e. a
statement that the matrix-certificate route cannot reach Z at all.
"""
import sys
import numpy as np
from monodromy_certificates import search


def max_nullity(n, k, tries=25, seed=0, rmin=3):
    out = {}
    for r in range(2 * k + 2, rmin - 1, -1):
        best, _, _ = search(n, k, r=r, tries=tries, seed=seed, verbose=False)
        out[r] = best is not None
        print(f"  P({n},{k})  r={r:2d}: "
              f"{'ADMISSIBLE CERTIFICATE' if best is not None else 'none found'}"
              + (f"   (gap {best[1]:.1e}, min req.wt {best[2]:.3f})"
                 if best is not None else ""), flush=True)
        if best is not None:
            return r, out
    return None, out


if __name__ == "__main__":
    cases = []
    for arg in sys.argv[1:]:
        n, k = arg.split(",")
        cases.append((int(n), int(k)))
    if not cases:
        cases = [(12, 2), (14, 2), (13, 3), (15, 3), (17, 3), (20, 3),
                 (18, 4), (20, 4), (24, 4), (23, 5), (28, 6)]
    print(f"{'graph':>10}  {'ceiling 2k+2':>12}  {'max nullity found':>18}")
    rows = []
    for (n, k) in cases:
        r, _ = max_nullity(n, k)
        rows.append((n, k, 2 * k + 2, r))
        print(f"{'P(%d,%d)'%(n,k):>10}  {2*k+2:>12}  {str(r):>18}", flush=True)
    print("\nsummary")
    print(f"{'graph':>10} {'2k+2':>6} {'max nullity':>12}")
    for (n, k, c, r) in rows:
        print(f"{'P(%d,%d)'%(n,k):>10} {c:>6} {str(r):>12}")
