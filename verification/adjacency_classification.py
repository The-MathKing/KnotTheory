"""
Complete classification of the adjacency nullity of P(n,k).

The adjacency matrix is the period-1 certificate with a = d = 0, b = c = e = 1,
so its Fourier blocks are [[s_m, 1],[1, t_m]] and

    nullity(Adj P(n,k)) = #{ m : s_m t_m = 1 }
                        = #{ m : 2cos(2 pi (k+1)m/n) + 2cos(2 pi (k-1)m/n) = 1 },

a rational linear relation among cosines of rational angles -- the setting of
the Conway-Jones theorem (1976), which classifies all such relations and in
particular implies only finitely many angle-denominators can occur.

That finiteness can be made completely explicit.  Put z = e^{2 pi i m/n}.  Then
s t = 1 reads z^{k+1} + z^{-(k+1)} + z^{k-1} + z^{-(k-1)} = 1, and multiplying
through by z^{k+1} gives the integer polynomial

    P_k(z) = z^{2k+2} + z^{2k} - z^{k+1} + z^2 + 1 .

So the m that count are exactly those with omega^m a common root of P_k and
z^n - 1, i.e. the roots of P_k that are n-th roots of unity.  Factoring P_k
over Q and keeping its CYCLOTOMIC factors therefore gives, exactly,

    nullity(Adj P(n,k)) = sum over d with Phi_d | P_k and d | n of phi(d).

This is a complete answer for every k: a finite list of d per k, computed once.
"""
import sys

from sympy import Poly, symbols, factor_list, cyclotomic_poly, totient, divisors

z = symbols("z")


def P_k(k):
    return Poly(z**(2*k+2) + z**(2*k) - z**(k+1) + z**2 + 1, z)


def cyclotomic_factors(k, dmax=400):
    """The d with Phi_d dividing P_k."""
    p = P_k(k)
    out = []
    for d in range(1, dmax + 1):
        phi = Poly(cyclotomic_poly(d, z), z)
        if phi.degree() > p.degree():
            continue
        q, r = divmod(p, phi)
        if r.is_zero:
            out.append(d)
    return out


def nullity(n, k, facs=None):
    if facs is None:
        facs = cyclotomic_factors(k)
    return sum(int(totient(d)) for d in facs if n % d == 0)


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    print("Adjacency nullity of P(n,k), classified exactly\n")
    print("P_k(z) = z^(2k+2) + z^(2k) - z^(k+1) + z^2 + 1\n")
    print(f"{'k':>3} {'2k+2':>5} {'cyclotomic factors Phi_d of P_k':>34} "
          f"{'lcm':>6} {'nullity when lcm | n':>21}")
    for k in range(2, kmax + 1):
        facs = cyclotomic_factors(k)
        if not facs:
            print(f"{k:>3} {2*k+2:>5} {'none':>34} {'-':>6} "
                  f"{'0 for every n':>21}")
            continue
        import numpy as np
        L = int(np.lcm.reduce(facs))
        tot = sum(int(totient(d)) for d in facs)
        tag = "  = 2k+2" if tot == 2 * k + 2 else ""
        print(f"{k:>3} {2*k+2:>5} {str(facs):>34} {L:>6} {str(tot)+tag:>21}")
    print("\ncross-check against direct computation:")
    import numpy as np
    bad = 0
    for k in (2, 5, 8):
        facs = cyclotomic_factors(k)
        for n in range(2 * k + 3, 200):
            pred = nullity(n, k, facs)
            m = np.arange(n)
            th = 2 * np.pi * m / n
            direct = int(np.sum(np.abs(2*np.cos((k+1)*th) + 2*np.cos((k-1)*th) - 1)
                                < 1e-9))
            if pred != direct:
                bad += 1
                if bad <= 5:
                    print(f"  MISMATCH k={k} n={n}: formula {pred}, direct {direct}")
    print(f"  k = 2, 5, 8 over 13 <= n < 200: "
          f"{'formula matches direct count everywhere' if bad == 0 else f'{bad} mismatches'}")
