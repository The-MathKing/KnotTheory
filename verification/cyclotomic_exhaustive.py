"""
Is the cyclotomic search EXHAUSTIVE, or just bounded?

A period-1 symbol is F(s) = (s+a)L_k(s) + alpha s + beta, monic of degree k+1.
Its nullity is 2*(number of distinct roots in the open interval (-2,2) that lie
in Gamma_n) + (number of roots at +-2).  So nullity 2k+2 forces F to be
SQUAREFREE with all k+1 roots interior and on the grid.

If F additionally has RATIONAL coefficients, then F is a product of distinct
minimal polynomials Psi_d of 2cos(2 pi/d), d >= 3, with

    sum_{d in D} deg Psi_d = k+1,     deg Psi_d = phi(d)/2.

The key point: every individual factor must satisfy deg Psi_d <= k+1, i.e.
phi(d) <= 2k+2.  Since phi(d) -> infinity, only FINITELY many d qualify, and
they can all be listed.  So for each k the search over rational symbols is a
FINITE, COMPLETE enumeration -- not a bounded scan that might have missed
something further out.

This script makes that explicit: for each k it prints the complete list of
admissible d, enumerates every D, and reports for each candidate why it
fails (not in the three-parameter family / c^2 <= 0) or that it succeeds.
A "no" for some k is therefore a theorem about rational symbols, not a
statement about how far we looked.  Irrational symbols are NOT covered --
verification/period1_optimum.py searches those.
"""
import sys
from fractions import Fraction

import numpy as np
from sympy import totient

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from cyclotomic_certificates import lucas_poly, psi, membership


def admissible_d(k):
    """Every d >= 3 with deg Psi_d = phi(d)/2 <= k+1.  Finite and complete:
    phi(d) >= sqrt(d/2), so phi(d) <= 2k+2 forces d <= 2*(2k+2)^2."""
    cap = 2 * (2 * k + 2) ** 2
    return [d for d in range(3, cap + 1) if int(totient(d)) // 2 <= k + 1]


def scan_k(k, verbose=True):
    degs = {d: int(totient(d)) // 2 for d in admissible_d(k)}
    pool = sorted(degs)
    target = k + 1
    subsets = []

    def rec(start, remaining, chosen):
        if remaining == 0:
            subsets.append(tuple(chosen)); return
        for i in range(start, len(pool)):
            d = pool[i]
            if degs[d] > remaining:
                continue
            chosen.append(d); rec(i + 1, remaining - degs[d], chosen); chosen.pop()

    rec(0, target, [])
    hits, reasons = [], {"not in family": 0, "c^2 <= 0": 0}
    for D in subsets:
        F = [1]
        for d in D:
            F = np.polymul(np.array(F, dtype=object),
                           np.array(psi(d), dtype=object)).tolist()
        F = [int(v) for v in F]
        mem = membership(F, k)
        if mem is None:
            reasons["not in family"] += 1
            continue
        a, alpha, beta = mem
        c2 = a * alpha - beta
        if c2 <= 0:
            reasons["c^2 <= 0"] += 1
            continue
        hits.append((D, a, alpha, c2, int(np.lcm.reduce(list(D)))))
    if verbose:
        print(f"\nk = {k}   (target degree k+1 = {target}, ceiling 2k+2 = {2*k+2})")
        print(f"  admissible d (phi(d)/2 <= {target}), complete list: {pool}")
        print(f"  candidate factorisations F = prod Psi_d : {len(subsets)}")
        print(f"    rejected, not in the 3-parameter family : "
              f"{reasons['not in family']}")
        print(f"    rejected, c^2 <= 0 (not realisable)     : {reasons['c^2 <= 0']}")
        print(f"    ADMISSIBLE, nullity 2k+2                : {len(hits)}")
        for (D, a, al, c2, L) in hits:
            print(f"      D={D}  a={a} d={al} c^2={c2}  ->  every n divisible by {L}")
        if not hits:
            print(f"    => NO rational period-1 symbol attains {2*k+2} for k={k}.")
            print(f"       This is exhaustive over rational symbols, not a "
                  f"bounded search.")
    return hits, len(subsets)


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    print("Complete enumeration of RATIONAL period-1 symbols attaining 2k+2")
    print("=" * 72)
    summary = []
    for k in range(2, kmax + 1):
        hits, ncand = scan_k(k)
        summary.append((k, len(hits), ncand))
    print("\n" + "=" * 72)
    print(f"{'k':>3} {'2k+2':>5} {'candidates':>11} {'admissible':>11}  verdict")
    for (k, h, n) in summary:
        print(f"{k:>3} {2*k+2:>5} {n:>11} {h:>11}  "
              f"{'ATTAINED' if h else 'impossible for rational symbols'}")
