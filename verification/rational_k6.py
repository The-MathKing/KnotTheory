"""
Hunt for a genuinely RATIONAL period-d certificate at k = 6.

The obstruction (verification/rational_obstruction.py) says rational weights
force a Galois-closed root set.  At (k,d,n) = (6,3,60) and (6,3,72) every
Galois-closed set degenerates, so no rational certificate exists there.

(6,4,64) is different.  There m = 16 and Gamma_16 has exactly 7 interior
values for the 7 required, so the root set is forced to be ALL of them -- and a
set that is everything is automatically Galois-stable.  The obstruction is
therefore silent, and a realisable certificate is already known to exist at
those parameters.  So this is the one place to look.

The target symbol is prod over all interior sigma of (s - sigma) = the
Chebyshev-like s^7 - 6 s^5 + 10 s^3 - 4 s, with INTEGER coefficients, so the
variety {w : det M_l(w) = 0, l = 1..7} is defined over Q (Galois permutes the
equations among themselves).  With 5d = 20 weights and 7 equations the solution
set is 13-dimensional, so rational points should be plentiful if any exist.

Strategy: fix 13 weights at chosen rationals, solve the remaining 7 numerically
at high precision, and test the result for rationality by integer-relation
detection.  Recognition is heuristic; the exact check that follows is not.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import sys
import numpy as np
import mpmath as mp
from scipy.optimize import least_squares

sys.path.insert(0, f"{_REPO}/verification")
from period_d_blocks import blocks
from prescribe_symbol import grid_interior
from verify_period_d_cert import verify

k, d, n = 6, 4, 64
m = n // d
G = grid_interior(m)
LS = [l for (l, s) in G]
print(f"k={k} d={d} n={n} m={m}: interior grid indices {LS} "
      f"({len(LS)} values, need {k+1})")
assert len(LS) == k + 1


def resid(w, free_idx, fixed):
    full = fixed.copy()
    full[free_idx] = w
    out = []
    for l in LS:
        M = blocks(full, n, k, d)[l]
        out.append(float(np.real(np.linalg.det(M))))
    return np.array(out)


rng = np.random.default_rng(0)
best = None
print(f"\n{'trial':>6} {'residual':>12} {'min|req|/scale':>15} {'nullity':>8}")
for trial in range(40):
    # fix 13 weights at simple rationals, leave 7 free
    fixed = np.zeros(5 * d)
    vals = np.array([1, -1, 2, -2, 1, 3, -3, 1, 2, -1, 1, -2, 3, 1, -1, 2,
                     1, -1, 1, 2], dtype=float)
    perm = rng.permutation(5 * d)
    fixed[:] = vals[rng.permutation(len(vals))]
    free_idx = np.sort(perm[:k + 1])
    # keep required-nonzero entries away from zero in the fixed part
    for j in range(3 * d):
        if j not in free_idx and abs(fixed[j]) < 0.5:
            fixed[j] = 1.0
    x0 = rng.standard_normal(k + 1) + np.sign(rng.standard_normal(k + 1))
    sol = least_squares(resid, x0, args=(free_idx, fixed), method="lm",
                        xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
    r = np.abs(sol.fun).max()
    if r > 1e-10:
        continue
    full = fixed.copy(); full[free_idx] = sol.x
    ok, nul, gap, minoff = verify(full, n, k, d, verbose=False)
    print(f"{trial:>6} {r:>12.2e} {minoff:>15.5f} {nul:>8}"
          f"  {'REALISABLE' if ok else ''}", flush=True)
    if ok:
        best = (full, free_idx, fixed)
        break

if best is None:
    print("\nno realisable solution from these rational fixings")
else:
    full, free_idx, fixed = best
    print(f"\nfree coordinates {list(free_idx)} solved to:")
    for j, v in zip(free_idx, full[free_idx]):
        print(f"   w[{j:>2}] = {v:+.15f}")
    np.save(f"{_REPO}/results/zero_forcing/rat_k6_d4_n64.npy", full)
    print("\nAre the free coordinates rational?  (integer-relation test)")
    mp.mp.dps = 40
    for j, v in zip(free_idx, full[free_idx]):
        rel = mp.pslq([mp.mpf(float(v)), mp.mpf(1)], maxcoeff=10**8,
                      maxsteps=10000)
        print(f"   w[{j:>2}]: " + (f"= {-rel[1]}/{rel[0]}" if rel and rel[0]
                                   else "no low-height rational relation"))
