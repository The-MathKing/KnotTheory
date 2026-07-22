"""
Certified period-1 lower bounds on Z(P(n,k)), and the exact values they give.

Pipeline.  For each (n,k):
  1. Filter.  The family condition at a root r is linear
     (a L_k(r) + alpha r + beta = -r L_k(r)), so any three distinct grid roots
     determine (a, alpha, beta).  Running over all triples of
     Gamma_n = {2cos(2 pi m/n)} therefore finds every period-1 symbol with at
     least three grid roots, hence every nullity >= 6.  This pass is floating
     point and is used ONLY to propose candidate root sets.
  2. Certify.  Each candidate root set, recorded as a set of Fourier indices
     m, is re-checked in exact arithmetic in Q(zeta_n)
     (verification/exact_certifier.py): that prod (s - r_m) really does lie in
     the family, that a, alpha, beta, c^2 are real, and that c^2 > 0.
     Floating point alone is not admissible here -- a loose grid tolerance
     once reported nullity 7 for k = 2, which the ceiling 2k+2 = 6 forbids.
  3. Report.  nullity(A) is a lower bound on Z(P(n,k)) because M(G) <= Z(G);
     combined with Z(P(n,k)) <= 2k+2 (the rotation-bootstrap theorem), a
     certified nullity of 2k+2 determines Z(P(n,k)) exactly.
"""
import itertools
import sys

import numpy as np

from exact_certifier import certify, numeric_check


def lucas_poly(k):
    Lprev, Lcur = np.array([2.0]), np.array([1.0, 0.0])
    for _ in range(2, k + 1):
        Lprev, Lcur = Lcur, np.polysub(np.polymul([1.0, 0.0], Lcur), Lprev)
    return Lcur


def candidates(n, k, tol=1e-9):
    """Propose root index sets, best first, by the floating-point filter."""
    ms = [m for m in range(0, n // 2 + 1)]
    G = np.array([2 * np.cos(2 * np.pi * m / n) for m in ms])
    Lk = lucas_poly(k)
    LG = np.polyval(Lk, G)
    mult = np.array([1 if m == 0 or 2 * m == n else 2 for m in ms])
    out = {}
    for t in itertools.combinations(range(len(ms)), 3):
        M = np.column_stack([LG[list(t)], G[list(t)], np.ones(3)])
        if abs(np.linalg.det(M)) < 1e-12:
            continue
        a, al, be = np.linalg.solve(M, -G[list(t)] * LG[list(t)])
        if a * al - be <= 1e-9:
            continue
        vals = (G + a) * LG + al * G + be
        scale = max(1.0, abs(a) + abs(al) + abs(be), np.abs(LG).max())
        hit = np.abs(vals) < tol * scale
        if hit.sum() != k + 1:
            continue
        key = tuple(sorted(ms[i] for i in np.where(hit)[0]))
        out[key] = int(mult[hit].sum())
    return sorted(out.items(), key=lambda kv: -kv[1])


def run(cases):
    print(f"{'graph':>10} {'2k+2':>5} {'nullity':>8} {'a':>10} {'d':>10} "
          f"{'c^2':>10} {'exact':>6} {'matrix':>7} {'gap':>9}")
    exact_values, bounds = [], []
    for (n, k) in cases:
        got = None
        for (ms, nul) in candidates(n, k):
            res, why = certify(n, k, list(ms))
            if res is None:
                continue
            r, cubic, gap = numeric_check(n, k, res["a"], res["alpha"],
                                          res["c2"])
            if r != res["nullity"] or not cubic:
                continue
            got = (res, r, gap)
            break
        if got is None:
            print(f"{'P(%d,%d)'%(n,k):>10} {2*k+2:>5} {'-':>8}")
            continue
        res, r, gap = got
        print(f"{'P(%d,%d)'%(n,k):>10} {2*k+2:>5} {res['nullity']:>8} "
              f"{res['a']:>10.5f} {res['alpha']:>10.5f} {res['c2']:>10.5f} "
              f"{'YES':>6} {r:>7} {gap:>9.2e}", flush=True)
        if res["nullity"] == 2 * k + 2:
            exact_values.append((n, k, res))
        else:
            bounds.append((n, k, res))
    print("\nEXACT VALUES  (certified nullity 2k+2, with Z <= 2k+2 from the "
          "rotation bootstrap)")
    for (n, k, res) in exact_values:
        print(f"  Z(P({n},{k})) = M(P({n},{k})) = {2*k+2}"
              f"    [a={res['a']:.5f}, d={res['alpha']:.5f}, "
              f"c^2={res['c2']:.5f}, roots m in {res['ms']}]")
    print("\nOTHER CERTIFIED LOWER BOUNDS")
    for (n, k, res) in bounds:
        print(f"  Z(P({n},{k})) >= {res['nullity']}  (2k+2 = {2*k+2})")
    return exact_values, bounds


if __name__ == "__main__":
    cases = [(40, 3), (60, 3), (80, 3), (120, 3),
             (60, 4), (70, 4), (90, 4), (120, 4),
             (24, 5), (48, 5), (72, 5), (96, 5), (120, 5),
             (14, 2), (18, 2), (30, 2)]
    if len(sys.argv) > 1:
        cases = [tuple(int(v) for v in a.split(",")) for a in sys.argv[1:]]
    run(cases)
