"""
A construction valid for ALL n: Z(P(n,2)) >= 6.

For k=2, s_m = 2cos(theta_m) and t_m = 2cos(2 theta_m) = s_m^2 - 2 exactly.
So the singularity condition (a + b s)(d + e t) = c^2 becomes, with b = 1 and
D = d - 2e, the CUBIC in s

        (a + s)(e s^2 + D) - c^2 = 0,

whose coefficients are (e, ae, D, aD - c^2). Given any target monic-normalised
cubic with roots r1,r2,r3 we may solve
        e  = A3,   a = A2/A3,   D = A1,   c^2 = a D - A0,
so ANY three values of s can be made roots. Choosing three of the s_m gives
three points, each contributing blocks m and n-m, hence nullity 6 --- and 6 is
maximal here because a cubic has only three roots.

This is uniform in n: it needs only three distinct s_m with m != 0, n/2, i.e.
n >= 7, plus c^2 > 0, which we check.
"""
import numpy as np
from math import cos, pi
from itertools import combinations
from verification.nullity_period import build, pattern_ok


def certificate(n, tol=1e-9):
    """Return (nullity, params) for an explicit rank-deficient A in S(P(n,2))."""
    S = sorted({round(2*cos(2*pi*m/n), 12) for m in range(1, n) if m != n/2})
    best = (0, None)
    for tri in combinations(S, 3):
        r1, r2, r3 = tri
        # monic cubic with these roots: s^3 + A2 s^2 + A1 s + A0
        A2 = -(r1+r2+r3); A1 = r1*r2 + r1*r3 + r2*r3; A0 = -(r1*r2*r3)
        e = 1.0; a = A2/e; D = A1; c2 = a*D - A0
        if c2 <= 1e-9:
            continue
        d = D + 2*e
        p = np.array([a, 1.0, np.sqrt(c2), d, e])     # a, b, c, inner-diag, inner-edge
        A = build(n, 2, 1, p)
        if not pattern_ok(n, 2, A):
            continue
        sc = np.max(np.abs(A))
        if min(abs(p[1]), abs(p[2]), abs(p[4])) < 0.01*sc:
            continue
        ev = np.sort(np.abs(np.linalg.eigvalsh(A)))
        nul = int(np.sum(ev < 1e-9*sc))
        if 0 < nul < len(ev) and ev[nul] < 1e5*ev[nul-1]:
            continue
        if nul > best[0]:
            best = (nul, p)
    return best


if __name__ == "__main__":
    print("Uniform certificate for Z(P(n,2)) >= 6")
    print(f"{'n':>4} {'nullity':>8} {'Z':>3}  status")
    print("-"*30)
    allok = True
    for n in range(10, 41, 2):
        nul, p = certificate(n)
        ok = (nul >= 6)
        allok &= ok
        print(f"{n:>4} {nul:>8} {6:>3}  {'>= 6 OK' if ok else 'FAILS'}", flush=True)
    for n in range(11, 42, 2):
        nul, p = certificate(n)
        ok = (nul >= 6)
        allok &= ok
        print(f"{n:>4} {nul:>8} {6:>3}  {'>= 6 OK' if ok else 'FAILS'}", flush=True)
    print("\nCONSTRUCTION SUCCEEDS FOR EVERY n TESTED" if allok else "\nSOME n FAIL")
