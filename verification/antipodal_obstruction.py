"""The antipodal obstruction.

The period-one symbol is F(s) = (s+a)L_k(s) + alpha s + beta, and the
certificate is admissible only if c^2 = a alpha - beta is nonzero (any sign in
the combinatorially symmetric class, positive in the symmetric one).

THEOREM (parity).  Since L_k(-s) = (-1)^k L_k(s): if k is EVEN and F has two
roots y, -y with y != 0, then subtracting the two root conditions gives
alpha = -L_k(y) and adding them gives beta = -a L_k(y), so

    c^2 = a alpha - beta = -a L_k(y) + a L_k(y) = 0

identically.  So for even k a period-one symbol may have NO antipodal pair of
roots.  For odd k the same elimination gives beta = -y L_k(y) and
alpha = -a L_k(y)/y, hence c^2 = L_k(y)(y^2-a^2)/y, and there is no obstruction.

For k = 2 the symbol has exactly three roots and no residual conditions, so the
criterion is closed-form: matching coefficients gives c^2 = e3 - e1 e2, and by
the elementary identity (s1+s2)(s1+s3)(s2+s3) = e1 e2 - e3,

    c^2 = -(s1+s2)(s1+s3)(s2+s3).

So c^2 = 0 exactly when two roots are antipodal -- a factorisation, not an
observation -- and c^2 > 0 exactly when an odd number of the pairwise sums is
negative.

COROLLARY (which cyclotomic symbols are excluded for even k).  The roots of
Psi_{2d} are the negatives of the roots of Psi_d for odd d, and the root set of
Psi_d is closed under negation when 4 | d and phi(d) >= 4.  So for even k the
factor set D may not contain both d and 2d for any odd d, nor any d divisible
by 4 with phi(d) >= 4.  This script checks that prediction against every
candidate D, and confirms that every such D has c^2 EXACTLY zero.
"""
import itertools
import sympy as sp

s = sp.symbols("s")

def L(k):
    if k == 0: return sp.Integer(2)
    a, b = sp.Integer(2), s
    for _ in range(k - 1):
        a, b = b, sp.expand(s * b - a)
    return b if k >= 1 else a

def psi(d):
    if d == 1: return sp.Poly(s - 2, s)
    if d == 2: return sp.Poly(s + 2, s)
    return sp.Poly(sp.minimal_polynomial(2 * sp.cos(2 * sp.pi / d), s), s)

def has_antipodal_pair(D):
    """Psi_e(-s) = +- Psi_{e'}(s); detect a shared root up to sign exactly by
    checking whether Psi_d(s) and Psi_e(-s) have a nontrivial common factor."""
    for d, e in itertools.combinations_with_replacement(D, 2):
        if d == e and D.count(d) < 2 and d == e:
            # a single factor can still be self-antipodal (e.g. Psi_8 = s^2-2)
            g = sp.gcd(psi(d).as_expr(), sp.expand(psi(d).as_expr().subs(s, -s)))
            if sp.Poly(g, s).degree() >= 1 and sp.Poly(psi(d), s).degree() >= 2:
                return True
            continue
        g = sp.gcd(psi(d).as_expr(), sp.expand(psi(e).as_expr().subs(s, -s)))
        if sp.Poly(g, s).degree() >= 1:
            return True
    return False

def c2_of_D(k, D):
    F = sp.Integer(1)
    for d in D: F *= psi(d).as_expr()
    F = sp.Poly(sp.expand(F), s)
    if F.degree() != k + 1: return None
    G = sp.Poly(sp.expand(F.as_expr() - s * L(k)), s)
    a = G.coeff_monomial(s**k)
    H = sp.Poly(sp.expand(G.as_expr() - a * L(k)), s)
    if H.degree() > 1: return "family"
    al, be = H.coeff_monomial(s), H.coeff_monomial(1)
    return sp.simplify(a * al - be)

print(__doc__)
print("check L_k(-s) = (-1)^k L_k(s):",
      all(sp.expand(L(k).subs(s, -s) - (-1)**k * L(k)) == 0 for k in range(1, 11)))

print("\nSYMBOLIC c^2 with a prescribed antipodal pair {y,-y} and a third root x:")
x, y = sp.symbols("x y", positive=True)
for k in range(2, 9):
    a, al, be = sp.symbols("a alpha beta")
    Lk = L(k)
    eqs = [sp.Eq(a * Lk.subs(s, r) + al * r + be, -r * Lk.subs(s, r))
           for r in (x, y, -y)]
    sol = sp.solve(eqs, [a, al, be], dict=True)
    v = sp.simplify(sol[0][a] * sol[0][al] - sol[0][be]) if sol else None
    z = (v == 0)
    print(f"  k={k} ({'even' if k%2==0 else 'odd '}):  c^2 "
          f"{'= 0  (obstructed)' if z else '!= 0  (no obstruction)'}"
          f"   {'' if z else '  ' + str(sp.factor(v))[:70]}")

print("\nk=2 CLOSED FORM")
r1, r2, r3 = sp.symbols("r1 r2 r3")
a, al, be = sp.symbols("a alpha beta")
sol = sp.solve([sp.Eq(a*(r**2-2) + al*r + be, -r*(r**2-2)) for r in (r1, r2, r3)],
               [a, al, be], dict=True)[0]
c2 = sp.simplify(sol[a]*sol[al] - sol[be])
print("  c^2 + (r1+r2)(r1+r3)(r2+r3) =",
      sp.simplify(c2 + (r1+r2)*(r1+r3)*(r2+r3)))

print("\nCOROLLARY: candidate cyclotomic factor sets for even k")
print("  k  D                  antipodal?  c^2              prediction")
adm = {2: [1,2,3,4,5,6,7,8,9,10,12,14,18],
       4: [1,2,3,4,5,6,7,8,9,10,11,12,14,15,16,18,20,22,24,30]}
viol = tested = 0
for k in (2, 4):
    for rr in (1, 2, 3):
        for D in itertools.combinations(adm[k], rr):
            v = c2_of_D(k, D)
            if v is None or v == "family": continue
            ap = has_antipodal_pair(list(D)); tested += 1
            ok = (not ap) or v == 0
            viol += (not ok)
            if ap or rr <= 2:
                print(f"  {k}  {str(D):19s}{'YES' if ap else 'no ':12s}"
                      f"{str(v):17s}{'ok' if ok else 'VIOLATION'}")
print(f"\n{tested} factor sets in the 3-parameter family tested; "
      f"violations of the prediction: {viol}")
