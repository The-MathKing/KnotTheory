"""The k=3 certificate: F = Psi_5 Psi_10 = s^4 - 3 s^2 + 1.

Psi_5 = s^2+s-1 and Psi_10 = s^2-s-1, so F = s^4-3s^2+1 = s*L_3(s) + 1, giving
a = 0, alpha = 0, beta = 1 and c^2 = a*alpha - beta = -1.  Negative, so there is
no symmetric certificate; in the combinatorially symmetric class the two spoke
weights need only multiply to -1, so take them to be 1 and -1:

    A = [[ P + P^-1 ,  I ], [ -I , P^3 + P^-3 ]]

an integer matrix, zero diagonal -- the adjacency matrix of P(n,3) with one set
of spokes negated.  Its four symbol roots are +-phi and +-1/phi, i.e. TWO
antipodal pairs, which would force c^2 = 0 if k were even.  k = 3 is odd, so by
the parity theorem there is no obstruction, and the nullity is 2k+2 = 8 for
every n divisible by 10.
"""
import subprocess
import numpy as np
import sympy as sp

s = sp.symbols("s")
p5 = sp.expand(sp.minimal_polynomial(2 * sp.cos(2 * sp.pi / 5), s))
p10 = sp.expand(sp.minimal_polynomial(2 * sp.cos(2 * sp.pi / 10), s))
F = sp.expand(p5 * p10)
L3 = s**3 - 3 * s
print(f"Psi_5 = {p5}    Psi_10 = {p10}")
print(f"F = Psi_5 * Psi_10 = {F}")
print(f"F - s*L_3 = {sp.expand(F - s*L3)}   =>  a = 0, alpha = 0, beta = 1, c^2 = -1")
print(f"roots of F: {[sp.radsimp(r) for r in sp.Poly(F, s).all_roots()]}")
print(f"root set closed under negation: "
      f"{sp.expand(F.subs(s, -s) - F) == 0}  (two antipodal pairs)")
print()


def build(n, k=3):
    P = np.roll(np.eye(n), 1, axis=0)
    U = P + P.T
    V = np.linalg.matrix_power(P, k) + np.linalg.matrix_power(P.T, k)
    return np.block([[U, np.eye(n)], [-np.eye(n), V]])


def pattern_ok(A, n, k=3):
    Adj = np.zeros((2 * n, 2 * n), int)
    for i in range(n):
        Adj[i, (i+1) % n] = Adj[(i+1) % n, i] = 1
        Adj[i, n+i] = Adj[n+i, i] = 1
        Adj[n+i, n+(i+k) % n] = Adj[n+(i+k) % n, n+i] = 1
    patt = (np.abs(A) > 1e-12).astype(int)
    np.fill_diagonal(patt, 0)
    return np.array_equal(patt, Adj)


print("A = [[P+P^-1, I], [-I, P^3+P^-3]]   integer, pattern exactly P(n,3)")
print("    n   nullity  pattern  next singular value   Z(P(n,3))  verdict")
bad = []
for n in (10, 20, 30, 40, 50, 60, 70, 80, 90, 100):
    A = build(n)
    sv = np.linalg.svd(A, compute_uv=False)
    nul = int(np.sum(sv < 1e-9 * sv.max()))
    ok = pattern_ok(A, n)
    Z = None
    if n <= 20:                       # exhaustive Z is only tractable here
        Z = int(subprocess.run(["/Volumes/2TB/scifair/src/zero_forcing/c/zf",
                                str(n), "3", "9"], capture_output=True,
                               text=True).stdout.split("Z=")[1].split()[0])
    good = (nul == 8 and ok and Z in (8, None))
    if not good: bad.append(n)
    print(f"{n:5d}{nul:9d}   {str(ok):6s}{sv[-9]:20.6f}"
          f"{str(Z) if Z else '     (too large)':>11s}   {'OK' if good else 'FAIL'}")

print("\nexact check of the nullity via the symbol, for the same n")
print("  null A = 2 * #{m : F(2cos(2 pi m/n)) = 0, 0 < m < n/2} and every root")
print("  of F is a root of Psi_5 or Psi_10, so it is on the grid iff 10 | n.")
for n in (10, 20, 30, 7, 12, 15):
    cnt = sum(1 for m in range(0, n)
              if abs(float(F.subs(s, 2 * np.cos(2 * np.pi * m / n)))) < 1e-9)
    A = build(n)
    sv = np.linalg.svd(A, compute_uv=False)
    print(f"  n={n:4d}  grid roots counted with multiplicity: {cnt:2d}"
          f"   numerical nullity: {int(np.sum(sv < 1e-9*sv.max())):2d}"
          f"   {'match' if cnt == int(np.sum(sv < 1e-9*sv.max())) else 'MISMATCH'}")

print("\nnon-example: the UNSIGNED adjacency matrix (both spokes +1) has c^2=+1,")
print("so its symbol is s*L_3 - 1, a different polynomial:")
for n in (10, 20, 30):
    P = np.roll(np.eye(n), 1, axis=0)
    A = np.block([[P + P.T, np.eye(n)],
                  [np.eye(n), np.linalg.matrix_power(P, 3) + np.linalg.matrix_power(P.T, 3)]])
    sv = np.linalg.svd(A, compute_uv=False)
    print(f"  n={n}: nullity {int(np.sum(sv < 1e-9*sv.max()))}")

print("\nfailures:", bad or "none")
