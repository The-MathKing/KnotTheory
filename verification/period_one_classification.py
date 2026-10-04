"""EXACTLY which n admit a rotation-invariant certificate with a rational symbol.

A rotation-invariant matrix on P(n,k) with weights (a, 1, c, d, e) -- outer
edges 1, spokes c, inner edges e, diagonals a and d -- has Fourier blocks
    [[a + s_m, c], [c, d + e t_k(s_m)]],   s_m = 2cos(2 pi m/n),  t_k(s) = 2 T_k(s/2),
and nullity equal to the number of m with F(s_m) = 0 for the SYMBOL
    F(s) = (a + s)(d + e t_k(s)) - c^2 .
Nullity 2k+2 needs k+1 distinct roots, each an interior grid value 2cos(2 pi l/n)
(|s| < 2), each hit by m and n - m.

If F has RATIONAL coefficients (the case for every integer / cyclotomic
certificate in the paper), its root set is a union of full Galois orbits
    O_d = { 2cos(2 pi l/d) : gcd(l, d) = 1 },   |O_d| = phi(d)/2,   d >= 3,
and lies on the grid of P(n,k) iff d | n for every d used.  Conversely, a
union R of orbits with |R| = k+1 is the root set of a realisable symbol iff
    P_R(s) := prod_{r in R} (s - r)  =  (s + a)(t_k(s) + d') - c0
for rationals a, d', c0 with c0 != 0  (then e is free, c^2 = e c0, and the sign
of e makes c^2 > 0 for a symmetric certificate).  Since t_k is monic of degree k,
this says: P_R - (s + a) t_k has degree <= 1, where a = [s^k] P_R.  All the
middle coefficients of P_R are forced by t_k -- the "three free parameters" of
the paper, made exact.

So the set of n admitting a rational-symbol rotation-invariant certificate is
    { n : L | n for some L in LCMS_k },
where LCMS_k is the finite list of lcm(d : O_d in R) over the admissible R.
This module enumerates it: a finite, exact computation in Z[s].
"""
import itertools
import sys
from math import gcd, lcm

import sympy as sp

s = sp.symbols("s")


def psi(d):
    """Minimal polynomial of 2cos(2 pi/d) over Q, monic in Z[s]."""
    z = sp.symbols("z")
    # 2cos(2 pi/d) = z + 1/z with z a primitive d-th root of unity
    mp = sp.minimal_polynomial(2 * sp.cos(2 * sp.pi / d), s)
    return sp.Poly(mp, s)


def t_k(k):
    return sp.Poly(sp.expand(2 * sp.chebyshevt(k, s / 2)), s)


def orbit_size(d):
    return int(sp.totient(d)) // 2


def admissible_sets(k, dmax=None):
    """All unions R of orbits O_d (d >= 3, distinct d) with |R| = k+1 whose
    monic product polynomial has the forced middle coefficients, together with
    (a, d', c0) and whether c0 != 0.  dmax bounds d by phi(d)/2 <= k+1."""
    want = k + 1
    ds = [d for d in range(3, 4 * want * want + 100) if orbit_size(d) <= want]
    if dmax:
        ds = [d for d in ds if d <= dmax]
    tk = t_k(k)
    out = []
    for r in range(1, want + 1):
        for combo in itertools.combinations(ds, r):
            if sum(orbit_size(d) for d in combo) != want:
                continue
            P = sp.Poly(1, s)
            for d in combo:
                P = P * psi(d)
            a = P.coeff_monomial(s ** k) if k >= 1 else 0
            rem = P - sp.Poly(s + a, s) * tk
            if rem.degree() > 1:
                continue
            dprime = rem.coeff_monomial(s) if rem.degree() >= 1 else 0
            const = rem.coeff_monomial(1)
            c0 = a * dprime - const          # F = (s+a)(t_k + d') - c0, so const = a d' - c0
            out.append(dict(ds=combo, lcm=lcm(*combo), a=a, dprime=dprime, c0=c0,
                            realisable=(c0 != 0), poly=P))
    return out


def lcms(k):
    """The finite list of L such that a rational-symbol certificate exists
    exactly for the n divisible by some L (minimal elements under divisibility)."""
    L = sorted({r["lcm"] for r in admissible_sets(k) if r["realisable"]})
    return [x for x in L if not any(y != x and x % y == 0 for y in L)]


def exists_for(n, k):
    return any(n % L == 0 for L in lcms(k))


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    for k in range(2, kmax + 1):
        sets = admissible_sets(k)
        print(f"k={k}: {len(sets)} Galois-closed root sets with the forced coefficients")
        for r in sets:
            print(f"   d={r['ds']}  lcm={r['lcm']}  a={r['a']} d'={r['dprime']} c0={r['c0']}  "
                  f"{'realisable' if r['realisable'] else 'c^2=0, NOT realisable'}")
        print(f"   => rational-symbol certificate exists iff n divisible by one of {lcms(k)}")
