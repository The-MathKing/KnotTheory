"""An explicit family of cubic covers on which Z grows and the symbol does not.

Context.  The minimum rank literature asks for sufficient conditions giving
M(G) < Z(G), and for a graph parameter Y explaining the gap (Fallat-Hogben,
"Variants on the minimum rank problem: a survey II").  Every well-documented
strict example is tree-like -- the Barioli-Fallat tree and a 16-vertex relative.
No regular example is standard, and the published cubic results reach only
Z = 3 and Z = 4 (Akbari-Vatandoost-Golkhandy Pour).

The family.  Take the K_4 base with voltages

        0-1 : 0     0-2 : 1     0-3 : 0
        1-2 : 2     1-3 : 0     2-3 : 1

and its cyclic covers.  Every cover is cubic, connected and simple, on 4n
vertices.  Two facts, both computed rather than assumed:

  * The degree span of det M(zeta) is D = 6, INDEPENDENT of n.
  * Z of the cover is n + 2, verified by CP-SAT with optimality PROVED for
    n = 4,...,8 (Z = 6,7,8,9,10).

and one exact certificate:

  * all six edge weights 2, diagonals (4,4,5,4) gives an INTEGER matrix on the
    cover whose nullity is exactly 6, at n = 7 and n = 14.

Why those weights.  det M(zeta) is palindromic, so in x = zeta + 1/zeta it is a
cubic; the minimal polynomial of 2cos(2pi/7) is also a cubic, x^3+x^2-2x-1.
Matching them forces all four coefficients of zeta^3 det M equal, which happens
exactly when the three diagonals d0 = d1 = d3 =: t agree and
d2 = (3t+4)/((t-1)(t+2)).  Taking t = 2 gives d2 = 5/2, and scaling the matrix
by 2 clears the denominator.  The resulting symbol is 16(zeta^7-1)/(zeta-1),
which vanishes at every primitive 7th root of unity -- six singular blocks.

What this does and does not establish.  M >= 6 is certified exactly, and
Z = n+2 is certified exactly.  M <= 6 is the regular-base ceiling, which is
CONJECTURAL (thm:cexcover kills it for arbitrary bases; cor:regblocks says why
regularity is the right hypothesis).  If it holds, M = 6 while Z = n+2, so

        Z - M  =  n - 4  ->  infinity

on cubic graphs -- an infinite family with bounded maximum nullity and unbounded
zero forcing number, the gap explained by a parameter read off the base.  Until
the ceiling is proved, what is unconditional is: Z - (equivariant maximum
nullity) = n - 4, since thm:cover bounds equivariant matrices by D outright.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from verification.cover_ceiling_attack import cover_connected, degree_span

K4_BASE = ([(0, 1, 0), (0, 2, 1), (0, 3, 0), (1, 2, 2), (1, 3, 0), (2, 3, 1)], 4)

#: the certificate: every edge weight 2, diagonals (4,4,5,4)
CERT_EDGE_WEIGHT = 2
CERT_DIAG = (4, 4, 5, 4)

#: Z of the cover, by CP-SAT with optimality proved (see check_z_values)
KNOWN_Z = {4: 6, 5: 7, 6: 8, 7: 9, 8: 10}


def symbol_coefficients():
    """Coefficients of zeta^3 * det M(zeta) for the certificate weights."""
    z = sp.symbols("z")
    be, nV = K4_BASE
    M = sp.zeros(nV, nV)
    for e, (a, b, v) in enumerate(be):
        M[a, b] += CERT_EDGE_WEIGHT * z ** v
        M[b, a] += CERT_EDGE_WEIGHT * z ** (-v)
    for i in range(nV):
        M[i, i] += CERT_DIAG[i]
    num, _den = sp.fraction(sp.together(sp.expand(M.det())))
    P = sp.Poly(sp.expand(num), z)
    co = {m[0]: c for m, c in zip(P.monoms(), P.coeffs())}
    return [co.get(i, 0) for i in range(7)]


def certificate_matrix(n):
    """The integer matrix on the cover, as an exact sympy Matrix."""
    be, nV = K4_BASE
    N = nV * n
    A = sp.zeros(N, N)
    for (x, y, v) in be:
        for i in range(n):
            p, q = x * n + i, y * n + ((i + v) % n)
            A[p, q] += sp.Integer(CERT_EDGE_WEIGHT)
            A[q, p] += sp.Integer(CERT_EDGE_WEIGHT)
    for x in range(nV):
        for i in range(n):
            A[x * n + i, x * n + i] = sp.Integer(CERT_DIAG[x])
    return A, N


def check_span_constant(ns=(4, 5, 6, 7, 8, 9, 10)):
    """D = 6 for the base, and the cover is cubic, simple and connected."""
    be, nV = K4_BASE
    D = degree_span(be, nV)
    rows = []
    for n in ns:
        A, N = certificate_matrix(n)
        degs = {sum(1 for c in range(N) if c != r and A[r, c] != 0)
                for r in range(N)}
        rows.append((n, N, D, sorted(degs), cover_connected(be, nV, n)))
    return D, rows


def check_symbol():
    """The certificate realises 16(zeta^7-1)/(zeta-1): all coefficients equal."""
    co = symbol_coefficients()
    return co, len(set(co)) == 1 and co[0] != 0


def check_certificate(ns=(7, 14)):
    """Exact nullity of the integer certificate equals D."""
    be, nV = K4_BASE
    D = degree_span(be, nV)
    rows = []
    for n in ns:
        A, N = certificate_matrix(n)
        rows.append((n, N, N - A.rank(), D))
    return rows


def check_z_values(max_seconds=600):
    """Z of the cover, by CP-SAT, optimality proved.  Returns (n, |V|, Z)."""
    sys.path.insert(0, f"{_REPO}/src/zero_forcing")
    from cpsat import zero_forcing_number
    be, nV = K4_BASE
    rows = []
    for n in sorted(KNOWN_Z):
        A, N = certificate_matrix(n)
        masks = [sum(1 << u for u in range(N) if u != v and A[v, u] != 0)
                 for v in range(N)]
        r = zero_forcing_number(masks, max_seconds=max_seconds)
        Z = r[0] if isinstance(r, tuple) else r
        rows.append((n, N, Z, KNOWN_Z[n]))
    return rows


if __name__ == "__main__":
    D, rows = check_span_constant()
    print("K_4 base: D = %d, constant in n" % D)
    for n, N, D_, degs, conn in rows:
        print("   n=%-3d |V|=%-4d degrees=%s connected=%s" % (n, N, degs, conn))
    co, ok = check_symbol()
    print("symbol coefficients of zeta^3 det M: %s   all equal? %s" % (co, ok))
    print("exact certificate (edges 2, diagonals %s):" % (CERT_DIAG,))
    for n, N, nul, D_ in check_certificate():
        print("   n=%-3d |V|=%-4d exact nullity=%d  vs D=%d  %s"
              % (n, N, nul, D_, "=" if nul == D_ else "!"))
    print("zero forcing number by CP-SAT (optimality proved):")
    for n, N, Z, want in check_z_values():
        print("   n=%-3d |V|=%-4d Z=%-4s (expected %d)   Z - D = %+d"
              % (n, N, Z, want, (Z - D) if Z else 0))
