"""Identity tiles for every length, from two conditions at one point.

Setting (sec:symplectic of the paper).  Fix k and a DOCK: constant weights
(a0, b0=1, c0, d0, e0) at k+1 positions at each end of a tile.  A tile of length
l has 5(l-2k-2) free interior weights w and a transfer product P_l(w) in
Sp(2k+2,R).  S_l = { P_l(w) : all b,c,e nonzero }.  Concatenation gives
S_l S_m <= S_{l+m}.  Identity tiles of every length in [L, 2L) give
Z(P(n,k)) = M(P(n,k)) = 2k+2 for all n >= L (thm:tiling).

Two conditions, both at the single point w0 = "interior equals the dock":

  (E) ELLIPTIC DOCK.  The constant-weight step matrix S0 is diagonalisable with
      every eigenvalue on the unit circle.  Equivalently the dock symbol
      F(s) = (a0+s)(d0+e0 t_k(s)) - c0^2,  t_k(s) = 2T_k(s/2), has k+1 distinct
      real roots in (-2,2).  Then {S0^m : m>=0} has compact closure T, a group,
      so S0^{-N} is in T for every N.

  (S) SUBMERSION AT THE DOCK.  For some l0 the differential of w -> P_{l0}(w) at
      w0 has rank dim Sp(2k+2) = (k+1)(2k+3).  Then S_{l0} contains an open
      neighbourhood of S0^{l0}, i.e. S0^{l0} u for all u in a ball B around I.

THEOREM.  (E) and (S) imply: there is L with I in S_N for every N >= L.
Proof.  For M tiles from the ball,  S0^{l0}u_1 ... S0^{l0}u_M = S0^{M l0} u'_1...u'_M
with u'_i = S0^{-(M-i)l0} u_i S0^{(M-i)l0} ranging over a ball B' (conjugation by
the compact set T is uniformly bounded).  B'^M covers the compact set T for M
large, so S0^{-M l0 - r} is a product of M elements of B' for every r, and
I = S0^{M l0}(u'_1...u'_M) S0^r  lies in  S_{M l0 + r}  whenever r = 0 or
r >= 2k+2 (a pure-dock tile of length r).  Taking l0 >= 2k+2, every N >= M l0 + 2k+2
is of this form.                                                            []

(E) is decided by Sturm's theorem on F; (S) is one rank computation at an
explicit point.  Neither involves a search.  This module checks both.
"""
import os as _os
import sys
import numpy as np

_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), ".."))
sys.path.insert(0, f"{_REPO}/verification")
from recurrence_order import gamma_row


def t_k(k, s):
    return 2 * np.cos(k * np.arccos(np.clip(s / 2, -1, 1))) if abs(s) <= 2 else 2 * np.cosh(k * np.arccosh(abs(s) / 2)) * (np.sign(s) ** k)


def dock_symbol_roots(k, dock):
    """Roots z of det block = 0 as a palindromic polynomial in z (degree 2k+2)."""
    a0, c0, d0, e0 = dock
    # (a0 + z + 1/z)(d0 + e0 (z^k + z^-k)) - c0^2 = 0, times z^{k+1}
    p = np.zeros(2 * k + 3)
    # (a0 z + z^2 + 1) * (d0 z^k + e0 z^{2k} + e0) - c0^2 z^{k+1}
    A = np.zeros(3); A[0] = 1; A[1] = a0; A[2] = 1
    B = np.zeros(2 * k + 1); B[0] = e0; B[k] = d0; B[2 * k] = e0
    p[:2 * k + 3] = np.convolve(A, B)
    p[k + 1] -= c0 ** 2
    return np.roots(p[::-1])


def is_elliptic(k, dock, tol=1e-9):
    r = dock_symbol_roots(k, dock)
    onU = np.all(np.abs(np.abs(r) - 1) < tol)
    distinct = len(set(np.round(r, 7))) == len(r)
    return bool(onU and distinct), r


def find_elliptic_dock(k, rng=None, tries=2000):
    """A dock with the explicit family a0=d0=0, e0=+-1, c0 small, else random."""
    for e0 in (1.0, -1.0):
        for c0 in (0.3, 0.5, 0.2, 0.7, 0.1):
            ok, _ = is_elliptic(k, (0.0, c0, 0.0, e0))
            if ok:
                return (0.0, c0, 0.0, e0)
    rng = rng or np.random.default_rng(0)
    for _ in range(tries):
        dock = (rng.uniform(-1, 1), rng.uniform(0.1, 1.5), rng.uniform(-1, 1), rng.choice([-1, 1]) * rng.uniform(0.5, 1.5))
        if is_elliptic(k, dock)[0]:
            return dock
    return None


def tile_product(w, l, k, dock):
    """Transfer product of a tile of length l with dock `dock` = (a0,c0,d0,e0),
    b0 = 1, and interior weights w (5 blocks: b, c, e, a, d)."""
    a0, c0, d0, e0 = dock
    m = k + 1
    nint = l - 2 * m
    D = dict(b=np.ones(m), c=np.full(m, c0), e=np.full(m, e0), a=np.full(m, a0), d=np.full(m, d0))
    t = {}
    for idx, key in enumerate("bcead"):
        t[key] = np.concatenate([D[key], w[idx * nint:(idx + 1) * nint], D[key]])
    # tile it with itself so the wrap-around sees a dock on either side
    W = {key: np.concatenate([t[key], t[key]]) for key in "bcead"}
    n = 2 * l
    r = 2 * k + 2
    P = np.eye(r)
    for i in range(l):
        g = gamma_row(n, k, i, W["b"], W["c"], W["e"], W["a"], W["d"])
        lead = g[k + 1]
        Ti = np.zeros((r, r)); Ti[:r - 1, 1:] = np.eye(r - 1)
        for p, v in g.items():
            if p != k + 1:
                Ti[r - 1, p + k + 1] -= v / lead
        P = Ti @ P
    return P


def dock_point(l, k, dock):
    a0, c0, d0, e0 = dock
    nint = l - 2 * (k + 1)
    return np.concatenate([np.ones(nint), np.full(nint, c0), np.full(nint, e0), np.full(nint, a0), np.full(nint, d0)])


def jacobian_rank(l, k, dock, h=1e-6, tol=1e-7):
    """Rank of d(P_l)/dw at the dock point, measured in the Lie algebra:
    columns  (P(w+h e_j) - P(w-h e_j)) / 2h * P(w)^{-1}."""
    w0 = dock_point(l, k, dock)
    P0 = tile_product(w0, l, k, dock)
    P0inv = np.linalg.inv(P0)
    cols = []
    for j in range(len(w0)):
        wp = w0.copy(); wp[j] += h
        wm = w0.copy(); wm[j] -= h
        dP = (tile_product(wp, l, k, dock) - tile_product(wm, l, k, dock)) / (2 * h)
        cols.append((dP @ P0inv).ravel())
    J = np.array(cols).T
    sv = np.linalg.svd(J, compute_uv=False)
    rank = int(np.sum(sv > tol * sv[0]))
    return rank, sv


def dim_sp(k):
    return (k + 1) * (2 * k + 3)


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    for k in range(2, kmax + 1):
        dock = find_elliptic_dock(k)
        if dock is None:
            print(f"k={k}: no elliptic dock found"); continue
        ok, roots = is_elliptic(k, dock)
        print(f"k={k}: elliptic dock a0,c0,d0,e0 = {tuple(round(x,3) for x in dock)}; dim Sp = {dim_sp(k)}")
        need = dim_sp(k)
        for l in range(2 * k + 2 + 2, 2 * k + 2 + 40, 2):
            rank, sv = jacobian_rank(l, k, dock)
            print(f"   l={l:3d}: params {5*(l-2*k-2):3d}, rank {rank:3d} / {need}", "  <-- SUBMERSION" if rank == need else "")
            if rank == need:
                break
