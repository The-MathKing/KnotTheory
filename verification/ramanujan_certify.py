"""Certify the Ramanujan classification of P(n,k) exactly, end to end.

For each k the work is finite and the finiteness is itself certified:

  1. finiteness_bound(k) gives B_k, an upper bound on any Ramanujan n, obtained
     from an exact rational bracket on the largest root of the integer
     polynomial D_k below 1.  No n > B_k can be Ramanujan.
  2. Every n in [2k+1, B_k] is then decided by is_ramanujan_exact, which uses
     integer arithmetic in Z[zeta_m] for the exact-zero test and a separation
     guard for the sign.  Nothing in the decision is floating point.
  3. The float64 classifier is run alongside as a CONTROL.  It has no authority;
     a disagreement is reported as a failure of the run, not silently resolved.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))

import sys
sys.path.insert(0, f"{_REPO}")

from verification.ramanujan import is_ramanujan
from verification.ramanujan_exact import is_ramanujan_exact, finiteness_bound, D_poly


def certify(kmax=10):
    print("Exact certification of the Ramanujan classification of P(n,k)")
    print("A cubic graph is Ramanujan iff every nontrivial eigenvalue has")
    print("|lambda| <= 2 sqrt 2; by Sunada this is the Riemann Hypothesis for")
    print("its Ihara zeta function.  Criterion used, exactly:")
    print("    D_k(u) = (7 + 4u T_k(u))^2 - 8(2u + 2T_k(u))^2  >=  0")
    print("at u = cos(2 pi j/n) for every nontrivial index j.")
    print()
    total = disagree = boundary = 0
    summary = []
    for k in range(1, kmax + 1):
        B = finiteness_bound(k)
        deg = D_poly(k).degree()
        print("--- k = %d   (deg D_k = %d, certified bound B_k = %d) ---" % (k, deg, B))
        ram, notram = [], []
        for n in range(2 * k + 1, B + 1):
            e, why = is_ramanujan_exact(n, k)
            f = is_ramanujan(n, k)
            total += 1
            if e != f:
                disagree += 1
                print("    [FAIL] P(%d,%d): exact=%s but float=%s   %s" % (n, k, e, f, why))
            (ram if e else notram).append(n)
        print("    Ramanujan (%d): %s" % (len(ram), ram))
        print("    not Ramanujan (%d): %s" % (len(notram), notram if len(notram) <= 30
                                              else str(notram[:28])[:-1] + ", ...]"))
        print("    no n > %d is Ramanujan, by the certified bound" % B)
        summary.append((k, B, ram))
    print()
    print("==================================================================")
    print("COMPLETE CLASSIFICATION  --  every case decided in exact arithmetic")
    for k, B, ram in summary:
        print("  k=%-3d  %2d Ramanujan values, largest n = %-4d  (bound %d)"
              % (k, len(ram), max(ram) if ram else 0, B))
    print()
    print("  cases certified: %d" % total)
    print("  disagreements with the float64 control: %d" % disagree)
    print("  ALL CERTIFIED" if disagree == 0 else "  RUN FAILED")


if __name__ == "__main__":
    certify(int(sys.argv[1]) if len(sys.argv) > 1 else 10)
