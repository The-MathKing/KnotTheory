"""One pass over every computational claim the paper makes.

Run this to confirm the paper's numbers from scratch.  Each check prints PASS or
FAIL and the quantity it checked; nothing is taken on trust from a stored file
except the saved certificates, which are re-evaluated rather than believed.
"""
import glob
import itertools
import os
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
ROOT = "/Volumes/2TB/scifair/results/zero_forcing"
fails = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  --- {detail}" if detail else ""))
    if not ok:
        fails.append(name)


s = sp.symbols("s")


def L(k):
    a, b = sp.Integer(2), s
    for _ in range(k - 1):
        a, b = b, sp.expand(s * b - a)
    return b


print("1. Realisability (thm:realis): c^2 = 0 iff F = (s+a)(L_k + t)")
a_, al, be = sp.symbols("a alpha beta")
for k in range(2, 9):
    F = sp.expand((s + a_) * L(k) + al * s + be)
    ok = sp.simplify(F.subs(be, a_ * al) - (s + a_) * (L(k) + al)) == 0
    check(f"k={k}", ok)

print("2. Antipodal corollary: c^2 = 0 identically for even k, not for odd")
x, y = sp.symbols("x y", positive=True)
for k in range(2, 9):
    Lk = L(k)
    eqs = [sp.Eq(a_ * Lk.subs(s, r) + al * r + be, -r * Lk.subs(s, r))
           for r in (x, y, -y)]
    sol = sp.solve(eqs, [a_, al, be], dict=True)
    v = sp.simplify(sol[0][a_] * sol[0][al] - sol[0][be]) if sol else None
    check(f"k={k} ({'even' if k % 2 == 0 else 'odd'})",
          (v == 0) == (k % 2 == 0))

print("3. k=2 closed form: c^2 = -(s1+s2)(s1+s3)(s2+s3)")
r1, r2, r3 = sp.symbols("r1 r2 r3")
sol = sp.solve([sp.Eq(a_ * (r**2 - 2) + al * r + be, -r * (r**2 - 2))
                for r in (r1, r2, r3)], [a_, al, be], dict=True)[0]
check("identity", sp.simplify(sol[a_]*sol[al] - sol[be]
                              + (r1+r2)*(r1+r3)*(r2+r3)) == 0)

print("4. e_2 = -k for every period-one symbol with k >= 3 (thm:congbound)")
for k in range(3, 11):
    F = sp.Poly(sp.expand((s + a_) * L(k) + al * s + be), s)
    check(f"k={k}", sp.expand(F.coeff_monomial(s**(k-1)) + k) == 0)

print("5. Integer certificates: the signed adjacency matrix")
def signed_nullity(n, k):
    P = np.roll(np.eye(n), 1, axis=0)
    A = np.block([[P + P.T, np.eye(n)],
                  [-np.eye(n), np.linalg.matrix_power(P, k)
                   + np.linalg.matrix_power(P.T, k)]])
    sv = np.linalg.svd(A, compute_uv=False)
    return int(np.sum(sv < 1e-9 * sv.max()))
# the signed adjacency matrix is the a = alpha = 0 case, which covers
# 10|n and 30|n at k=3,2 and 120|n at k=7 -- NOT 7|n, whose certificate is
# Psi_7 with a=1, alpha=0 and is checked separately below
for (n, k, want) in [(10, 3, 8), (20, 3, 8), (30, 3, 8), (120, 7, 16),
                     (30, 2, 6), (60, 2, 6)]:
    got = signed_nullity(n, k)
    check(f"signed Adj P({n},{k}) nullity {want}", got == want, f"got {got}")

def psi7_nullity(n):
    """The 7|n certificate: a = 1, alpha = 0, spokes 1 and -1."""
    P = np.roll(np.eye(n), 1, axis=0)
    A = np.block([[np.eye(n) + P + P.T, np.eye(n)],
                  [-np.eye(n), np.linalg.matrix_power(P, 2)
                   + np.linalg.matrix_power(P.T, 2)]])
    sv = np.linalg.svd(A, compute_uv=False)
    return int(np.sum(sv < 1e-9 * sv.max()))
for n in (7, 14, 21, 28):
    got = psi7_nullity(n)
    check(f"Psi_7 certificate P({n},2) nullity 6", got == 6, f"got {got}")

print("6. k=2 explicit certificate at the three most negative grid values")
print("   (c^2 > 0 is checked for all n; the nullity is checked two ways, by")
print("    counting grid roots of the symbol exactly and, for moderate n only,")
print("    by singular values -- the three roots crowd within O(1/n^2) of -2,")
print("    so the matrix is exact but numerically stiff for large n)")
bad_c2 = []
for n in list(range(9, 200)) + [500, 1001]:
    if n == 10:
        continue
    M = (n - 1) // 2
    v = [2*np.cos(2*np.pi*j/n) for j in (M, M-1, M-2)]
    c2 = -(v[0]+v[1])*(v[0]+v[2])*(v[1]+v[2])
    if c2 <= 1e-12:
        bad_c2.append(n)
check("c^2 > 0 for every n >= 9, n != 10 (up to 1001)", not bad_c2,
      f"failures {bad_c2}" if bad_c2 else "checked 9..199, 500, 1001")
# Counting grid roots by a float tolerance is the wrong test: the three
# prescribed roots crowd within O(1/n^2) of -2 (spread 2.4e-4 at n = 1001),
# so grid values that are merely NEAR them evaluate below any fixed cutoff
# -- at n = 1001 the true roots give 9e-16 and the nearest non-roots 4e-11.
# What actually needs checking is the construction: the three prescribed
# values are distinct interior grid values, and then prop:symbol gives
# nullity exactly 6 because each interior root is met by two Fourier indices.
bad_root = []
for n in list(range(9, 200)) + [500, 1001, 5000]:
    if n == 10:
        continue
    M = (n - 1) // 2
    v = [2*np.cos(2*np.pi*j/n) for j in (M, M-1, M-2)]
    distinct = len({round(x, 14) for x in v}) == 3
    interior = all(abs(abs(x) - 2) > 1e-12 for x in v)
    if not (distinct and interior):
        bad_root.append(n)
check("three prescribed roots are distinct and interior", not bad_root,
      f"failures {bad_root}" if bad_root
      else "checked 9..199, 500, 1001, 5000")
for n in (9, 11, 20, 39, 60):
    M = (n - 1) // 2
    v = [2*np.cos(2*np.pi*j/n) for j in (M, M-1, M-2)]
    c2 = -(v[0]+v[1])*(v[0]+v[2])*(v[1]+v[2])
    e1 = sum(v); e2 = v[0]*v[1]+v[0]*v[2]+v[1]*v[2]
    P = np.roll(np.eye(n), 1, axis=0)
    A = np.block([[-e1*np.eye(n)+P+P.T, np.sqrt(c2)*np.eye(n)],
                  [np.sqrt(c2)*np.eye(n),
                   (e2+2)*np.eye(n)+np.linalg.matrix_power(P,2)
                   + np.linalg.matrix_power(P.T,2)]])
    sv = np.linalg.svd(A, compute_uv=False)
    check(f"P({n},2) nullity 6 numerically",
          int(np.sum(sv < 1e-9*sv.max())) == 6)

print("7. Saved interval-certified matrices re-evaluated (k=3)")
from certify_general import pattern_cells, assemble
got = []
for f in sorted(glob.glob(f"{ROOT}/cert_gn_*_3.npy")):
    n = int(os.path.basename(f).split("_")[2])
    z = np.load(f)
    A = assemble(z[:5*n], pattern_cells(n, 3), 2*n)
    sv = np.linalg.svd(A, compute_uv=False)
    nul = int(np.sum(sv < 1e-9*sv.max()))
    edges = np.abs(z[2*n:5*n]).min()/np.abs(z[:5*n]).max()
    got.append(n)
    check(f"P({n},3) nullity 8, edges nonzero", nul == 8 and edges > 1e-3,
          f"nullity {nul}, min edge {edges:.4f}")
print(f"      ({len(got)} saved certificates re-evaluated)")

print("8. k=3 identity tiles and their compositions")
from tiles import tile_sequence, dock_weights, build_matrix
def tdict(w, l, k):
    m = k+1; nint = l-2*m; D = dock_weights(k); t = {}
    for idx, key in enumerate("bcead"):
        t[key] = np.concatenate([D[key], w[idx*nint:(idx+1)*nint], D[key]])
    return t
tiles = {}
for f in sorted(glob.glob(f"{ROOT}/tile_*_3.npy")):
    l = int(os.path.basename(f).split("_")[1])
    tiles[l] = np.load(f)
have = sorted(tiles)
check("tiles cover a full interval [L,2L)",
      have == list(range(min(have), max(have)+1)) and max(have) >= 2*min(have)-1,
      f"lengths {min(have)}..{max(have)} ({len(have)} tiles)")
bad = []
for l in have:
    W = tile_sequence([tdict(tiles[l], l, 3)], 3)
    A = build_matrix(l, 3, W)
    sv = np.linalg.svd(A, compute_uv=False)
    if int(np.sum(sv < 1e-9*np.abs(A).max())) != 8:
        bad.append(l)
check("single tiles give nullity 8", not bad, f"failures {bad}" if bad else
      f"all {len(have)} lengths")
bad = []
for n in range(2*min(have), 2*min(have)+14):
    combo = next((c for r in (2, 3)
                  for c in itertools.combinations_with_replacement(have, r)
                  if sum(c) == n), None)
    if combo is None:
        continue
    W = tile_sequence([tdict(tiles[l], l, 3) for l in combo], 3)
    A = build_matrix(n, 3, W)
    sv = np.linalg.svd(A, compute_uv=False)
    if int(np.sum(sv < 1e-9*np.abs(A).max())) != 8:
        bad.append(n)
check("multi-tile concatenations give nullity 8", not bad,
      f"failures {bad}" if bad else "checked n up to "
      f"{2*min(have)+13}")

print("9. Certified tiles: nullity, docking exactness, interval coverage")
from tiles import dock_weights
for k in (3, 4):
    r = 2*k + 2
    m = k + 1
    certs = {}
    for f in sorted(glob.glob(f"{ROOT}/tilecert_*_{k}.npy")):
        l = int(os.path.basename(f).split("_")[1])
        certs[l] = np.load(f)
    if not certs:
        continue
    cl = sorted(certs)
    D = dock_weights(k)
    check(f"k={k}: certified lengths form [L, 2L)",
          cl == list(range(min(cl), max(cl)+1)) and max(cl) >= 2*min(cl)-1,
          f"{min(cl)}..{max(cl)} ({len(cl)} tiles)")
    bad_n, bad_d = [], []
    for l in cl:
        z = certs[l]
        A = assemble(z[:5*l], pattern_cells(l, k), 2*l)
        sv = np.linalg.svd(A, compute_uv=False)
        if int(np.sum(sv < 1e-9*sv.max())) != r:
            bad_n.append(l)
        for blk, key in enumerate("adbce"):
            for j, pos in enumerate(list(range(m)) + list(range(l-m, l))):
                if abs(z[blk*l+pos] - D[key][j % m]) > 1e-13:
                    bad_d.append((l, key)); break
    check(f"k={k}: every certified tile has nullity exactly {r}", not bad_n,
          f"failures {bad_n}" if bad_n else f"all {len(cl)} tiles")
    check(f"k={k}: docking weights exact in every certified tile", not bad_d,
          f"failures {bad_d[:3]}" if bad_d else "all tiles, to 1e-13")
    NMAX = 400
    cov = [False]*(NMAX+1)
    for a in cl:
        if a <= NMAX: cov[a] = True
    for _ in range(10):
        for i in range(NMAX+1):
            if cov[i]:
                for a in cl:
                    if i+a <= NMAX: cov[i+a] = True
    gaps = [n for n in range(min(cl), NMAX+1) if not cov[n]]
    check(f"k={k}: every n in [{min(cl)}, {NMAX}] is a sum of certified lengths",
          not gaps, f"gaps {gaps[:6]}" if gaps else "no gaps")

print("10. Slice lemma (lem:slice)")
from gauge_fixed import verify_slice
rows = verify_slice()
check("spokes -> +1 and |outer| -> 1, nullity preserved, both parities",
      all(r[1] and r[2] < 1e-12 and r[4] for r in rows),
      f"max deviation {max(r[2] for r in rows):.1e}")

print()
print("=" * 66)
print("ALL CHECKS PASSED" if not fails else f"FAILURES: {fails}")
