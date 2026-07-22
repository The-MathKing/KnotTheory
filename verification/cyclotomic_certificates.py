"""
Exact, uniform-in-n maximum-nullity certificates for P(n,k) from cyclotomy.

SETUP (period 1).  For A in S(P(n,k)) invariant under the rotation rho, put
b = 1 (scaling) and
    U = a I + (P + P^{-1}),  V = d I + e(P^k + P^{-k}),  C = c I,
so the Fourier blocks are M_m = [[a + s_m, c],[c, d + e t_m]] with
s_m = 2cos(2 pi m/n), t_m = 2cos(2 pi k m/n), and

    nullity(A) = #{ m in Z_n : (a + s_m)(d + e t_m) = c^2 }.

Since s = z + 1/z forces t = z^k + z^{-k} = L_k(s), where L_k is the monic
integer polynomial with L_k(z + 1/z) = z^k + z^{-k}, dividing by e turns the
singularity condition into a MONIC polynomial of degree k+1 in s alone:

    F(s) = (s + a) L_k(s) + alpha s + beta,    alpha = d/e,  beta = (a d - c^2)/e.

F therefore carries exactly three free parameters no matter how large k is,
which is why choosing three roots by hand caps the nullity at 6.  The way past
that cap is not more parameters but ARITHMETIC: if F is chosen with RATIONAL
coefficients, its roots come in full Galois orbits, and the Galois orbit of a
grid value 2cos(2 pi m/n) consists of grid values again.  So a single rational
F can place all k+1 of its roots on the grid at once.

CONSTRUCTION.  For d >= 3 let Psi_d be the minimal polynomial of 2cos(2 pi/d),
of degree phi(d)/2, whose roots are exactly the primitive values
2cos(2 pi j/d), gcd(j,d) = 1.  Take a set D of distinct integers with

    sum_{d in D} deg Psi_d = k + 1,    F = prod_{d in D} Psi_d.

Every root of F lies in Gamma_n = {2cos(2 pi m/n)} as soon as every d in D
divides n.  F lies in the three-parameter family iff, writing
G = F - s L_k(s) and a = [s^k] G, the polynomial G - a L_k(s) has degree <= 1;
that is k-2 linear conditions with integer coefficients.  When they hold, read
off alpha and beta from G - a L_k = alpha s + beta, set e = 1, d = alpha,
c^2 = a alpha - beta, and the certificate is admissible iff c^2 > 0.

Each root in the open interval (-2,2) is hit by two Fourier indices m and n-m,
so an admissible squarefree F with all k+1 roots interior gives

    nullity(A) = 2(k+1) = 2k+2   for EVERY n divisible by lcm(D),

and with Z(P(n,k)) <= 2k+2 from the rotation-bootstrap theorem this forces
    Z(P(n,k)) = M(P(n,k)) = 2k+2   for every such n.
Psi_1 = s-2 and Psi_2 = s+2 contribute only one index each (s = +-2 is fixed by
m -> n-m), so admitting them yields 2k+1 or 2k instead.

Everything here is integer arithmetic: F, the membership conditions, a, alpha,
beta and c^2 are all exact rationals, so the certificates are proofs, not
numerics.  The final check re-derives the nullity from an explicit matrix.
"""
import itertools
from fractions import Fraction

import numpy as np
from sympy import Poly, cyclotomic_poly, symbols, Rational, totient

S = symbols("s")


def lucas_poly(k):
    """L_k as a list of integer coefficients, highest degree first."""
    Lprev, Lcur = [2], [1, 0]                    # L_0 = 2, L_1 = s
    if k == 0:
        return Lprev
    for _ in range(2, k + 1):
        nxt = np.polysub(np.polymul([1, 0], Lcur), Lprev).astype(object).tolist()
        Lprev, Lcur = Lcur, nxt
    return [int(v) for v in Lcur]


def psi(d):
    """Minimal polynomial of 2cos(2 pi/d) over Q, integer coefficients,
    highest degree first.  Uses x^g Psi_d(x + 1/x) = Phi_d(x) with
    g = phi(d)/2, valid for d >= 3; Psi_1 = s - 2, Psi_2 = s + 2."""
    if d == 1:
        return [1, -2]
    if d == 2:
        return [1, 2]
    x = symbols("x")
    coeffs = Poly(cyclotomic_poly(d, x), x).all_coeffs()   # degree phi(d)
    deg = len(coeffs) - 1
    g = deg // 2
    assert deg == int(totient(d)) and deg % 2 == 0
    # Phi_d is palindromic: Phi_d(x)/x^g = c_0 + sum_{j=1}^{g} c_j (x^j + x^-j)
    asc = coeffs[::-1]                                     # ascending powers
    c = [int(asc[g])] + [int(asc[g + j]) for j in range(1, g + 1)]
    out = [0]
    for j, cj in enumerate(c):
        term = np.polymul([cj], lucas_poly(j)) if j else [cj * 2 // 2 * 1]
        if j == 0:
            term = [cj]
        out = np.polyadd(out, term).astype(object).tolist()
    return [int(v) for v in out]


def membership(F, k):
    """Is F in the family (s+a)L_k + alpha s + beta?  Returns
    (a, alpha, beta) as Fractions, or None."""
    Lk = lucas_poly(k)
    G = np.polysub(np.array(F, dtype=object),
                   np.polymul([1, 0], Lk).astype(object)).tolist()
    G = [Fraction(int(v)) for v in G]
    while len(G) > 1 and G[0] == 0:
        G.pop(0)
    degG = len(G) - 1
    if degG > k:
        return None
    Gp = [Fraction(0)] * (k + 1 - len(G)) + G           # pad to degree k
    a = Gp[0]
    rem = [x - a * Fraction(int(y)) for x, y in zip(Gp, [1] + [0] * 0 + Lk[1:])]
    rem = [Gp[i] - a * Fraction(int(Lk[i])) for i in range(k + 1)]
    if any(rem[i] != 0 for i in range(0, k - 1)):
        return None
    alpha, beta = rem[k - 1], rem[k]
    return a, alpha, beta


def build_matrix(n, k, a, alpha, c):
    """A in S(P(n,k)) with outer weight 1, inner weight 1, spoke weight c,
    outer diagonal a and inner diagonal alpha."""
    P = np.roll(np.eye(n), 1, axis=1)
    U = float(a) * np.eye(n) + (P + P.T)
    V = float(alpha) * np.eye(n) + (np.linalg.matrix_power(P, k)
                                    + np.linalg.matrix_power(P.T, k))
    C = float(c) * np.eye(n)
    return np.block([[U, C], [C, V]])


def build_matrix_int(n, k, a, alpha, c):
    """The same matrix over Z, for exact rank certification (requires a,
    alpha and c integral, which holds for every certificate reported)."""
    N = 2 * n
    A = [[0] * N for _ in range(N)]
    for i in range(n):
        A[i][(i + 1) % n] += 1
        A[(i + 1) % n][i] += 1
        A[i][n + i] += c
        A[n + i][i] += c
        A[n + i][n + (i + k) % n] += 1
        A[n + (i + k) % n][n + i] += 1
        A[i][i] = a
        A[n + i][n + i] = alpha
    return A


def exact_nullity(A):
    """Nullity over Q by exact Gaussian elimination with Fractions."""
    M = [[Fraction(v) for v in row] for row in A]
    rows, cols, rank = len(M), len(M[0]), 0
    for c in range(cols):
        sel = next((r for r in range(rank, rows) if M[r][c] != 0), None)
        if sel is None:
            continue
        M[rank], M[sel] = M[sel], M[rank]
        inv = Fraction(1) / M[rank][c]
        M[rank] = [x * inv for x in M[rank]]
        for r in range(rows):
            if r != rank and M[r][c] != 0:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[rank])]
        rank += 1
        if rank == rows:
            break
    return cols - rank


def off_diagonal_degrees(A, tol=1e-12):
    B = np.abs(A) > tol
    np.fill_diagonal(B, False)
    return B.sum(axis=1)


def check_membership_identity(F, k, a, alpha, beta):
    """Verify F == (s+a) L_k(s) + alpha s + beta exactly."""
    Lk = [Fraction(v) for v in lucas_poly(k)]
    lhs = [Fraction(v) for v in F]
    prod = [Fraction(0)] * (len(Lk) + 1)
    for i, cv in enumerate(Lk):                 # (s + a) * L_k
        prod[i] += cv
        prod[i + 1] += a * cv
    prod[-2] += alpha
    prod[-1] += beta
    return lhs == prod


def a_int_ok(r):
    """Are a and alpha integers, so the certificate matrix is integral?"""
    return r["a"].denominator == 1 and r["alpha"].denominator == 1


def scan(kmax=12, dmax=210, allow_pm2=True):
    results = []
    degs = {}
    for d in range(1, dmax + 1):
        degs[d] = 1 if d in (1, 2) else int(totient(d)) // 2
    for k in range(2, kmax + 1):
        target = k + 1
        pool = sorted(d for d in degs
                      if degs[d] <= target and (allow_pm2 or d > 2))
        # enumerate distinct-d sets by degree budget, pruning as we go: a
        # brute-force pass over all subsets is astronomically large by k ~ 10.
        subsets = []

        def rec(start, remaining, chosen):
            if remaining == 0:
                subsets.append(tuple(chosen))
                return
            for idx in range(start, len(pool)):
                d = pool[idx]
                if degs[d] > remaining:
                    continue
                chosen.append(d)
                rec(idx + 1, remaining - degs[d], chosen)
                chosen.pop()

        rec(0, target, [])
        for D in subsets:
            F = [1]
            for d in D:
                F = np.polymul(np.array(F, dtype=object),
                               np.array(psi(d), dtype=object)).tolist()
            F = [int(v) for v in F]
            mem = membership(F, k)
            if mem is None:
                continue
            a, alpha, beta = mem
            assert check_membership_identity(F, k, a, alpha, beta), (k, D)
            c2 = a * alpha - beta
            if c2 <= 0:
                continue
            interior = sum(degs[d] for d in D if d > 2)
            ends = sum(1 for d in D if d in (1, 2))
            results.append(dict(k=k, D=D, F=F, a=a, alpha=alpha, beta=beta,
                                c2=c2, nullity=2 * interior + ends,
                                modulus=int(np.lcm.reduce([max(d, 1)
                                                           for d in D]))))
    return results


if __name__ == "__main__":
    res = scan()
    print("Exact period-1 certificates from cyclotomic symbol polynomials")
    print("(only cases with nullity >= 2k are listed)\n")
    print(f"{'k':>3} {'2k+2':>5} {'nullity':>8} {'n | by':>8} "
          f"{'factors Psi_d':>22} {'a':>5} {'d':>5} {'c^2':>5}")
    best = {}
    for r in sorted(res, key=lambda r: (r["k"], -r["nullity"], r["modulus"])):
        if r["nullity"] < 2 * r["k"]:
            continue
        print(f"{r['k']:>3} {2*r['k']+2:>5} {r['nullity']:>8} "
              f"{r['modulus']:>8} {str(r['D']):>22} {str(r['a']):>5} "
              f"{str(r['alpha']):>5} {str(r['c2']):>5}")
        cur = best.get(r["k"])
        if cur is None or r["nullity"] > cur["nullity"] or (
                r["nullity"] == cur["nullity"] and r["modulus"] < cur["modulus"]):
            best[r["k"]] = r

    print("\nBest certificate for each k:")
    for k in sorted(best):
        r = best[k]
        verdict = ("= 2k+2, so Z(P(n,k)) = M(P(n,k)) = 2k+2 exactly"
                   if r["nullity"] == 2 * k + 2
                   else f"so Z(P(n,{k})) >= {r['nullity']}")
        print(f"  k={k}: nullity {r['nullity']} for every n divisible by "
              f"{r['modulus']}   ({verdict})")

    print("\nVerification on the least admissible n of each best case")
    print(f"{'graph':>10} {'nullity':>8} {'float':>6} {'exact':>6} "
          f"{'cubic':>6} {'gap':>9}")
    allok = True
    for k in sorted(best):
        r = best[k]
        n = r["modulus"]
        while n < 2 * k + 3 or 2 * k >= n:
            n += r["modulus"]
        csq = r["c2"]
        croot = Fraction(csq).limit_denominator()
        c_int = int(round(float(csq) ** 0.5))
        integral = (c_int * c_int == csq and a_int_ok(r))
        A = build_matrix(n, k, r["a"], r["alpha"], float(csq) ** 0.5)
        lam = np.sort(np.abs(np.linalg.eigvalsh(A)))
        got = int(np.sum(lam < 1e-9 * np.abs(A).max()))
        cubic = bool(np.all(off_diagonal_degrees(A) == 3))
        ex = "-"
        if integral:
            ex = exact_nullity(build_matrix_int(n, k, int(r["a"]),
                                                int(r["alpha"]), c_int))
        ok = (got == r["nullity"] and cubic
              and (ex == "-" or ex == r["nullity"]))
        allok &= ok
        print(f"{'P(%d,%d)'%(n,k):>10} {r['nullity']:>8} {got:>6} {str(ex):>6} "
              f"{str(cubic):>6} {lam[r['nullity']]:>9.2e}  "
              f"{'OK' if ok else 'MISMATCH'}")
    print("\nall best certificates verified:", "YES" if allok else "NO")
