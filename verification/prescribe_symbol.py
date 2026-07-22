"""
Prescribe the symbol, then solve for the weights.

The rank law (verification/period_d_rank.py) says the map

    (5d period-d weights)  ->  (k+1 monic coefficients of G(sigma))

has rank min(2d+1, k+1), so for d >= ceil(k/2) it is a submersion.  That makes
a far better-posed problem available than minimising eigenvalues:

    choose k+1 interior grid values of Gamma_m, form the monic polynomial G*
    with exactly those roots, and SOLVE G(w) = G* for the weights.

This is k+1 equations in 5d unknowns with a full-rank Jacobian, so Newton
converges locally and the solution set is a manifold of dimension 5d-(k+1).
Minimising the r smallest eigenvalues instead gives the optimiser room to cheat
by collapsing an edge weight toward zero -- which is exactly what it did at
(n,k,d) = (48,6,3), returning 1.3e-5 with no spectral gap and the minimum
weight pinned against the barrier.

Realisability is still a separate hurdle: the solve may return weights with a
vanishing required entry, in which case that target G* is unreachable even
though it is in the image of the linearisation.
"""
import itertools
import sys

import numpy as np
from scipy.optimize import least_squares

WSYM = 1.0e4   # weight on the symbol residual relative to the barrier

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from period_d_rank import G_coeffs
from period_d_blocks import blocks


def grid_interior(m):
    """Interior values of Gamma_m, with their representative indices."""
    out = []
    for l in range(0, m // 2 + 1):
        s = 2 * np.cos(2 * np.pi * l / m)
        if abs(abs(s) - 2) > 1e-9:
            out.append((l, s))
    return out


def target_coeffs(roots):
    return np.poly(roots)            # monic, highest degree first


def solve_for(n, k, d, roots, tries=60, seed=0, tau=0.05, push=3.0):
    """Solve G(w) = G* for the weights.

    The solution set is a manifold of dimension 5d-(k+1) (eight-dimensional for
    k=6, d=3), so hitting the symbol is not enough: the solver must be steered
    toward a point of that manifold where every required-nonzero weight is
    actually nonzero.  Without the barrier it happily returns a point with all
    spokes zero -- which is a legitimate solution of G(w) = G*, because with
    c = 0 the matrix block-diagonalises and G factors as det(U) det(V), but it
    describes a DIFFERENT graph (the spokes are gone) and certifies nothing."""
    m = n // d
    tgt = target_coeffs(roots)[1:]            # drop the leading 1
    P = 5 * d
    rng = np.random.default_rng(seed)
    best = None
    for t in range(tries):
        w0 = rng.standard_normal(P)
        w0[:3 * d] += 1.1 * np.sign(w0[:3 * d])

        def res(w):
            g = G_coeffs(w, n, k, d)
            if g is None:
                return np.full(k + 1 + 3 * d, 1e3)
            scale = max(np.abs(w).max(), 1e-12)
            bar = push * np.maximum(0.0, tau - np.abs(w[:3 * d]) / scale)
            # The symbol residual must dominate the barrier, or least_squares
            # trades them off and converges to neither: with them comparable it
            # returned symbol error 1e-4 and every weight pinned exactly at tau.
            # Weighting the symbol heavily makes the barrier act only within
            # the (5d-k-1)-dimensional fibre, which is what it is for.
            return np.concatenate([WSYM * (g[1:] - tgt), bar])

        sol = least_squares(res, w0, method="trf", xtol=1e-15, ftol=1e-15,
                            gtol=1e-15, max_nfev=600)
        w = sol.x
        g = G_coeffs(w, n, k, d)
        err = np.inf if g is None else np.abs(g[1:] - tgt).max()
        minnz = np.abs(w[:3 * d]).min() / max(np.abs(w).max(), 1e-12)
        if best is None or (err, -minnz) < (best[1], -best[2]):
            best = (w.copy(), err, minnz)
    return best


def true_nullity(w, n, k, d, tol=1e-8):
    vals = np.concatenate([np.abs(np.linalg.eigvalsh(M))
                           for M in blocks(w, n, k, d)])
    scale = max(np.abs(w).max(), 1e-12)
    vals = np.sort(vals)
    r = int(np.sum(vals < tol * scale))
    gap = vals[r] / scale if r < len(vals) else np.inf
    return r, gap


if __name__ == "__main__":
    k, d, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    tries = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    nsets = int(sys.argv[5]) if len(sys.argv) > 5 else 25
    m = n // d
    G = grid_interior(m)
    print(f"k={k}, d={d}, n={n}, m={m}: {len(G)} interior grid values, "
          f"need {k+1}; rank law says rank = min({2*d+1},{k+1})")
    if len(G) < k + 1:
        print("  grid too small"); raise SystemExit
    rng = np.random.default_rng(0)
    combos = list(itertools.combinations(range(len(G)), k + 1))
    rng.shuffle(combos)
    print(f"  {len(combos)} possible root sets; trying {min(nsets,len(combos))}")
    print(f"{'root indices':>34} {'solve err':>11} {'min|wt|':>9} "
          f"{'nullity':>8} {'gap':>10}  verdict")
    found = 0
    for combo in combos[:nsets]:
        idx = [G[i][0] for i in combo]
        roots = [G[i][1] for i in combo]
        w, err, minnz = solve_for(n, k, d, roots, tries=tries)
        if err > 1e-9:
            continue
        r, gap = true_nullity(w, n, k, d)
        ok = (r == 2 * k + 2) and minnz > 1e-2 and gap > 1e-3
        print(f"{str(tuple(idx)):>34} {err:>11.2e} {minnz:>9.4f} {r:>8} "
              f"{gap:>10.2e}  {'CERTIFICATE' if ok else ''}", flush=True)
        if ok:
            found += 1
            print(f"     weights = {np.array2string(w, precision=6)}")
            if found >= 3:
                break
    if not found:
        print("  no realisable solution among the root sets tried")
