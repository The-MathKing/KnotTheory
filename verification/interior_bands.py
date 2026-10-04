"""Where the negative bands of D_k lie on [-1, 1], decided EXACTLY.

The Ramanujan criterion (thm:crit) says P(n,k) satisfies the RH iff
D_k(cos 2*pi*j/n) >= 0 at every nontrivial j, where

    D_k(u) = (7 + 4u T_k(u))^2 - 8 (2u + 2T_k(u))^2   in  Z[u],

T_k the Chebyshev polynomial.  D_k(1) = -7 always, and D_k(-1) = -7 for odd k,
so there is a band of negativity at u = 1 and, for odd k, at u = -1.  Whether
there are OTHER negative bands inside (-1, 1) decides whether the classification
for that k is an initial segment (thm:closedsmall) or needs the census.

This module isolates the real roots of D_k in [-1, 1] with exact rational
arithmetic (sympy's Poly.intervals: Sturm/VAS root isolation over Q) and reads
off the sign pattern.  Nothing floating-point enters the decision.

simple(k) is True when the negative set of D_k on [-1,1] is exactly
  (u_k, 1]            for even k,
  [-1,-u_k) u (u_k,1] for odd k,
with u_k the largest root below 1.  Then the only grid points that can fall in
a band are j = 1 and, for odd n and odd k, j = (n-1)/2 -- which is the whole
content of the closed form.
"""
import sys
import sympy as sp

u = sp.symbols("u")


def Dk_poly(k):
    Tk = sp.chebyshevt(k, u)
    return sp.Poly(sp.expand((7 + 4 * u * Tk) ** 2 - 8 * (2 * u + 2 * Tk) ** 2), u)


def band_structure(k):
    """Return (roots, signs, simple) where roots are the exact isolating
    intervals of the real roots of D_k in [-1,1] (as Rationals, in increasing
    order), signs are the signs of D_k on the gaps between consecutive roots
    (from -1 to 1), and simple says the only bands are the end bands."""
    D = Dk_poly(k)
    ivals = [(sp.Rational(a), sp.Rational(b)) for (a, b), _m in D.intervals(inf=-1, sup=1)]
    signs = []
    prev = sp.Integer(-1)
    for a, b in ivals:
        signs.append(int(sp.sign(D.eval((prev + a) / 2))))
        prev = b
    signs.append(int(sp.sign(D.eval((prev + 1) / 2))))
    expected = 1 if k % 2 == 0 else 2
    simple = (len(ivals) == expected
              and signs[-1] == -1
              and signs[0] == (1 if k % 2 == 0 else -1)
              and all(s == 1 for s in signs[1:-1]))
    return ivals, signs, simple


def simple_ks(kmax=45):
    return [k for k in range(1, kmax + 1) if band_structure(k)[2]]


def check_symmetry(kmax=45):
    """D_k is an even function of u exactly when k is odd (T_k odd => u T_k even,
    2u + 2T_k odd); for even k it is not.  Used in the proof of thm:closedsmall."""
    bad = []
    for k in range(1, kmax + 1):
        D = Dk_poly(k)
        even = sp.Poly(D.as_expr().subs(u, -u), u) == D
        if even != (k % 2 == 1):
            bad.append(k)
    return bad


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 45
    for k in range(1, kmax + 1):
        ivals, signs, simple = band_structure(k)
        uk = float(ivals[-1][0]) if ivals else None
        print(f"k={k:2d}: {len(ivals)} root(s) in [-1,1], signs on gaps {signs}, "
              f"u_k >= {uk:.6f}  ->  {'end bands only' if simple else 'interior band'}")
    print("simple k:", simple_ks(kmax))
    print("symmetry exceptions:", check_symmetry(kmax))
