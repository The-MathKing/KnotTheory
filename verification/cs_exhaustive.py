"""Exhaustive enumeration of rational period-one symbols, in the LARGER class.

Proposition prop:exh enumerated rational symbols attaining 2k+2 and required
c^2 = a alpha - beta > 0, the condition for a SYMMETRIC certificate.  In the
combinatorially symmetric class the two spoke weights are independent and need
only have product c^2, so the condition weakens to c^2 != 0.  And

    c^2 = 0  <=>  beta = a alpha  <=>  F = (s+a) L_k(s) + alpha (s+a)
             <=>  F = (s+a)(L_k(s) + t)   for some constant t,

an exact characterisation, one line, valid for every k.  The antipodal
obstruction of thm:antipodal is the special case forced by parity when k is
even.  This script redoes the enumeration with the weaker condition.
"""
import itertools
import sympy as sp

s = sp.symbols("s")


def L(k):
    a, b = sp.Integer(2), s
    for _ in range(k - 1):
        a, b = b, sp.expand(s * b - a)
    return b


def psi(d):
    if d == 1: return s - 2
    if d == 2: return s + 2
    return sp.expand(sp.minimal_polynomial(2 * sp.cos(2 * sp.pi / d), s))


def deg(d):
    return 1 if d <= 2 else sp.totient(d) // 2


def analyse(k, D, Lk):
    F = sp.Integer(1)
    for d in D: F *= psi(d)
    F = sp.Poly(sp.expand(F), s)
    if F.degree() != k + 1: return None
    G = sp.Poly(sp.expand(F.as_expr() - s * Lk), s)
    a = G.coeff_monomial(s**k)
    H = sp.Poly(sp.expand(G.as_expr() - a * Lk), s)
    if H.degree() > 1: return ("outside", None, None, None)
    al, be = H.coeff_monomial(s), H.coeff_monomial(1)
    c2 = sp.simplify(a * al - be)
    # cross-check the factorisation characterisation of c2 = 0
    fac = sp.simplify(sp.expand(F.as_expr() - (s + a) * (Lk + al))) == 0
    assert (c2 == 0) == fac, (D, c2, fac)
    return ("inside", a, al, c2)


print(__doc__)
print("all Psi_d are used with every root interior, so each contributes 2 to the")
print("nullity; D must have sum of degrees k+1 and every d >= 3 to reach 2k+2.\n")
rows = []
for k in range(2, 11):
    Lk = L(k)
    cap = k + 1
    adm = [d for d in range(3, 200) if deg(d) <= cap]
    cand = ins = pos = neg = zero = 0
    hits = []
    # DFS over increasing d with pruning on the running degree sum: the naive
    # itertools.combinations over ~30 admissible d up to size k+1 is ~6e6 sets
    # at k=7 and does not finish.
    sets = []
    degs = [(d, int(deg(d))) for d in adm]
    def dfs(i, acc, tot):
        if tot == k + 1:
            sets.append(tuple(acc)); return
        if i == len(degs) or tot > k + 1: return
        d, dg = degs[i]
        if tot + dg <= k + 1:
            acc.append(d); dfs(i + 1, acc, tot + dg); acc.pop()
        dfs(i + 1, acc, tot)
    dfs(0, [], 0)
    for D in sets:
        if True:
            res = analyse(k, D, Lk)
            if res is None: continue
            cand += 1
            if res[0] == "outside": continue
            ins += 1
            a, al, c2 = res[1], res[2], res[3]
            if c2 == 0: zero += 1
            elif c2 > 0: pos += 1; hits.append((D, a, al, c2, "sym"))
            else: neg += 1; hits.append((D, a, al, c2, "cs"))
    lcms = sorted({int(sp.lcm(list(h[0]))) for h in hits})
    rows.append((k, cand, ins, zero, pos, neg, lcms))
    print(f"k = {k}   ceiling 2k+2 = {2*k+2}")
    print(f"  candidate factor sets of total degree {k+1}: {cand}")
    print(f"    outside the 3-parameter family : {cand - ins}")
    print(f"    inside, c^2 = 0 (dead, = (s+a)(L_k+t)) : {zero}")
    print(f"    inside, c^2 > 0 (SYMMETRIC certificate): {pos}")
    print(f"    inside, c^2 < 0 (cs certificate ONLY)  : {neg}")
    for D, a, al, c2, cls in sorted(hits, key=lambda h: int(sp.lcm(list(h[0])))):
        print(f"      D={str(D):16s} a={str(a):4s} alpha={str(al):4s} "
              f"c^2={str(c2):4s} [{cls}]  ->  every n divisible by "
              f"{int(sp.lcm(list(D)))}")
    if not hits:
        print("      none: no rational period-one symbol attains 2k+2, in either class")
    print()

print("=" * 72)
print(" k  ceiling  sym certs  cs-only certs  attained n (lcm)")
for k, cand, ins, zero, pos, neg, lcms in rows:
    print(f"{k:3d}{2*k+2:9d}{pos:11d}{neg:15d}  {lcms if lcms else '--'}")
