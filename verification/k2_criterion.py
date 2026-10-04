"""Verify Theorem (k=2, all n): the explicit certificate at the three most
negative grid values, checked against exhaustively computed Z(P(n,2)).

For each n the theorem prescribes roots s_M, s_{M-1}, s_{M-2} with
M = floor((n-1)/2), sets a = -e1, alpha = e2+2, beta = -e3-2e1, c = sqrt(c^2)
with c^2 = -(s1+s2)(s1+s3)(s2+s3), and claims nullity exactly 6 whenever
c^2 > 0, which happens for odd n >= 9 and even n >= 12.  For 7 | n the
combinatorially symmetric integer matrix with spoke weights 1 and -1 does it
instead.  This script builds both and counts nullity numerically.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import subprocess
import numpy as np

ZF = f"{_REPO}/src/zero_forcing/c/zf"


def true_Z(n):
    out = subprocess.run([ZF, str(n), "2", "8"], capture_output=True, text=True).stdout
    return int(out.split("Z=")[1].split()[0])


def nullity(a, alpha, c, cprime, n):
    P = np.roll(np.eye(n), 1, axis=0)
    U = a * np.eye(n) + P + P.T
    V = alpha * np.eye(n) + np.linalg.matrix_power(P, 2) + np.linalg.matrix_power(P.T, 2)
    A = np.block([[U, c * np.eye(n)], [cprime * np.eye(n), V]])
    sv = np.linalg.svd(A, compute_uv=False)
    return int(np.sum(sv < 1e-9 * sv.max())), A


def pattern_ok(A, n):
    Adj = np.zeros((2 * n, 2 * n), int)
    for i in range(n):
        Adj[i, (i + 1) % n] = Adj[(i + 1) % n, i] = 1
        Adj[i, n + i] = Adj[n + i, i] = 1
        Adj[n + i, n + (i + 2) % n] = Adj[n + (i + 2) % n, n + i] = 1
    patt = (np.abs(A) > 1e-12).astype(int)
    np.fill_diagonal(patt, 0)
    return np.array_equal(patt, Adj)


print("  n   M   c^2 (3 most negative)   null   pattern   symbolic c^2 check"
      "   Z(P(n,2))   agree")
bad = []
for n in range(5, 41):
    M = (n - 1) // 2
    Z = true_Z(n) if 2 * n <= 128 else None
    if M < 3:
        print(f"{n:3d}{M:4d}   fewer than 3 interior values                       "
              f"                     {Z}")
        continue
    v = [2 * np.cos(2 * np.pi * j / n) for j in (M, M - 1, M - 2)]
    c2 = -(v[0] + v[1]) * (v[0] + v[2]) * (v[1] + v[2])
    # closed form must agree with e3 - e1 e2
    e1 = sum(v); e2 = v[0]*v[1] + v[0]*v[2] + v[1]*v[2]; e3 = v[0]*v[1]*v[2]
    chk = abs(c2 - (e3 - e1 * e2)) < 1e-12
    # and with the predicted trigonometric form
    pred = (-4 * np.cos(4 * np.pi / n) * np.cos(np.pi / n) if n % 2 else
            -4 * np.cos(5 * np.pi / n) * np.cos(np.pi / n))
    chk = chk and abs(pred - (v[1] + v[2])) < 1e-12
    if c2 <= 1e-12:
        print(f"{n:3d}{M:4d}{c2:+22.9f}      --   --        {'ok' if chk else 'BAD'}"
              f"                   {Z}      (no symmetric certificate)")
        continue
    a, alpha = -e1, e2 + 2
    nul, A = nullity(a, alpha, np.sqrt(c2), np.sqrt(c2), n)
    ok = (nul == 6) and pattern_ok(A, n) and (Z == 6 if Z else True)
    if not ok: bad.append(n)
    print(f"{n:3d}{M:4d}{c2:+22.9f}{nul:8d}   {str(pattern_ok(A,n)):7s}   "
          f"{'ok' if chk else 'BAD':18s}{Z if Z else '-':>9}      "
          f"{'yes' if ok else 'NO'}")

print("\nthe cs certificate for 7 | n  (a=1, alpha=0, spokes 1 and -1)")
for n in (7, 14, 21, 28, 35):
    nul, A = nullity(1.0, 0.0, 1.0, -1.0, n)
    Z = true_Z(n) if 2 * n <= 128 else None
    okp = pattern_ok(A, n)
    print(f"  P({n},2): nullity {nul}   pattern {okp}   Z = {Z}"
          f"   {'ok' if nul == 6 and okp and (Z in (6, None)) else 'NO'}")
    if not (nul == 6 and okp and Z in (6, None)): bad.append(n)

print("\nexhaustive Z for the exceptional n")
for n in (5, 6, 8, 10):
    print(f"  Z(P({n},2)) = {true_Z(n)}")
print("\nfailures:", bad or "none")
