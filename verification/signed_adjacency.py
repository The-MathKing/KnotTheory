"""The signed adjacency matrix of P(n,k), and an infinite-family question.

The k=3 and k=7 certificates both have a = alpha = 0 and beta = 1, i.e. symbol
F = s L_k(s) + 1.  That is not a coincidence: a = alpha = 0 means both diagonals
vanish, so the matrix is

    A = [[ P + P^-1 , I ], [ -I , P^k + P^-k ]]

the adjacency matrix of P(n,k) with one set of spokes negated.  Substituting
s = z + 1/z and L_k = z^k + z^-k and clearing denominators,

    F(s) = 0   <=>   Q_k(z) := z^(2k+2) + z^(2k) + z^(k+1) + z^2 + 1 = 0,

which is exactly the adjacency polynomial P_k(z) = z^(2k+2) + z^(2k) - z^(k+1)
+ z^2 + 1 of thm:adjclass with the sign of the middle term flipped -- the spoke
sign flip.  So by the same argument as thm:adjclass,

    null(signed Adj P(n,k)) = sum of phi(d) over d with Phi_d | Q_k and d | n,

and the nullity attains the ceiling 2k+2 exactly when Q_k is a product of
cyclotomic polynomials.  This script decides that for each k.
"""
import numpy as np
import sympy as sp

z = sp.symbols("z")


def Q(k, sign=+1):
    return sp.Poly(z**(2*k+2) + z**(2*k) + sign*z**(k+1) + z**2 + 1, z)


def cyclotomic_factorisation(poly):
    """Return the list of d with Phi_d | poly (with multiplicity), or None if
    poly is not a product of cyclotomics."""
    ds = []
    for f, m in sp.factor_list(poly.as_expr())[1]:
        fp = sp.Poly(f, z).monic()
        d = None
        for dd in range(1, 4 * poly.degree() + 8):
            if sp.totient(dd) == fp.degree() and \
               sp.expand(fp.as_expr() - sp.cyclotomic_poly(dd, z)) == 0:
                d = dd; break
        if d is None:
            return None
        ds += [d] * m
    return sorted(ds)


print(__doc__)
print("Q_k(z) = z^(2k+2) + z^(2k) + z^(k+1) + z^2 + 1   (SIGNED spokes)")
print("  k  deg  product of cyclotomics?   d's            sum phi(d)   lcm(d)")
hits = []
for k in range(2, 61):
    q = Q(k)
    ds = cyclotomic_factorisation(q)
    if ds is None:
        continue
    tot = sum(int(sp.totient(d)) for d in ds)
    lc = int(sp.lcm(ds))
    hits.append((k, ds, tot, lc))
    print(f"{k:3d}{q.degree():5d}   YES                     {str(ds):15s}"
          f"{tot:9d}{lc:9d}   {'CEILING' if tot == 2*k+2 else ''}")
print(f"\nk in 2..60 for which Q_k is a product of cyclotomics: "
      f"{[h[0] for h in hits]}")

print("\nfor contrast, the UNSIGNED P_k(z) = ... - z^(k+1) + ... (thm:adjclass)")
for k in range(2, 31):
    ds = cyclotomic_factorisation(Q(k, -1))
    if ds is not None:
        tot = sum(int(sp.totient(d)) for d in ds)
        print(f"  k={k:3d}  d's {str(ds):15s} sum phi = {tot}"
              f"  lcm = {int(sp.lcm(ds))}  {'CEILING' if tot == 2*k+2 else ''}")

print("\nnumerical confirmation: nullity of the signed matrix")
def nul(n, k):
    P = np.roll(np.eye(n), 1, axis=0)
    A = np.block([[P + P.T, np.eye(n)],
                  [-np.eye(n), np.linalg.matrix_power(P, k)
                   + np.linalg.matrix_power(P.T, k)]])
    sv = np.linalg.svd(A, compute_uv=False)
    return int(np.sum(sv < 1e-9 * sv.max()))
print("    k   lcm   n      predicted   actual")
for k, ds, tot, lc in hits:
    for mult in (1, 2):
        n = lc * mult
        if 2 * k >= n or 2 * n > 400: continue
        print(f" {k:4d}{lc:6d}{n:5d}{tot:13d}{nul(n, k):9d}"
              f"   {'OK' if nul(n,k) == tot else 'FAIL'}")
