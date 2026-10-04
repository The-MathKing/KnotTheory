"""
When does the P(n,k) elimination generalise to an arbitrary cyclic cover?

For P(n,k) the ceiling null A <= 2k+2 holds for EVERY matrix carrying the
pattern, because the nonzero spoke weights let us solve the equation at u_i for
y_i and reduce to one scalar recurrence.  What made that work was not the
spokes as such but an ORDERING of the base vertices along which each equation
releases exactly one new unknown.

Concretely: pick a spanning structure and gauge the voltages so it carries
voltage 0 (voltage assignments are equivalent under switching
v -> v + t_a - t_b, so this is free).  Process the base vertices in an order
a_1, ..., a_p.  The kernel equation at (a_j, i) involves a_j's own fibre
coordinate with the DIAGONAL as coefficient -- and the diagonal may be zero, so
it cannot be solved for.  It can, however, be solved for a NEIGHBOUR of a_j.
So the elimination runs iff each a_{j+1} is adjacent to a_j: that is, iff the
base graph has a HAMILTONIAN PATH.

The consequence to test: for such a base graph, the map
    ker A  ->  (x_{a_1, i})_{i in a window of length D}
should be injective, where D is the degree span of det M(zeta).  Injectivity
gives null A <= D for every matrix carrying the pattern, not just equivariant
ones.  This checks that injectivity directly, on matrices tuned to have
genuinely nonzero nullity.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import itertools
import sys

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, f"{_REPO}/verification")
from cyclic_covers import build_full, blocks


def has_hamiltonian_path(be, nV):
    adj = {x: set() for x in range(nV)}
    for (x, y, v) in be:
        if x != y:
            adj[x].add(y); adj[y].add(x)
    for perm in itertools.permutations(range(nV)):
        if all(perm[i + 1] in adj[perm[i]] for i in range(nV - 1)):
            return True, perm
    return False, None


def degree_span(be, nV, rng):
    th = np.linspace(0.11, 2 * np.pi - 0.13, 90)
    w = rng.standard_normal(len(be)) + 1.6
    dg = rng.standard_normal(nV)
    vals = []
    for t in th:
        z = np.exp(1j * t)
        M = np.zeros((nV, nV), dtype=complex)
        for e, (x, y, v) in enumerate(be):
            M[x, y] += w[e] * z ** v
            M[y, x] += w[e] * np.conj(z) ** v
        for x in range(nV):
            M[x, x] += dg[x]
        vals.append(np.linalg.det(M))
    D = sum(abs(v) for (_, _, v) in be) + nV
    V = np.stack([np.exp(1j * j * th) for j in range(-D, D + 1)], axis=1)
    c, *_ = np.linalg.lstsq(V, np.array(vals), rcond=None)
    nz = np.flatnonzero(np.abs(c) > 1e-8 * np.abs(c).max())
    return int(nz.max() - nz.min())


def tuned_matrix(be, nV, n, rng, m0):
    """Weights tuned so block m0 is singular, giving nonzero nullity."""
    w = rng.standard_normal(len(be)) + 1.6
    dg = rng.standard_normal(nV)

    def f(t):
        d = dg.copy(); d[0] = t
        return float(np.real(np.linalg.det(blocks(be, nV, n, w, d)[m0])))

    xs = np.linspace(-60, 60, 3000); vs = np.array([f(x) for x in xs])
    s = np.flatnonzero(np.sign(vs[:-1]) * np.sign(vs[1:]) < 0)
    if len(s) == 0:
        return None
    d = dg.copy(); d[0] = brentq(f, xs[s[0]], xs[s[0] + 1], xtol=1e-14)
    return build_full(be, nV, n, w, d)


def window_injective(A, n, root, D, tol=1e-8):
    """Is ker A -> (x_{root,i}) on a window of length D injective?"""
    N = A.shape[0]
    sv = np.linalg.svd(A, compute_uv=False)
    r = int(np.sum(sv < tol * sv[0]))
    if r == 0:
        return None, 0
    K = np.linalg.svd(A)[2][-r:].T            # N x r kernel basis
    best = True
    for start in range(n):
        idx = [root * n + ((start + t) % n) for t in range(D)]
        blk = K[idx, :]
        if np.linalg.matrix_rank(blk, tol=1e-7) < r:
            best = False
    return best, r


if __name__ == "__main__":
    cases = [
        ("P(n,2) base",     [(0, 0, 1), (1, 1, 2), (0, 1, 0)], 2, 14),
        ("P(n,3) base",     [(0, 0, 1), (1, 1, 3), (0, 1, 0)], 2, 15),
        ("theta 0,1,3",     [(0, 1, 0), (0, 1, 1), (0, 1, 3)], 2, 13),
        ("path 3-vertex",   [(0, 0, 1), (1, 1, 2), (2, 2, 3),
                             (0, 1, 0), (1, 2, 0)], 3, 12),
        ("star 4-vertex",   [(0, 1, 0), (0, 2, 0), (0, 3, 0),
                             (1, 1, 1), (2, 2, 2), (3, 3, 3)], 4, 11),
        ("cycle 4-vertex",  [(0, 1, 0), (1, 2, 1), (2, 3, 0), (3, 0, 2),
                             (0, 0, 1)], 4, 11),
    ]
    rng = np.random.default_rng(0)
    print(f"{'base graph':>16} {'Ham path':>9} {'nV':>3} {'n':>4} {'D':>4} "
          f"{'nullity':>8} {'window injective?':>18}")
    for (nm, be, nV, n) in cases:
        hp, order = has_hamiltonian_path(be, nV)
        D = degree_span(be, nV, rng)
        results = []
        for m0 in (1, 2, 3):
            A = tuned_matrix(be, nV, n, rng, m0)
            if A is None:
                continue
            inj, r = window_injective(A, n, 0, D)
            if inj is not None:
                results.append((inj, r))
        if not results:
            print(f"{nm:>16} {str(hp):>9} {nV:>3} {n:>4} {D:>4} "
                  f"{'-':>8} {'no singular case':>18}")
            continue
        allinj = all(i for (i, _) in results)
        rs = {r for (_, r) in results}
        print(f"{nm:>16} {str(hp):>9} {nV:>3} {n:>4} {D:>4} "
              f"{str(sorted(rs)):>8} {str(allinj):>18}", flush=True)
