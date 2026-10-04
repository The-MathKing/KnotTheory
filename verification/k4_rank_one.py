"""The K4 gap family is the counterexample to the regular-base ceiling.

The K4 base of cubic_gap_family.py has voltages

        0-1 : 0     0-2 : 1     0-3 : 0
        1-2 : 2     1-3 : 0     2-3 : 1

The three edges of voltage 0 are 0-1, 0-3, 1-3: a TRIANGLE.  So every fibre
index i carries a triangle {(0,i),(1,i),(3,i)}, and the only edges leaving a
triangle go to the fibre over vertex 2.  Put a rank-one block u u^T (u entrywise
nonzero) on each triangle: the off-diagonal entries u_a u_b are nonzero as the
pattern requires and the diagonal is free.  Then the rows at the 3n triangle
vertices have rank <= n + n (block-diagonal rank-one part, plus a block with n
columns) and the rows over vertex 2 number n, so rank A <= 3n and
null A >= n.  This refutes conj:cubicgap (M = 6) and the regular-base ceiling
of rem:mindeg, and it shows thm:cover needs det M(zeta) != 0: the rank-one
matrix is equivariant and its symbol vanishes identically.

The general form is prop:lowrank:  M(G) >= |V| - mr(G[S]) - 2|V minus S| for every
S, of which the independent-set bound prop:indobs is the case mr(G[S]) = 0.

Second check: the top coefficient of det M(zeta), as a polynomial in the edge
weights and diagonals, is a MONOMIAL in edge weights on every base where the
ceiling is proved, and CONTAINS A DIAGONAL on every base where it fails
(conj:leading).
"""
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from verification.cover_ceiling_attack import BASES, degree_span
from verification.cubic_gap_family import K4_BASE

TRIANGLE = (0, 1, 3)          # the zero-voltage edges of K4_BASE form this triangle
CROSS_VERTEX = 2

#: known status of the non-equivariant ceiling on each base in BASES, plus K_{2,3}
PROVED = ["P(n,2) two-loop", "P(n,3) two-loop", "theta (0,1,2)", "theta (0,1,3)",
          "4-edge theta", "triangle (0,1,2)", "C4 cycle base"]
REFUTED = {
    "star-4 + loop": BASES["star-4 + loop"],
    "K4 assorted": BASES["K4 assorted"],
    "K_{2,3}": ([(0, 2, 0), (0, 3, 1), (0, 4, 2), (1, 2, 1), (1, 3, 0), (1, 4, 1)], 5),
}


def cover_edges(n):
    be, nV = K4_BASE
    E = set()
    for (x, y, v) in be:
        for i in range(n):
            p, q = x * n + i, y * n + ((i + v) % n)
            E.add((min(p, q), max(p, q)))
    return E


def rank_one_matrix(n, u=(1, 2, 3), cross_w=1, d2=1):
    """Exact sympy matrix: rank-one triangle blocks, nonzero cross weights."""
    be, nV = K4_BASE
    N = nV * n
    A = sp.zeros(N, N)
    uu = dict(zip(TRIANGLE, [sp.Integer(t) for t in u]))
    for i in range(n):
        for a in TRIANGLE:
            for b in TRIANGLE:
                A[a * n + i, b * n + i] = uu[a] * uu[b]
    for (x, y, v) in be:
        if x in TRIANGLE and y in TRIANGLE:
            continue
        for i in range(n):
            p, q = x * n + i, y * n + ((i + v) % n)
            A[p, q] += sp.Integer(cross_w)
            A[q, p] += sp.Integer(cross_w)
    for i in range(n):
        A[CROSS_VERTEX * n + i, CROSS_VERTEX * n + i] = sp.Integer(d2)
    return A, N


def pattern_ok(A, n):
    """Off-diagonal support is exactly E(B^n)."""
    N = A.shape[0]
    E = cover_edges(n)
    return all(((p, q) in E) == (A[p, q] != 0)
               for p in range(N) for q in range(p + 1, N))


def check_rank_one(ns=range(4, 11)):
    """(n, |V|, pattern ok, exact nullity over Q, D).  Claim: nullity >= n > D."""
    be, nV = K4_BASE
    D = degree_span(be, nV)
    rows = []
    for n in ns:
        A, N = rank_one_matrix(n)
        rows.append((n, N, pattern_ok(A, n), N - A.rank(), D))
    return rows


def check_symbol_vanishes():
    """det M(zeta) == 0 identically for the equivariant rank-one matrix."""
    z = sp.symbols("z")
    be, nV = K4_BASE
    u = dict(zip(TRIANGLE, sp.symbols("u0 u1 u3")))
    w = {e: sp.Symbol("w%d%d" % (x, y)) for e, (x, y, v) in enumerate(be)}
    d2 = sp.Symbol("d2")
    M = sp.zeros(nV, nV)
    for a in TRIANGLE:
        for b in TRIANGLE:
            M[a, b] = u[a] * u[b]
    for e, (x, y, v) in enumerate(be):
        if x in TRIANGLE and y in TRIANGLE:
            continue
        M[x, y] += w[e] * z ** v
        M[y, x] += w[e] * z ** (-v)
    M[CROSS_VERTEX, CROSS_VERTEX] = d2
    return sp.simplify(M.det()) == 0


def top_coefficient(be, nV):
    """Top coefficient of det M(zeta) in symbolic edge weights and diagonals.
    Returns (factored coefficient, contains a diagonal?, number of terms)."""
    z = sp.symbols("z")
    ws = sp.symbols("w0:%d" % len(be))
    ds = sp.symbols("d0:%d" % nV)
    M = sp.zeros(nV, nV)
    for e, (x, y, v) in enumerate(be):
        if x == y:
            M[x, x] += ws[e] * (z ** v + z ** (-v))
        else:
            M[x, y] += ws[e] * z ** v
            M[y, x] += ws[e] * z ** (-v)
    for i in range(nV):
        M[i, i] += ds[i]
    num, _ = sp.fraction(sp.together(sp.expand(M.det())))
    P = sp.Poly(sp.expand(num), z)
    top = sp.factor(P.coeff_monomial(z ** P.degree()))
    has_diag = any(top.has(d) for d in ds)
    return top, has_diag, len(sp.Add.make_args(sp.expand(top)))


def check_leading_coefficient():
    """Monomial in edge weights on every proved base; a diagonal on every
    refuted one.  Returns (proved_rows, refuted_rows)."""
    proved = []
    for name in PROVED:
        be, nV = BASES[name]
        top, has_diag, nterms = top_coefficient(be, nV)
        proved.append((name, str(top), (not has_diag) and nterms == 1))
    refuted = []
    for name, (be, nV) in REFUTED.items():
        top, has_diag, nterms = top_coefficient(be, nV)
        refuted.append((name, str(top), has_diag))
    return proved, refuted


if __name__ == "__main__":
    print("K4 base: zero-voltage edges form the triangle %s" % (TRIANGLE,))
    for n, N, ok, nul, D in check_rank_one():
        print("   n=%-3d |V|=%-4d pattern=%s  exact null A = %-3d  vs D=%d   %s"
              % (n, N, ok, nul, D, "EXCEEDS D" if nul > D else ""))
    print("equivariant rank-one matrix: det M(zeta) == 0 identically?",
          check_symbol_vanishes())
    proved, refuted = check_leading_coefficient()
    print("top coefficient of det M(zeta):")
    for name, top, mono in proved:
        print("   PROVED   %-18s %-10s %s" % (name, "monomial" if mono else "NOT", top))
    for name, top, has_d in refuted:
        print("   REFUTED  %-18s %-10s %s" % (name, "diagonal" if has_d else "NO DIAG", top))
