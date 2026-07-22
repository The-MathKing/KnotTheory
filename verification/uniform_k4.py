"""
Uniform-in-n lower bound for k=4:  Z(P(n,4)) >= 8.

d=2, k=4 (kappa=2). With x = cos(2 pi l/m), m=n/2, the inner variable is
w = 2cos(2 kappa pi l/m) = 2 T_kappa(x) = 4x^2 - 2. Substituting into the
singularity condition (x + mu) N(w) = L(w) turns N and L into EVEN QUARTICS in
x, so the condition is the quintic

    n4 x^5 + (mu n4 - l4) x^4 + n2 x^3 + (mu n2 - l2) x^2 + n0 x + (mu n0 - l0).

Its coefficients are free (choose n_i, then l_i = mu n_i - A_i), so any five
roots are attainable in principle. Realisability -- N and L must factor over R,
c_r^2 > 0, |mu| >= 1 -- is what limits us; empirically five roots force
c_r^2 <= 0, so we fit FOUR roots, leaving a free root to absorb the constraint,
giving 4 points and nullity 8.
"""
import numpy as np
from math import cos, pi
from itertools import combinations
from verification.nullity_d2 import recover
from verification.nullity_period import build, pattern_ok


def xs(n):
    m = n//2
    return sorted({round(cos(2*pi*l/m), 12) for l in range(1, m) if l != m/2})


def certificate(n, ngrid=160):
    """Explicit period-2 matrix in S(P(n,4)); returns (nullity, params)."""
    X = xs(n)
    if len(X) < 4:
        return 0, None
    best = (0, None)
    for four in combinations(X, 4):
        # quintic with these four as roots, fifth root free -> pencil in r5
        for r5 in np.linspace(-1.95, 1.95, ngrid):
            roots = list(four) + [r5]
            poly = np.poly(roots)           # monic degree-5 coefficients A5..A0
            A5, A4, A3, A2, A1, A0 = poly
            n4, n2, n0 = A5, A3, A1
            for mu in (1.02, 1.2, 1.5, 2.0, 3.0, -1.2, -2.0):
                l4, l2, l0 = mu*n4 - A4, mu*n2 - A2, mu*n0 - A0
                # back to w-coefficients: n0=G-2H+4K, n2=4H-16K, n4=16K
                K = n4/16.0
                H = (n2 + 16*K)/4.0
                G = n0 + 2*H - 4*K
                LK = l4/16.0
                LH = (l2 + 16*LK)/4.0
                LG = l0 + 2*LH - 4*LK
                p = recover((G, H, K, mu*G - LG, mu*H - LH, mu*K - LK), mu)
                if p is None:
                    continue
                A = build(n, 4, 2, p)
                if not pattern_ok(n, 4, A):
                    continue
                sc = np.max(np.abs(A))
                if min(abs(p[2]), abs(p[3]), abs(p[4]), abs(p[5]),
                       abs(p[8]), abs(p[9])) < 0.015*sc:
                    continue
                ev = np.sort(np.abs(np.linalg.eigvalsh(A)))
                nul = int(np.sum(ev < 1e-9*sc))
                if 0 < nul < len(ev) and ev[nul] < 1e5*ev[nul-1]:
                    continue
                if nul > best[0]:
                    best = (nul, p)
                    if nul >= 8:
                        return best
    return best


if __name__ == "__main__":
    print("Uniform certificate attempt for Z(P(n,4)) >= 8")
    print(f"{'n':>4} {'nullity':>8}  status")
    print("-"*26)
    res = {}
    for n in range(14, 41, 2):
        nul, _ = certificate(n)
        res[n] = nul
        print(f"{n:>4} {nul:>8}  {'>= 8 OK' if nul >= 8 else ('=%d' % nul)}", flush=True)
    good = [n for n,v in res.items() if v >= 8]
    print(f"\nreached 8 for n in {good}")
    print(f"failed for n in {[n for n,v in res.items() if v < 8]}")
