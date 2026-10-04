"""The general cover ceiling is FALSE, with explicit integer counterexamples.

The paper recorded as open:

    "Whether the corresponding elimination can be carried out over an arbitrary
     base graph -- and so whether the ceiling is a property of the cover rather
     than of equivariant matrices on it -- we leave open."

It is not.  The ceiling is a property of equivariant matrices, not of the cover.

THE MECHANISM.  A base vertex of degree 1 lifts to PENDANT vertices of the
cover.  Diagonal entries are free in S(G), so set the pendant diagonals to zero:
the row at a pendant p attached to u then reads w * x_u = 0 with w != 0, forcing
x_u = 0, and x_p itself is unconstrained by that row.  With TWO leaves on the
same base vertex, every vertex of the shared fibre is forced to zero and one
free parameter survives per fibre index, so the nullity grows like n while D is
a constant read off the voltages.

COUNTEREXAMPLE 1 -- star-with-a-loop, D = 2.
    base: 0-1, 0-2, 0-3 (voltages 0,1,2) and a loop of voltage 1 at vertex 1;
    degrees (3,3,1,1).
    All edge weights 1; diagonals 1 on fibre 0, 3 on fibre 1, ZERO on the two
    pendant fibres.  Then null A = n for every n, against D = 2.

The natural repair -- demand minimum degree 2, so the cover has no pendants --
also fails.

COUNTEREXAMPLE 2 -- K_{2,3}, D = 4, minimum degree 2.
    base: parts {0,1} and {2,3,4}, voltages as below; degrees (3,3,2,2,2).
    Zeroing the diagonals on the three degree-2 fibres gives null A = 6 at n = 5
    and 8 at n = 7, both connected, against D = 4.

WHAT SURVIVES.  Every REGULAR base tested holds, and every counterexample found
is irregular.  That is the refined conjecture, and it is not a retreat from
anything the paper needs: P(n,k) and the theta covers are cubic, so the
published results are untouched.  What dies is only the claim for an ARBITRARY
base, which is what was stated as open.

Everything here is exact: the ranks are computed over Z with sympy, not by an
optimiser.  That matters, because the same statement was first suggested by a
numerical search that had already produced one false counterexample today.
"""
import itertools
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from verification.cover_ceiling_attack import cover_connected, degree_span

STAR_LOOP = ([(0, 1, 0), (0, 2, 1), (0, 3, 2), (1, 1, 1)], 4)
K23 = ([(0, 2, 0), (0, 3, 1), (0, 4, 2), (1, 2, 1), (1, 3, 0), (1, 4, 1)], 5)


def base_degrees(base_edges, nV):
    d = [0] * nV
    for (x, y, v) in base_edges:
        if x == y:
            d[x] += 2
        else:
            d[x] += 1
            d[y] += 1
    return d


def build_exact(base_edges, nV, n, zero_fibres, weight=1):
    """Integer matrix on the cover: unit edge weights, chosen fibres given
    diagonal zero (legal -- the diagonal is free in S(G))."""
    N = nV * n
    A = sp.zeros(N, N)
    for (x, y, v) in base_edges:
        for i in range(n):
            p, q = x * n + i, y * n + ((i + v) % n)
            if p == q:
                continue
            A[p, q] += sp.Integer(weight)
            A[q, p] += sp.Integer(weight)
    for x in range(nV):
        for i in range(n):
            A[x * n + i, x * n + i] = (sp.Integer(0) if x in zero_fibres
                                       else sp.Integer(2 * x + 1))
    return A, N


def nullity_exact(base_edges, nV, n, zero_fibres, weight=1):
    A, N = build_exact(base_edges, nV, n, zero_fibres, weight)
    return N - A.rank()


def check_star_loop(ns=(5, 6, 7), weights=(1, 2, 3)):
    """null A = n against D = 2, for every n and every unit-ish weight."""
    be, nV = STAR_LOOP
    D = degree_span(be, nV)
    rows = []
    for n in ns:
        if not cover_connected(be, nV, n):
            continue
        for w in weights:
            rows.append((n, w, nullity_exact(be, nV, n, {2, 3}, w), D))
    return rows


def check_k23(ns=(5, 7)):
    """Minimum degree 2, connected, and still over the ceiling."""
    be, nV = K23
    D = degree_span(be, nV)
    rows = []
    for n in ns:
        if not cover_connected(be, nV, n):
            continue
        rows.append((n, nullity_exact(be, nV, n, {2, 3, 4}), D))
    return rows


REGULAR_BASES = {
    "C3 (2-reg)": ([(0, 1, 0), (1, 2, 1), (0, 2, 2)], 3),
    "theta (3-reg)": ([(0, 1, 0), (0, 1, 1), (0, 1, 2)], 2),
    "two-loop (3-reg)": ([(0, 0, 1), (1, 1, 2), (0, 1, 0)], 2),
    "K4 (3-reg)": ([(0, 1, 0), (0, 2, 1), (0, 3, 0),
                    (1, 2, 2), (1, 3, 0), (2, 3, 1)], 4),
    "4-theta (4-reg)": ([(0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 1, 3)], 2),
}


def check_regular_survive(ns=(5, 6), maxzero=3):
    """The zeroing attack, run against regular bases: it should never exceed D."""
    rows = []
    for name, (be, nV) in REGULAR_BASES.items():
        D = degree_span(be, nV)
        for n in ns:
            if nV * n > 30 or not cover_connected(be, nV, n):
                continue
            best = 0
            for zero in itertools.chain.from_iterable(
                    itertools.combinations(range(nV), r)
                    for r in range(0, min(nV, maxzero) + 1)):
                best = max(best, nullity_exact(be, nV, n, set(zero)))
            rows.append((name, n, best, D))
    return rows


if __name__ == "__main__":
    be, nV = STAR_LOOP
    print("COUNTEREXAMPLE 1: star-with-a-loop, degrees %s, D = %d"
          % (base_degrees(be, nV), degree_span(be, nV)))
    for n, w, nul, D in check_star_loop():
        print("   n=%d weight=%d: null A = %-3d  vs D = %d   %s"
              % (n, w, nul, D, "OVER" if nul > D else "ok"))
    be, nV = K23
    print("COUNTEREXAMPLE 2: K_{2,3}, degrees %s (min 2), D = %d"
          % (base_degrees(be, nV), degree_span(be, nV)))
    for n, nul, D in check_k23():
        print("   n=%d: null A = %-3d  vs D = %d   %s"
              % (n, nul, D, "OVER" if nul > D else "ok"))
    print("REGULAR bases, same attack:")
    for name, n, best, D in check_regular_survive():
        print("   %-18s n=%d: best null A = %-3d  vs D = %-3d  %s"
              % (name, n, best, D, "OVER" if best > D else "within"))
