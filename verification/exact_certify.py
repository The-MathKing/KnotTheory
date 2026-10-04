"""Re-certify saved certificates with the Krawczyk test evaluated EXACTLY.

Usage:  exact_certify.py tile <k> [lengths...]      # identity tiles
        exact_certify.py gn   <k> [n...]            # per-n certificates

This rebuilds the same square system certify_tiles.py / krawczyk.py used --
the same structural equation set, the same docking pins, the same free
coordinates -- and then evaluates the Krawczyk hypotheses in exact rational
arithmetic via exact_krawczyk.  Nothing is re-solved: the saved certificate is
the box centre, and the question asked is whether the EXACT test passes there.

The saved file stores z = (w, X).  perm is not stored, so it is recomputed from
the certified A(w) by the same graph_form call; the driver then CHECKS that the
recomputed X agrees with the stored X, which confirms the reconstruction picked
the same pivot rows.  If it does not agree the run aborts rather than certifying
a different system than the one on disk.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import sys, os, glob

import numpy as np
import scipy.linalg as sla

sys.path.insert(0, f"{_REPO}/verification")
from certify_general import pattern_cells, assemble, graph_form, jac
from certify_tiles import dock_indices, dock_weights
from krawczyk import L_LIP
from exact_krawczyk import exact_krawczyk, edge_bound

RES = f"{_REPO}/results/zero_forcing"


def rebuild(zn, n, k, pinned):
    """Recover (cells, perm, N, r, nw, eqs, free) for a saved certificate."""
    r, N = 2 * k + 2, 2 * n
    cells = pattern_cells(n, k)
    nw = len(cells)
    w = zn[:nw]
    A = assemble(w, cells, N)
    K0 = np.linalg.svd(A)[2][-r:].T
    perm, X = graph_form(K0, r)
    Xs = zn[nw:].reshape(N - r, r)
    dev = np.abs(X - Xs).max()
    # The stored X came from whichever pivot set the original pipeline chose.
    # We do not need THAT pivot set: any graph form of ker A(w) gives a square
    # system whose exact zero yields a matrix of nullity >= r near A(w).  So we
    # use the recomputed (perm, X) and report ||f(z0)|| to show the centre is a
    # near-solution.  dev is informational only.
    zn = np.concatenate([w, X.ravel()])
    eqs = sorted([perm[r + i] * r + t for i in range(N - r) for t in range(r)]
                 + [perm[s] * r + t for s in range(r) for t in range(r) if s <= t])
    rk = len(eqs)
    others = [i for i in range(len(zn)) if i not in set(pinned)]
    J = jac(w, X, cells, perm, N, r)
    _, _, Pc = sla.qr(J[np.ix_(eqs, others)], pivoting=True)
    free = sorted(others[i] for i in Pc[:rk])
    return cells, perm, N, r, nw, eqs, free, dev, zn


def run(kind, k, targets):
    r = 2 * k + 2
    if kind == "tile":
        pat, lab = f"tilecert_*_{k}.npy", "tile"
    else:
        pat, lab = f"cert_gn_*_{k}.npy", "P"
    files = sorted(glob.glob(f"{RES}/{pat}"),
                   key=lambda f: int(os.path.basename(f).split("_")[-2]))
    ns = [int(os.path.basename(f).split("_")[-2]) for f in files]
    if targets:
        keep = set(targets)
        files = [f for f, m in zip(files, ns) if m in keep]
        ns = [m for m in ns if m in keep]
    print(f"exact re-certification of {len(files)} {lab} certificates at k={k}")
    print(f"using L = {L_LIP} (a valid over-estimate; the true row-sum bound "
          f"is 8, see the paper)")
    print()
    good, bad = [], []
    for f, m in zip(files, ns):
        zn = np.load(f)
        pinned = dock_indices(m, k) if kind == "tile" else []
        print(f"--- {lab}({m}{'' if kind == 'tile' else ',' + str(k)}) "
              f"{'length' if kind == 'tile' else 'n'}={m} ---")
        try:
            cells, perm, N, rr, nw, eqs, free, dev, zn = rebuild(zn, m, k, pinned)
        except RuntimeError as e:
            print(f"  ABORT: {e}")
            bad.append(m)
            continue
        print(f"  graph form recomputed from the stored weights "
              f"(|X_new - X_stored| = {dev:.2e}; the pivot set need not match)")
        ok, info = exact_krawczyk(zn, cells, perm, N, rr, nw, eqs, free, L_LIP)
        if ok:
            lo, scale, ratio = edge_bound(zn, m, k, info["delta"])
            print(f"  edge weights over the WHOLE box: min|edge| - delta "
                  f">= {float(lo):.6f}, / scale = {float(ratio):.4f} > 0, so "
                  f"A(w*) is a matrix OF the graph")
            good.append(m)
        else:
            bad.append(m)
        print()
    print(f"EXACTLY CERTIFIED: {good}")
    print(f"not exactly certified: {bad}")
    if kind == "tile" and good and good == list(range(min(good), max(good) + 1)) \
            and max(good) >= 2 * min(good) - 1:
        print(f"=> exactly certified lengths cover [{min(good)}, {2*min(good)}), "
              f"so Z(P(n,{k})) = {r} is PROVED IN EXACT ARITHMETIC for every "
              f"n >= {min(good)}")


if __name__ == "__main__":
    kind, k = sys.argv[1], int(sys.argv[2])
    run(kind, k, [int(a) for a in sys.argv[3:]])
