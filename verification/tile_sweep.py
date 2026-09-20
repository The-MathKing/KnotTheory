"""Solve for identity tiles of every length in a range, then test the theorem.

If a tile of length l has transfer product I, and tiles exist for every length
in [L, 2L), then every n >= L is a sum of available lengths, so T = I for every
such n and Z(P(n,k)) = M(P(n,k)) = 2k+2 for all n >= L, with no congruence
condition.  This script does the solving and then the end-to-end test: build the
actual matrix on P(n,k) from a tiling and check its nullity.
"""
import glob as glob_mod
import os
import sys

import numpy as np

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from tiles import (solve_tile, tile_product, tile_sequence, dock_weights,
                   build_matrix, monodromy_range, extend_tile)


def tile_dict(w, l, k):
    m = k + 1
    nint = l - 2 * m
    D = dock_weights(k)
    t = {}
    for idx, key in enumerate("bcead"):
        t[key] = np.concatenate([D[key], w[idx*nint:(idx+1)*nint], D[key]])
    return t


def main():
    k = int(sys.argv[1])
    lo, hi = int(sys.argv[2]), int(sys.argv[3])
    r = 2 * k + 2
    print(f"k = {k}   nullity target {r}   tile lengths {lo}..{hi}")
    print(f"  a tile of length l has 5(l - {2*(k+1)}) free weights against "
          f"{r*r} equations")
    print("    l  unknowns   max|T - I|   min|edge|/scale   verdict")
    sols = {}
    # reuse tiles already on disk: a sweep restarted over a wider range should
    # not re-solve lengths that are done
    for f in glob_mod.glob(f"/Volumes/2TB/scifair/results/zero_forcing/"
                           f"tile_*_{k}.npy"):
        ll = int(os.path.basename(f).split("_")[1])
        if lo <= ll <= hi:
            sols[ll] = np.load(f)
    if sols:
        print(f"  reusing {len(sols)} tiles already solved: {sorted(sols)}")
    for l in range(lo, hi + 1):
        if l in sols:
            continue
        nint = l - 2 * (k + 1)
        # A tile needs at least as many free weights as the condition T = I
        # imposes.  The reachable set of monodromies is smaller than the full
        # matrix space, so the sharp count is unknown; require at least r*r - 13
        # (the deficiency measured at k=3) and report the margin.
        if 5 * nint < r * r - 13:
            print(f" {l:5d}{5*nint:10d}   only {5*nint} unknowns for "
                  f"{r*r} equations; skipped")
            continue
        warm = None
        if sols:
            lp = max(sols)
            warm = extend_tile(sols[lp], lp, l, k)
        b = solve_tile(l, k, tries=20, seed=l, nfev=1200, w0=warm)
        if b is None:
            print(f" {l:5d}{5*nint:10d}   nothing found")
            continue
        err, negme, w = b
        ok = err < 1e-10 and -negme > 1e-3
        if ok:
            sols[l] = w
            np.save(f"/Volumes/2TB/scifair/results/zero_forcing/"
                    f"tile_{l}_{k}.npy", w)
        print(f" {l:5d}{5*nint:10d}{err:13.2e}{-negme:18.4f}   "
              f"{'IDENTITY TILE' if ok else 'no'}")
    print(f"\nidentity tiles found for l = {sorted(sols)}")
    if not sols:
        return
    L = min(sols)
    have = sorted(sols)
    print(f"\nend-to-end test: build P(n,k) from tilings and check the nullity")
    print("     n   tiling            nullity   next sv/scale   min|edge|/scale")
    import itertools
    tested = 0
    for n in range(L, 4 * L):
        combo = None
        for rr in (1, 2, 3):
            for c in itertools.combinations_with_replacement(have, rr):
                if sum(c) == n:
                    combo = c; break
            if combo: break
        if combo is None:
            continue
        W = tile_sequence([tile_dict(sols[l], l, k) for l in combo], k)
        A = build_matrix(n, k, W)
        sv = np.linalg.svd(A, compute_uv=False)
        sc = np.abs(A).max()
        nul = int(np.sum(sv < 1e-9 * sc))
        edges = min(np.abs(W["b"]).min(), np.abs(W["c"]).min(),
                    np.abs(W["e"]).min())
        print(f" {n:5d}   {str(combo):17s}{nul:8d}{sv[-r-1]/sc:16.4f}"
              f"{edges/sc:18.4f}   {'OK' if nul == r else 'MISMATCH'}")
        tested += 1
        if tested > 40:
            break


if __name__ == "__main__":
    main()
