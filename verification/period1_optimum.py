"""
The exact maximum nullity attainable by a period-1 certificate on P(n,k).

The symbol is F(s) = (s + a) L_k(s) + alpha s + beta (see
verification/cyclotomic_certificates.py for the derivation), a MONIC
polynomial of degree k+1 with exactly three free parameters, and

    nullity(A) = sum over roots r of F lying in Gamma_n = {2cos(2 pi m/n)}
                 of  (2 if |r| < 2 else 1),

counting distinct roots, since m and n-m give the same r and s = +-2 is fixed
by that involution.  Admissibility is e != 0 (automatic: F is monic after
dividing by e) together with c^2 = a alpha - beta > 0.

This scan is EXHAUSTIVE for every nullity >= 6.  At a root r the family
condition is linear,

    a L_k(r) + alpha r + beta = -r L_k(r),

so any three distinct grid roots determine (a, alpha, beta) uniquely.  Hence
every admissible F with three or more grid roots is produced by some triple,
and running over all triples of Gamma_n finds the true period-1 optimum.
Evaluating F on the whole grid at once replaces root-finding, which is what
makes the full range of n affordable.
"""
import itertools
import sys

import numpy as np


def lucas_poly(k):
    Lprev, Lcur = np.array([2.0]), np.array([1.0, 0.0])
    for _ in range(2, k + 1):
        Lprev, Lcur = Lcur, np.polysub(np.polymul([1.0, 0.0], Lcur), Lprev)
    return Lcur if k >= 1 else Lprev


def grid(n):
    return np.array(sorted({round(2 * np.cos(2 * np.pi * m / n), 13)
                            for m in range(0, n // 2 + 1)}))


def matrix_nullity(n, k, a, alpha, c2, cond_max=1e3, tol=1e-11):
    """Nullity counted BLOCK BY BLOCK, which is the only scale-free way.

    Counting grid hits by |F(r)| < tol against a global scale gives false
    positives: with a loose tolerance it reported nullity 7 for k = 2 (the
    ceiling 2k+2 = 6 forbids it), and with a badly scaled certificate --
    |a| enormous against the edge weights 1 -- a threshold relative to
    max|A| swallowed 48 eigenvalues at (n,k) = (48,7).  Each Fourier block
    M_m = [[a + s_m, c], [c, alpha + t_m]] carries its own scale, so test
    |det M_m| against that block's norm squared, and reject certificates
    whose diagonal dwarfs the edge weights, since those are useless anyway."""
    c = np.sqrt(c2)
    if max(abs(a), abs(alpha)) > cond_max * min(1.0, c):
        return 0
    m = np.arange(n)
    s = 2 * np.cos(2 * np.pi * m / n)
    t = 2 * np.cos(2 * np.pi * k * m / n)
    det = (a + s) * (alpha + t) - c2
    nrm = np.maximum.reduce([np.abs(a + s), np.abs(alpha + t),
                             np.full(n, abs(c))])
    return int(np.sum(np.abs(det) < tol * np.maximum(nrm, 1.0) ** 2))


def best_for(n, k, tol=1e-10):
    Lk = lucas_poly(k)
    G = grid(n)
    LG = np.polyval(Lk, G)
    mult = np.where(np.abs(np.abs(G) - 2.0) < 1e-9, 1, 2)
    best = (0, None)
    idx = range(len(G))
    for t in itertools.combinations(idx, 3):
        r = G[list(t)]
        M = np.column_stack([LG[list(t)], r, np.ones(3)])
        det = np.linalg.det(M)
        if abs(det) < 1e-12:
            continue
        a, alpha, beta = np.linalg.solve(M, -r * LG[list(t)])
        c2 = a * alpha - beta
        if c2 <= 1e-9:
            continue
        vals = (G + a) * LG + alpha * G + beta
        scale = max(1.0, np.abs(a) + np.abs(alpha) + np.abs(beta),
                    np.abs(LG).max())
        hit = np.abs(vals) < tol * scale
        nul = int(mult[hit].sum())
        if nul <= best[0]:
            continue
        conf = matrix_nullity(n, k, a, alpha, c2)
        assert conf <= 2 * k + 2, (n, k, conf)      # the structural ceiling
        if conf > best[0]:
            best = (conf, (float(a), float(alpha), float(beta), float(c2),
                           tuple(np.round(G[hit], 6))))
    return best


def verify(n, k, a, alpha, c2, expect):
    P = np.roll(np.eye(n), 1, axis=1)
    A = np.block([[a * np.eye(n) + P + P.T, np.sqrt(c2) * np.eye(n)],
                  [np.sqrt(c2) * np.eye(n),
                   alpha * np.eye(n) + np.linalg.matrix_power(P, k)
                   + np.linalg.matrix_power(P.T, k)]])
    lam = np.sort(np.abs(np.linalg.eigvalsh(A)))
    got = int(np.sum(lam < 1e-9 * np.abs(A).max()))
    B = np.abs(A) > 1e-12
    np.fill_diagonal(B, False)
    return got, bool(np.all(B.sum(axis=1) == 3)), lam[expect] if expect < len(lam) else np.nan


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 130
    print("maximum period-1 nullity, exhaustive over all triples of grid roots")
    print(f"{'k':>3} {'2k+2':>5} {'best nullity':>13} {'attained at n':>40}")
    exact_hits = []
    for k in range(2, kmax + 1):
        per_n = {}
        for n in range(2 * k + 3, nmax + 1):
            if 2 * k >= n:
                continue
            nul, dat = best_for(n, k)
            per_n[n] = (nul, dat)
        top = max(v[0] for v in per_n.values())
        ns = [n for n, v in per_n.items() if v[0] == top]
        print(f"{k:>3} {2*k+2:>5} {top:>13} {str(ns[:12]):>40}", flush=True)
        for n in ns:
            nul, dat = per_n[n]
            if nul == 2 * k + 2:
                exact_hits.append((n, k, nul, dat))
        # also record the best n for each nullity level >= 2k
        for lvl in range(2 * k + 2, 2 * k - 1, -1):
            nn = sorted([n for n, v in per_n.items() if v[0] == lvl])
            if nn:
                print(f"       nullity {lvl:>2}: n = {nn[:14]}"
                      f"{' ...' if len(nn) > 14 else ''}", flush=True)
    print("\nexact values Z(P(n,k)) = 2k+2 certified by a period-1 matrix:")
    for (n, k, nul, dat) in exact_hits:
        a, alpha, beta, c2, roots = dat
        got, cubic, gap = verify(n, k, a, alpha, c2, nul)
        print(f"  Z(P({n},{k})) = {nul}   a={a:+.4f} d={alpha:+.4f} "
              f"c^2={c2:.4f}   matrix nullity {got}, cubic {cubic}, "
              f"gap {gap:.1e}  {'OK' if got == nul and cubic else 'MISMATCH'}")
