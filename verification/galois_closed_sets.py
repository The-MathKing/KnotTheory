"""
Galois-closed root sets: the route to an EXACT period-d certificate.

A period-d certificate is found numerically, so its weights are algebraic
numbers from a Newton solve rather than the integers the period-1 cyclotomic
certificates enjoy.  That makes exact verification awkward -- unless the target
symbol itself is rational.

The target is G* = prod (sigma - sigma_l) over the chosen grid values.  If the
chosen set is a union of full Galois orbits inside Gamma_m, then G* is a
product of the minimal polynomials Psi_e and therefore lies in Z[sigma].  The
system G(w) = G* then has RATIONAL coefficients, which is the precondition for
recovering exact weights.

The orbit of 2cos(2 pi l/m) consists of all l' with m/gcd(l',m) = m/gcd(l,m);
for order e >= 3 the orbit has size phi(e)/2.  This script enumerates the
interior orbits of Gamma_m, forms every union of total size k+1, and tests each
for a realisable solution.
"""
import itertools
import sys
from math import gcd

import numpy as np
from sympy import totient, Poly, symbols

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from prescribe_symbol import solve_for, grid_interior
from verify_period_d_cert import verify
from cyclotomic_certificates import psi


def interior_orbits(m):
    """{order e: sorted list of l in [1, m/2] with 2cos(2 pi l/m) of order e},
    restricted to interior values (|sigma| < 2, i.e. e >= 3)."""
    orb = {}
    for l in range(1, m // 2 + 1):
        e = m // gcd(l, m)
        if e < 3:                       # e = 1 or 2 gives sigma = +-2
            continue
        orb.setdefault(e, []).append(l)
    return orb


def galois_closed_sets(m, want):
    orb = interior_orbits(m)
    es = sorted(orb)
    out = []
    for r in range(1, len(es) + 1):
        for combo in itertools.combinations(es, r):
            if sum(len(orb[e]) for e in combo) == want:
                ls = sorted(l for e in combo for l in orb[e])
                out.append((combo, tuple(ls)))
    return out, orb


if __name__ == "__main__":
    k, d, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    tries = int(sys.argv[4]) if len(sys.argv) > 4 else 25
    m = n // d
    orb = interior_orbits(m)
    print(f"k={k} d={d} n={n} m={m}")
    print(f"interior Galois orbits of Gamma_{m}:")
    for e in sorted(orb):
        print(f"   order {e:>3}: l = {orb[e]}  (size {len(orb[e])} "
              f"= phi({e})/2 = {int(totient(e))//2})")
    sets, _ = galois_closed_sets(m, k + 1)
    print(f"\nGalois-closed sets of size {k+1}: {len(sets)}")
    s = symbols("s")
    G0 = grid_interior(m)
    for (orders, ls) in sets:
        F = [1]
        for e in orders:
            F = np.polymul(np.array(F, dtype=object),
                           np.array(psi(e), dtype=object)).tolist()
        F = [int(v) for v in F]
        print(f"\n  orders {orders}  ->  l = {ls}")
        print(f"    G* = {Poly(F, s).as_expr()}   (integer coefficients)")
        roots = [sig for (l, sig) in G0 if l in ls]
        w, err, _ = solve_for(n, k, d, roots, tries=tries, push=3.0)
        print(f"    symbol solve error {err:.2e}")
        ok, r, gap, minoff = verify(w, n, k, d, verbose=False)
        print(f"    nullity {r} (target {2*k+2}), gap {gap:.2e}, "
              f"min|required|/scale {minoff:.4f}  "
              f"{'REALISABLE' if ok else 'not realisable'}")
        if ok:
            np.save(f"/Volumes/2TB/scifair/results/zero_forcing/"
                    f"galois_cert_k{k}_d{d}_n{n}.npy", w)
            lab = ([f"b{i}" for i in range(d)] + [f"c{i}" for i in range(d)]
                   + [f"e{i}" for i in range(d)] + [f"aO{i}" for i in range(d)]
                   + [f"aI{i}" for i in range(d)])
            for L, v in zip(lab, w):
                print(f"       {L:>4} = {v:+.12f}")
