"""
Separate the two questions for a Galois-closed (rational) target symbol.

Running the solve with a realisability barrier conflates them: least_squares
trades the symbol residual against the barrier and lands on a compromise where
the symbol error sits at 1e-4 and every weight is pinned exactly at the barrier
value.  That says nothing about whether the target is reachable.

So: solve with NO barrier first.
  (1) does the symbol solve converge (error ~1e-14)?  If not, the rational
      target is simply not in the image and the root set is dead.
  (2) if it does converge, are the required weights nonzero?  Only then is
      realisability the live question, and only then is a barrier meaningful.
"""
import sys
import numpy as np

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from galois_closed_sets import galois_closed_sets, interior_orbits
from prescribe_symbol import solve_for, grid_interior
from verify_period_d_cert import verify

k, d, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
tries = int(sys.argv[4]) if len(sys.argv) > 4 else 30
m = n // d
sets, _ = galois_closed_sets(m, k + 1)
G0 = grid_interior(m)
sigma0 = [l for (l, s) in G0 if abs(s) < 1e-12]      # the index with sigma = 0
print(f"k={k} d={d} n={n} m={m}: {len(sets)} Galois-closed root sets")
print(f"sigma = 0 sits at l = {sigma0 if sigma0 else 'not in the grid'}\n")
print(f"{'orders':>20} {'has sig=0':>10} {'symbol err':>12} "
      f"{'min|req|/scale':>15} {'nullity':>8}  verdict")
for (orders, ls) in sets:
    roots = [s for (l, s) in G0 if l in ls]
    w, err, _ = solve_for(n, k, d, roots, tries=tries, push=0.0)
    scale = np.abs(w).max()
    minnz = np.abs(w[:3 * d]).min() / scale
    if err < 1e-9:
        ok, r, gap, minoff = verify(w, n, k, d, verbose=False)
        verdict = ("REALISABLE CERTIFICATE" if ok
                   else f"symbol hit, weight collapses (gap {gap:.1e})")
    else:
        r, verdict = -1, "symbol NOT reachable"
    print(f"{str(orders):>20} {str(bool(set(ls) & set(sigma0))):>10} "
          f"{err:>12.2e} {minnz:>15.5f} {r:>8}  {verdict}", flush=True)
    if err < 1e-9 and minnz > 1e-2:
        np.save(f"/Volumes/2TB/scifair/results/zero_forcing/"
                f"galois_cert_k{k}_d{d}_n{n}_{'_'.join(map(str,orders))}.npy", w)
