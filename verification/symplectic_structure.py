"""Tile products are symplectic: the structure behind a general existence proof.

The tiling theorem reduces "Z(P(n,k)) = 2k+2 for all large n" to the existence
of identity tiles of every length in [L,2L).  Existence is currently established
by computing the tiles, one k at a time.  A proof for all k needs to know what
the reachable set of tile products IS.

This module establishes that it lies in a symplectic group.  For a fixed docking
pattern there is a skew form B, unique up to scale, with

    P^T B P = B   for every tile product P with that docking,

and B is nondegenerate.  So the reachable set is contained in Sp(B), a connected
simple Lie group of dimension C(2k+3, 2) -- which is exactly the dimension of
the reachable set measured independently from the rank of dP/dw.  The mechanism
is the standard symplectic structure of self-adjoint difference systems: the
recurrence comes from a symmetric matrix, so the transfer matrices carry a
Wronskian-type form along, and a tile whose two ends carry the same docking
returns that form to itself.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import sys

import numpy as np

sys.path.insert(0, f"{_REPO}/verification")
from tiles import tile_product


def common_invariant_skew(mats, r, tol=1e-8):
    """Dimension of {skew B : P^T B P = B for all P}, and a representative."""
    idx = [(a, b) for a in range(r) for b in range(a + 1, r)]
    blocks = []
    for T in mats:
        cols = []
        for (a, b) in idx:
            E = np.zeros((r, r)); E[a, b] = 1; E[b, a] = -1
            cols.append((T.T @ E @ T - E)[np.triu_indices(r, 1)])
        blocks.append(np.array(cols).T)
    A = np.vstack(blocks)
    U, sv, Vt = np.linalg.svd(A)
    dim = int(np.sum(sv < tol * max(sv.max(), 1e-300)))
    v = Vt[-1]
    B = np.zeros((r, r))
    for c, (a, b) in zip(v, idx):
        B[a, b] = c; B[b, a] = -c
    return dim, B / max(np.abs(B).max(), 1e-300)


def reachable_dim(l, k, seed=0, h=1e-6):
    """Rank of d(tile product)/d(weights): the dimension of the reachable set."""
    r = 2 * k + 2
    nint = l - 2 * (k + 1)
    P = 5 * nint
    rng = np.random.default_rng(seed)
    w = rng.standard_normal(P); w[:3 * nint] += 1.4 * np.sign(w[:3 * nint])
    T0 = tile_product(w, l, k).ravel()
    J = np.zeros((r * r, P))
    for j in range(P):
        wp = w.copy(); wp[j] += h
        J[:, j] = (tile_product(wp, l, k).ravel() - T0) / h
    sv = np.linalg.svd(J, compute_uv=False)
    return int(np.sum(sv > 1e-7 * sv.max()))


def main():
    print(__doc__)
    print("  k   l    r   invariant   det B      |P^T B P - B|   reachable   "
          "dim Sp(r)")
    print("               skew dim                                 dim")
    for k, l in [(2, 14), (2, 18), (3, 22), (3, 30), (4, 31), (4, 40),
                 (5, 54), (6, 60)]:
        r = 2 * k + 2
        nint = l - 2 * (k + 1)
        rng = np.random.default_rng(11)
        mats = []
        for _ in range(14):
            w = rng.standard_normal(5 * nint)
            w[:3 * nint] += 1.4 * np.sign(w[:3 * nint])
            T = tile_product(w, l, k)
            if np.all(np.isfinite(T)):
                mats.append(T)
        dim, B = common_invariant_skew(mats, r)
        err = max(np.abs(T.T @ B @ T - B).max() for T in mats)
        det = np.linalg.det(B)
        rk = reachable_dim(l, k, seed=5)
        print(f" {k:3d}{l:5d}{r:5d}{dim:10d}   {det:+9.2e}   {err:.2e}"
              f"{rk:11d}{r*(r+1)//2:11d}"
              + ("" if (dim == 1 and abs(det) > 1e-12 and rk == r*(r+1)//2)
                 else "   <-- CHECK"))
    print()
    print("A single invariant form, nondegenerate, and a reachable set of full")
    print("dimension in Sp(r): the reachable set is an open subsemigroup of a")
    print("connected simple Lie group.")


if __name__ == "__main__":
    main()
