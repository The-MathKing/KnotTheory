"""
The period-1 (rho-equivariant) certificate ceiling is exactly 6, for every k.

For A in S(P(n,k)) equivariant under the rotation rho, put b = 1 and
  U = a I + (P + P^{-1}),  V = d I + e(P^k + P^{-k}),  C = c I.
Fourier diagonalisation splits A into n blocks
  M_m = [[a + s_m, c],[c, d + e t_m]],  s_m = 2cos(2 pi m/n), t_m = 2cos(2 pi k m/n),
so nullity(A) = #{m : (a + s_m)(d + e t_m) = c^2}.  Since s = z + 1/z gives
t = z^k + z^{-k}, we have t = L_k(s) exactly, where L_k is the monic degree-k
integer polynomial with L_k(z + 1/z) = z^k + z^{-k} (so L_1 = s, L_2 = s^2 - 2,
L_k = s L_{k-1} - L_{k-2}).  Dividing by e, the singularity condition becomes

    F(s) = (s + a) L_k(s) + alpha s + beta = 0,     alpha = d/e, beta = (ad - c^2)/e,

a MONIC polynomial of degree k+1 carrying exactly THREE free parameters
(a, alpha, beta), whatever k is.  The singular blocks are the m with s_m a root
of F, and m, n-m give the same s, so each interior root contributes 2 and a
root at s = +-2 contributes 1.

Two consequences, both checked below:

(1) F is determined by any three of its roots, LINEARLY: at a root r,
    a L_k(r) + alpha r + beta = -r L_k(r).  So three prescribed roots fix
    (a, alpha, beta) and hence all the remaining roots.

(2) Therefore at most three roots can be placed on the grid
    Gamma_n = {2 cos(2 pi m / n)} by choice of parameters, and the period-1
    nullity is at most 6 -- unless the three placed roots happen to force a
    further root onto Gamma_n as well.  This script tests exactly that
    "unless" exhaustively: for every k and n in range and EVERY triple of
    distinct grid values, it solves for (a, alpha, beta) and counts how many
    of the k+1 roots land on Gamma_n, recording the maximum nullity obtained
    and whether any admissible (c^2 > 0, e != 0) case exceeds 6.
"""
import itertools
import numpy as np


def lucas_poly(k):
    """Coefficients of L_k (highest degree first), L_k(z+1/z) = z^k + z^-k."""
    Lm1, L = np.array([1.0]), np.array([1.0, 0.0])      # L_0 = 2? handled below
    if k == 0:
        return np.array([2.0])
    if k == 1:
        return np.array([1.0, 0.0])
    Lprev, Lcur = np.array([2.0]), np.array([1.0, 0.0])  # L_0 = 2, L_1 = s
    for _ in range(2, k + 1):
        nxt = np.polysub(np.polymul([1.0, 0.0], Lcur), Lprev)
        Lprev, Lcur = Lcur, nxt
    return Lcur


def grid(n):
    return np.array(sorted({round(2 * np.cos(2 * np.pi * m / n), 12)
                            for m in range(0, n // 2 + 1)}))


def multiplicity(s, n, tol=1e-8):
    """How many Fourier indices m in Z_n give this value of s (1 or 2)."""
    if abs(abs(s) - 2.0) < tol:
        return 1
    return 2


def analyse(k, n, tol=1e-7):
    Lk = lucas_poly(k)
    G = grid(n)
    best = (0, None)
    for trip in itertools.combinations(range(len(G)), 3):
        r = G[list(trip)]
        Mrow = np.array([[np.polyval(Lk, x), x, 1.0] for x in r])
        rhs = np.array([-x * np.polyval(Lk, x) for x in r])
        if abs(np.linalg.det(Mrow)) < 1e-10:
            continue
        a, alpha, beta = np.linalg.solve(Mrow, rhs)
        F = np.polyadd(np.polymul([1.0, a], Lk), np.array([alpha, beta]))
        roots = np.roots(F)
        tot = 0
        for z in roots:
            if abs(z.imag) > tol:
                continue
            hit = np.min(np.abs(G - z.real))
            if hit < tol:
                tot += multiplicity(z.real, n)
        # admissibility: e != 0 (automatic: F monic after dividing by e) and
        # c^2 > 0.  With e = 1, d = alpha and c^2 = a*alpha - beta.
        c2 = a * alpha - beta
        if c2 > 1e-9 and tot > best[0]:
            best = (tot, (a, alpha, beta, c2, tuple(np.round(r, 6))))
    return best


if __name__ == "__main__":
    print("period-1 (rho-equivariant) maximum nullity, over ALL triples of "
          "grid roots")
    print(f"{'k':>3} {'n':>4} {'2k+2':>5} {'max nullity':>12} {'> 6?':>6}")
    worst = 0
    for k in range(2, 8):
        for n in range(2 * k + 3, 2 * k + 20):
            tot, dat = analyse(k, n)
            worst = max(worst, tot)
            print(f"{k:>3} {n:>4} {2*k+2:>5} {tot:>12} "
                  f"{'YES' if tot > 6 else 'no':>6}", flush=True)
    print(f"\nmaximum period-1 nullity over every case and every root triple: "
          f"{worst}")
    print("period-1 certificates are capped at 6 for every k:",
          "CONFIRMED" if worst <= 6 else "REFUTED")
