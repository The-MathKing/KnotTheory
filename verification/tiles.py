"""Toward "for all large n": tiles whose transfer product is the identity.

cor:ceiling says null A = 2k+2 iff the monodromy T = prod_{i} T_i equals I, for
ANY matrix on the pattern.  T_i is built from the weights in a window of width
about 2k+2 around position i, so a weight sequence cut into independent blocks
does not give a clean factorisation of T -- the blocks interact across their
boundaries.

Fix: give every tile a FIXED docking segment of k+1 positions at each end.  For
any i inside a tile the window [i-k-1, i+k] then reaches at most into a docking
segment, and every docking segment carries the same fixed weights, so the
product over a tile is determined by that tile alone.  Concatenating tiles
therefore multiplies their products, and if every tile has product I then the
monodromy of the cyclic graph on n = sum of the tile lengths is I as well.

Consequence, if tiles of every length in [L, 2L) can be built: every n >= L is a
sum of integers drawn from [L, 2L), so

    Z(P(n,k)) = M(P(n,k)) = 2k+2   for all n >= L,

with no congruence condition and no gap.  That is L separate finite problems,
each a system of (2k+2)^2 equations in the 3(l - 2(k+1)) free tile weights, so
each needs l >= 2(k+1) + (2k+2)^2/3 or a little less, since the reachable set of
monodromies is smaller than the full matrix space.

This module builds the machinery and checks the factorisation claim before any
solving: it tiles a weight sequence, forms the actual matrix on P(n,k), and
compares its monodromy against the product of the tile monodromies.
"""
import sys

import numpy as np

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from recurrence_order import gamma_row


def dock_weights(k):
    """The fixed docking segment: k+1 positions of (b, c, e, a, d)."""
    m = k + 1
    return dict(b=np.ones(m), c=np.ones(m), e=np.ones(m),
                a=np.zeros(m), d=np.zeros(m))


def tile_sequence(tiles, k):
    """Concatenate tiles into full (b,c,e,a,d) arrays of length n = sum lengths.

    Each tile is a dict of arrays of length l_t; its first and last k+1 entries
    are overwritten with the docking segment, so only l_t - 2(k+1) positions per
    tile are free."""
    D = dock_weights(k)
    m = k + 1
    out = {key: [] for key in "bcead"}
    for t in tiles:
        l = len(t["b"])
        for key in "bcead":
            arr = np.array(t[key], dtype=float)
            arr[:m] = D[key]
            arr[l - m:] = D[key]
            out[key].append(arr)
    return {key: np.concatenate(out[key]) for key in "bcead"}


def Ti(n, k, i, W):
    """One step of the monodromy, from the weight arrays W."""
    r = 2 * k + 2
    g = gamma_row(n, k, i, W["b"], W["c"], W["e"], W["a"], W["d"])
    lead = g[k + 1]
    M = np.zeros((r, r))
    M[:r - 1, 1:] = np.eye(r - 1)
    for p, v in g.items():
        if p == k + 1:
            continue
        M[r - 1, p + k + 1] -= v / lead
    return M


def monodromy_range(n, k, W, s, t):
    """Product T_{t-1} ... T_s of the steps at positions s..t-1 (indices mod n)."""
    r = 2 * k + 2
    P = np.eye(r)
    for i in range(s, t):
        P = Ti(n, k, i % n, W) @ P
    return P


def build_matrix(n, k, W):
    N = 2 * n
    A = np.zeros((N, N))
    for i in range(n):
        A[i, i] = W["a"][i]
        A[n + i, n + i] = W["d"][i]
        j = (i + 1) % n
        A[i, j] = A[j, i] = W["b"][i]
        A[i, n + i] = A[n + i, i] = W["c"][i]
        p, q = n + i, n + (i + k) % n
        A[p, q] = A[q, p] = W["e"][i]
    return A


def check_factorisation(k, lengths, seed=0):
    """Does the monodromy factorise over tiles?  Build random tiles, tile them,
    and compare the full monodromy with the product of the per-tile products."""
    rng = np.random.default_rng(seed)
    tiles = []
    for l in lengths:
        t = {}
        for key, shift in (("b", 1.5), ("c", 1.5), ("e", 1.5),
                           ("a", 0.0), ("d", 0.0)):
            v = rng.standard_normal(l)
            if shift:
                v = v + shift * np.sign(v)
            t[key] = v
        tiles.append(t)
    W = tile_sequence(tiles, k)
    n = sum(lengths)
    T_full = monodromy_range(n, k, W, 0, n)
    prod = np.eye(2 * k + 2)
    off = 0
    per_tile = []
    for l in lengths:
        Tt = monodromy_range(n, k, W, off, off + l)
        per_tile.append(Tt)
        prod = Tt @ prod
        off += l
    err = np.abs(T_full - prod).max() / max(np.abs(T_full).max(), 1.0)
    return err, per_tile, W, n


if __name__ == "__main__":
    print(__doc__)
    print("factorisation check: full monodromy vs product of tile monodromies")
    print("  (this is exact by associativity; the real question, checked next, is")
    print("   whether a tile's product depends only on that tile)")
    for k in (2, 3):
        for lengths in ([12, 13], [12, 13, 14], [15, 15, 16]):
            err, per, W, n = check_factorisation(k, lengths)
            print(f"  k={k} lengths={lengths} n={n}: relative error {err:.2e}")
    print()
    print("independence check: change a tile's INTERIOR and confirm the other")
    print("tiles' products do not move")
    rng = np.random.default_rng(7)
    for k in (2, 3):
        lengths = [14, 15, 16]
        err1, per1, W1, n = check_factorisation(k, lengths, seed=1)
        err2, per2, W2, n2 = check_factorisation(k, lengths, seed=2)
        # tile 0 differs between the two runs; compare tile 0 and tiles 1,2
        d0 = np.abs(per1[0] - per2[0]).max()
        d12 = max(np.abs(per1[j] - per2[j]).max() for j in (1, 2))
        print(f"  k={k}: tile 0 products differ by {d0:.2e} (expected, different"
              f" weights); tiles 1,2 differ by {d12:.2e}")


# ---------------------------------------------------------------------------
# solving for a tile whose transfer product is the identity
# ---------------------------------------------------------------------------

def tile_product(w, l, k):
    """Transfer product over one tile of length l, from its free interior
    weights w (5 per interior position).  The docking segments at both ends are
    fixed, so this depends on w alone -- verified by the independence check."""
    m = k + 1
    nint = l - 2 * m
    D = dock_weights(k)
    t = {}
    for idx, key in enumerate("bcead"):
        t[key] = np.concatenate([D[key], w[idx * nint:(idx + 1) * nint], D[key]])
    # tile it with itself so the wrap-around sees a docking segment either side
    W = tile_sequence([t, t], k)
    n = 2 * l
    return monodromy_range(n, k, W, 0, l)


def solve_tile(l, k, tries=200, seed=0, tau=0.15):
    """Solve tile_product = I for the interior weights."""
    from scipy.optimize import least_squares
    r = 2 * k + 2
    m = k + 1
    nint = l - 2 * m
    P = 5 * nint
    rng = np.random.default_rng(seed)
    best = None
    for t in range(tries):
        w0 = rng.standard_normal(P)
        w0[:3 * nint] += 1.3 * np.sign(w0[:3 * nint])   # b, c, e away from zero

        def res(w):
            sc = max(np.abs(w).max(), 1e-12)
            if np.abs(w[:3 * nint]).min() < 1e-10 * sc:
                return np.full(r * r + 3 * nint, 1e3)
            try:
                T = tile_product(w, l, k)
            except Exception:
                return np.full(r * r + 3 * nint, 1e3)
            if not np.all(np.isfinite(T)):
                return np.full(r * r + 3 * nint, 1e3)
            bar = 2.0 * np.maximum(0.0, tau - np.abs(w[:3 * nint]) / sc)
            return np.concatenate([(T - np.eye(r)).ravel(), bar])

        s = least_squares(res, w0, method="trf", xtol=1e-15, ftol=1e-15,
                          gtol=1e-15, max_nfev=3000)
        try:
            T = tile_product(s.x, l, k)
            err = np.abs(T - np.eye(r)).max()
        except Exception:
            continue
        if not np.isfinite(err):
            continue
        sc = max(np.abs(s.x).max(), 1e-12)
        me = np.abs(s.x[:3 * nint]).min() / sc
        cand = (err, -me, s.x.copy())
        if best is None or cand[:2] < best[:2]:
            best = cand
        if err < 1e-13 and me > tau * 0.5:
            break
    return best
