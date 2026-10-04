"""
Does the period-d construction work for MANY n, or only a lucky few?

A list of scattered values is much weaker than a general statement.  The rank
law predicts the construction should work whenever

    d >= ceil(k/2)          (the symbol is reachable), and
    m = n/d >= 2k+4         (Gamma_m holds k+1 distinct interior values),

with enough slack in the choice of root set to avoid the degenerate locus.
This sweeps n for a fixed k and reports, for each, whether SOME root set gives
a realisable certificate -- stopping at the first success per n, since one is
all a lower bound needs.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import itertools
import sys

import numpy as np

sys.path.insert(0, f"{_REPO}/verification")
from prescribe_symbol import solve_for, grid_interior
from verify_period_d_cert import verify

k = int(sys.argv[1])
d = int(sys.argv[2])
ns = [int(v) for v in sys.argv[3].split(",")]
nsets = int(sys.argv[4]) if len(sys.argv) > 4 else 6
tries = int(sys.argv[5]) if len(sys.argv) > 5 else 12

print(f"k={k}, d={d} (rank law needs d >= {(k+1)//2}), target nullity {2*k+2}")
print(f"{'n':>5} {'m':>5} {'interior':>9} {'root sets':>10} {'tried':>6} "
      f"{'result':>14} {'min|req|':>9} {'gap':>10}")
hits = []
rng = np.random.default_rng(0)
for n in ns:
    if n % d or 2 * k >= n:
        continue
    m = n // d
    G = grid_interior(m)
    if len(G) < k + 1:
        print(f"{n:>5} {m:>5} {len(G):>9} {'-':>10} {'-':>6} "
              f"{'grid too small':>14}")
        continue
    combos = list(itertools.combinations(range(len(G)), k + 1))
    rng.shuffle(combos)
    found = None
    tried = 0
    for combo in combos[:nsets]:
        tried += 1
        roots = [G[i][1] for i in combo]
        w, err, _ = solve_for(n, k, d, roots, tries=tries, push=3.0)
        if err > 1e-9:
            continue
        ok, r, gap, minoff = verify(w, n, k, d, verbose=False)
        if ok:
            found = (combo, minoff, gap, w)
            break
    if found:
        combo, minoff, gap, w = found
        ls = tuple(G[i][0] for i in combo)
        hits.append((n, ls))
        print(f"{n:>5} {m:>5} {len(G):>9} {len(combos):>10} {tried:>6} "
              f"{'CERTIFICATE':>14} {minoff:>9.4f} {gap:>10.2e}", flush=True)
        np.save(f"{_REPO}/results/zero_forcing/"
                f"cert_k{k}_d{d}_n{n}.npy", w)
    else:
        print(f"{n:>5} {m:>5} {len(G):>9} {len(combos):>10} {tried:>6} "
              f"{'none found':>14}", flush=True)

print(f"\nk={k}: certificates at n = {[h[0] for h in hits]}")
print(f"  => Z(P(n,{k})) = {2*k+2} for each of those n")
