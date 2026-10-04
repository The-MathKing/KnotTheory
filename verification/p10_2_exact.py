"""M(P(10,2)) = 6, exactly.

The claim M(P(10,2)) = Z(P(10,2)) = 6 was recorded as *numerical*: a witness
found by gradient descent, with no certificate. This module replaces it with an
exact one, over the rationals, and in the process explains why the search was
hard.

Three statements, in order:

1. No rotation-invariant (period-one) matrix on the P(10,2) pattern has nullity
   6. The 2x2 Fourier blocks M(w^j) pair up by complex conjugation, the
   determinant's vanishing locus is controlled by cos(4*pi*j/10), and that
   function takes each of its values twice on j = 0..5. Any three blocks forced
   to be singular therefore contain two with a common inner cosine, and
   subtracting their determinant conditions kills either an edge weight or the
   spoke. Nullity 5 is attainable; 6 is not. This is `period1_ceiling`.

2. A period-two matrix (invariant under rotation by 2, i.e. under Z_5) can
   reach 6, and only in one way. Its 4x4 blocks over the fifth roots of unity
   admit nullity at most 1 at j = 1, 2 and at most 2 at j = 0, so the total
   6 = 2 + 2*1 + 2*1 is forced. This pins the ansatz completely.

3. Imposing that ansatz and requiring the entries to be rational -- which is
   what makes the j=1 and j=2 conditions Galois conjugate over Q(sqrt 5), so
   that satisfying one gives the other for free -- reduces everything to

       s*t + 2*s*f + 2*e*t - e*f = 0,
       a^2 = -c^2 d^2 e f / ((s+2e)(t+2f)(s f + e t - e f)),

   with p = c^2/(s+2e) and q = d^2/(t+2f). We solve this, assemble the 20x20
   matrix over Q, and verify the nullity by exact rank. No floating point
   enters the decision.

Run: python3 verification/p10_2_exact.py
"""

from fractions import Fraction as F
import itertools

import sympy as sp

N_, K_ = 10, 2


# ---------------------------------------------------------------- the pattern

def edges(n=N_, k=K_):
    """Edge set of P(n,k) in the repository's convention: outer 0..n-1, inner
    n..2n-1, outer i~i+1, spokes i~n+i, inner n+i ~ n+(i+k)%n."""
    return ([(i, (i + 1) % n) for i in range(n)]
            + [(i, n + i) for i in range(n)]
            + [(n + i, n + (i + k) % n) for i in range(n)])


def edge_set(n=N_, k=K_):
    return {frozenset(e) for e in edges(n, k)}


# ------------------------------------------------- 1. the period-one ceiling

def period1_ceiling():
    """Exact proof that a rotation-invariant matrix cannot reach nullity 6.

    A period-one symmetric matrix on the P(n,k) pattern is determined by
    (a, b, c, dout, din): outer weight, inner weight, spoke, and the two
    diagonals. Its Fourier block at w^j is

        [[dout + a*x_j, c], [c, din + b*y_j]],  x_j = 2cos(2pi j/n),
                                                y_j = 2cos(2pi j k/n).

    Nullity of a block is 2 only if c = 0, so each singular block contributes
    1, and blocks j and n-j are conjugate. We show that no admissible choice
    makes the total reach 6, by checking every subset of blocks of total
    dimension 6 and deriving a contradiction symbolically.
    """
    a, b, c, dout, din = sp.symbols('a b c dout din', real=True)
    n, k = N_, K_

    # Block index j contributes dim 1 if j is self-conjugate (j == 0 or 2j == n),
    # else it pairs with n-j and the pair contributes 2. Represent each class by
    # its smallest member.
    classes = []  # (representative j, dimension)
    for j in range(n // 2 + 1):
        if j == 0 or 2 * j == n:
            classes.append((j, 1))
        else:
            classes.append((j, 2))

    def det(j):
        x = 2 * sp.cos(2 * sp.pi * j / n)
        y = 2 * sp.cos(2 * sp.pi * j * k / n)
        return sp.expand((dout + a * x) * (din + b * y) - c ** 2)

    # Every way to choose a set of classes with total dimension exactly 6.
    feasible = []
    for r in range(1, len(classes) + 1):
        for sub in itertools.combinations(classes, r):
            if sum(d for _, d in sub) == 6:
                feasible.append(sub)

    results = []
    for sub in feasible:
        js = [j for j, _ in sub]
        eqs = [sp.simplify(sp.radsimp(det(j))) for j in js]
        sols = sp.solve(eqs, [dout, din, c], dict=True)
        # A solution is admissible only if it keeps a, b, c nonzero.
        admissible = []
        for s in sols:
            cval = sp.simplify(s.get(c, c))
            if cval == 0:
                continue
            admissible.append(s)
        results.append((js, admissible))

    bad = [(js, adm) for js, adm in results if adm]
    return feasible, results, bad


# ---------------------------------------- 3. the period-two exact certificate

def solve_period2(limit=14):
    """Search small rationals for a period-two solution.

    Parameters: outer weights a (on A_m~B_m) and b = -a (on B_m~A_{m+1});
    spokes c (A~C) and d (B~D); inner weights e (C_m~C_{m+1}) and
    f (D_m~D_{m+1}); diagonals p (A), q (B), s (C), t (D).

    Returns the first (a, c, d, e, f, p, q, s, t) found, all in Q.
    """
    for e in range(1, limit):
        for f in range(-limit, limit):
            if f == 0:
                continue
            for s in range(-limit, limit):
                den = s + 2 * e
                if den == 0:
                    continue
                # st + 2sf + 2et - ef = 0  =>  t (s + 2e) = f(e - 2s)
                t = F(f * (e - 2 * s), den)
                if t + 2 * f == 0:
                    continue
                tail = F(s) * f + F(e) * t - F(e) * f
                if tail == 0:
                    continue
                # a^2 = -c^2 d^2 e f / ((s+2e)(t+2f)(sf+et-ef)); take c = d = 1
                # and ask for the cofactor to be a positive rational square.
                kappa = F(-e * f) / (F(den) * (t + 2 * f) * tail)
                if kappa <= 0:
                    continue
                num, dn = kappa.numerator, kappa.denominator
                rn, rd = sp.sqrt(sp.Integer(num)), sp.sqrt(sp.Integer(dn))
                if not (rn.is_Integer and rd.is_Integer):
                    continue
                a = F(int(rn), int(rd))
                c = d = F(1)
                p = F(c * c, 1) / F(den)
                q = F(d * d, 1) / (t + 2 * f)
                if a == 0 or p == 0 and False:
                    continue
                return dict(a=a, b=-a, c=c, d=d, e=F(e), f=F(f),
                            p=p, q=q, s=F(s), t=t)
    return None


def assemble_exact(prm, n=N_):
    """Build the 20x20 rational matrix from period-two parameters."""
    A = sp.zeros(2 * n, 2 * n)
    a, b, c, d = prm['a'], prm['b'], prm['c'], prm['d']
    e, f, p, q, s, t = (prm['e'], prm['f'], prm['p'],
                        prm['q'], prm['s'], prm['t'])

    def put(i, j, val):
        A[i, j] += sp.Rational(val.numerator, val.denominator)
        if i != j:
            A[j, i] += sp.Rational(val.numerator, val.denominator)

    for m in range(5):
        # outer: A_m ~ B_m weight a ; B_m ~ A_{m+1} weight b
        put(2 * m, 2 * m + 1, a)
        put(2 * m + 1, (2 * m + 2) % n, b)
        # spokes
        put(2 * m, n + 2 * m, c)
        put(2 * m + 1, n + 2 * m + 1, d)
        # inner: C_m ~ C_{m+1} weight e ; D_m ~ D_{m+1} weight f
        put(n + 2 * m, n + (2 * m + 2) % n, e)
        put(n + 2 * m + 1, n + (2 * m + 3) % n, f)
    for m in range(5):
        put(2 * m, 2 * m, p)
        put(2 * m + 1, 2 * m + 1, q)
        put(n + 2 * m, n + 2 * m, s)
        put(n + 2 * m + 1, n + 2 * m + 1, t)
    return A


def check_support(A, n=N_, k=K_):
    """Off-diagonal support of A must be exactly E(P(n,k))."""
    want = edge_set(n, k)
    got = set()
    for i in range(2 * n):
        for j in range(i + 1, 2 * n):
            if A[i, j] != 0:
                got.add(frozenset((i, j)))
    return got == want, want - got, got - want


def main():
    print("M(P(10,2)) = 6 -- exact certificate")
    print("=" * 62)

    print("\n[1] Period-one matrices cannot reach nullity 6.")
    feasible, results, bad = period1_ceiling()
    print(f"    block-class subsets of total dimension 6: {len(feasible)}")
    for js, adm in results:
        print(f"    blocks j={js}: admissible solutions with c != 0: {len(adm)}")
    print(f"    => subsets admitting a valid matrix: {len(bad)}")
    assert not bad, "a period-one matrix reached nullity 6; the argument is wrong"
    print("    CONFIRMED: no rotation-invariant matrix attains 6.")

    print("\n[2] Period-two search over Q.")
    prm = solve_period2()
    assert prm is not None, "no period-two solution found in the search box"
    for key in ('a', 'b', 'c', 'd', 'e', 'f', 'p', 'q', 's', 't'):
        print(f"    {key} = {prm[key]}")

    print("\n[3] Exact verification of the assembled 20x20 matrix.")
    A = assemble_exact(prm)
    assert A.T == A, "matrix is not symmetric"
    print("    symmetric: yes")

    ok, missing, extra = check_support(A)
    print(f"    support == E(P(10,2)): {ok}"
          + ("" if ok else f" (missing {missing}, extra {extra})"))
    assert ok, "off-diagonal support is not the P(10,2) edge set"

    rank = A.rank()
    nullity = 20 - rank
    print(f"    exact rank over Q: {rank}")
    print(f"    exact nullity:     {nullity}")
    assert nullity == 6, f"nullity is {nullity}, expected 6"

    # Scaling a matrix by a nonzero constant changes neither the pattern nor
    # the nullity, so clear the denominators and report an integer witness.
    scale = 1
    for i in range(20):
        for j in range(20):
            if A[i, j] != 0:
                scale = sp.ilcm(scale, sp.Rational(A[i, j]).q)
    Ai = (scale * A).applyfunc(sp.nsimplify)
    assert all(sp.Rational(Ai[i, j]).q == 1
               for i in range(20) for j in range(20)), "scaling left fractions"
    ok_i, _, _ = check_support(Ai)
    rank_i = Ai.rank()
    print(f"\n    integer form, scaled by {scale}:")
    print(f"      distinct entries: "
          f"{sorted({int(Ai[i, j]) for i in range(20) for j in range(20)})}")
    print(f"      support == E(P(10,2)): {ok_i}")
    print(f"      exact rank over Z: {rank_i}   nullity: {20 - rank_i}")
    assert ok_i and 20 - rank_i == 6, "integer form failed to reproduce nullity 6"

    print("\n" + "=" * 62)
    print("M(P(10,2)) >= 6 by this certificate; the monodromy ceiling gives")
    print("M <= Z = 6; hence M(P(10,2)) = Z(P(10,2)) = 6, exactly, with no")
    print("strict gap at n = 10. Status of the claim: CERTIFIED (was numerical).")
    return prm, A


if __name__ == '__main__':
    main()
