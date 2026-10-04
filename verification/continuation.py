"""
Continuation: push a vanishing weight off zero while holding the symbol exact.

Solving G(w) = G* by unconstrained least squares reliably lands on a point
where ONE required-nonzero weight has collapsed to zero -- and at such a point
the Jacobian of G drops rank (6 instead of the generic 7 for k=6, d=3).  That
is a singular point of the map, not a generic fibre point, which is why random
restarts keep returning to it: it is an attractor.

The fix is not more restarts but continuation.  Augment the system with an
explicit target for the vanishing coordinate,

    G(w)[1:] = G*[1:]            (k+1 equations)
    w[j0]    = tau               (1 equation)

and solve for increasing tau, warm-starting each solve from the previous
solution.  If the fibre genuinely leaves the degenerate locus, tau can be
driven up to an O(1) value with the symbol still exact and every other
required weight nonzero -- which is a certificate.  If tau stalls, the
degeneracy is real and the target G* is unreachable with the correct pattern.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import sys

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, f"{_REPO}/verification")
from period_d_rank import G_coeffs
from prescribe_symbol import grid_interior, target_coeffs, true_nullity, solve_for
from period_d_blocks import blocks


def labels(d):
    return ([f"b{r}" for r in range(d)] + [f"c{r}" for r in range(d)]
            + [f"e{r}" for r in range(d)] + [f"aO{r}" for r in range(d)]
            + [f"aI{r}" for r in range(d)])


def continue_off_zero(w0, n, k, d, tgt, j0, taus, verbose=True):
    w = w0.copy()
    sgn = 1.0 if w0[j0] >= 0 else -1.0
    hist = []
    for tau in taus:
        def res(v):
            g = G_coeffs(v, n, k, d)
            if g is None:
                return np.full(k + 2, 1e3)
            return np.concatenate([g[1:] - tgt, [v[j0] - sgn * tau]])
        sol = least_squares(res, w, method="trf", xtol=1e-15, ftol=1e-15,
                            gtol=1e-15, max_nfev=800)
        g = G_coeffs(sol.x, n, k, d)
        err = np.inf if g is None else np.abs(g[1:] - tgt).max()
        if err > 1e-9:
            if verbose:
                print(f"   tau={tau:<6.3f} symbol lost (err {err:.1e}) -- stop")
            break
        w = sol.x
        scale = np.abs(w).max()
        minnz = np.abs(w[:3 * d]).min() / scale
        hist.append((tau, err, minnz, w.copy()))
        if verbose:
            print(f"   tau={tau:<6.3f} symbol err {err:.2e}   "
                  f"min|required wt|/scale = {minnz:.5f}")
    return hist


if __name__ == "__main__":
    k, d, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    which = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    m = n // d
    G = grid_interior(m)
    lab = labels(d)
    import itertools
    combos = list(itertools.combinations(range(len(G)), k + 1))
    combo = combos[which % len(combos)]
    idx = [G[i][0] for i in combo]
    roots = [G[i][1] for i in combo]
    tgt = target_coeffs(roots)[1:]
    print(f"k={k} d={d} n={n} m={m}; root set l={tuple(idx)}")
    w0, err, _ = solve_for(n, k, d, roots, tries=30, push=0.0)
    scale = np.abs(w0).max()
    zeros = [j for j in range(3 * d) if abs(w0[j]) / scale < 1e-3]
    print(f"  base solution: symbol err {err:.2e}; "
          f"vanishing weights {[lab[j] for j in zeros]}")
    if not zeros:
        r, gap = true_nullity(w0, n, k, d)
        print(f"  ALREADY REALISABLE: nullity {r}, gap {gap:.2e}")
        raise SystemExit
    j0 = zeros[0]
    print(f"  continuing {lab[j0]} away from zero:")
    taus = [0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 2.0]
    hist = continue_off_zero(w0, n, k, d, tgt, j0, taus)
    if hist:
        tau, err, minnz, w = hist[-1]
        r, gap = true_nullity(w, n, k, d)
        ok = (r == 2 * k + 2) and minnz > 1e-2 and gap > 1e-3
        print(f"\n  best reached: tau={tau}, min|required wt|/scale={minnz:.5f}")
        print(f"  nullity {r} (target {2*k+2}), gap {gap:.2e}")
        print(f"  {'*** REALISABLE CERTIFICATE ***' if ok else 'not realisable'}")
        if ok:
            for L, v in zip(lab, w):
                print(f"     {L:>4} = {v:+.10f}")
