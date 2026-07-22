"""
Algebraic d=2 certificates:  Z(P(n,k)) >= nullity, n even, k even.

With A commuting with rho^2, entries have period 2 (a_r, b_r, c_r, e_r, f_r).
Fourier over Z/m, m=n/2, gives m Hermitian 4x4 blocks. With k=2*kappa the
inner block is diagonal, and

    det M = (a_0 v_0 - c_0^2)(a_1 v_1 - c_1^2) - |beta|^2 v_0 v_1,
    v_r = e_r + f_r w,   w = 2cos(2 pi kappa l/m),
    |beta|^2 = b_0^2 + b_1^2 + 2 b_0 b_1 x,   x = cos(2 pi l/m).

Singularity is therefore  (x + mu) N(w) = L(w)  with N,L quadratic in w and
mu = (b_0^2+b_1^2)/(2 b_0 b_1). Expanded in the monomials
(x, xw, xw^2, 1, w, w^2) this is linear and homogeneous in six coefficients, so
FIVE points determine it, versus three for d=1.

Realisability: |mu| >= 1 by AM-GM (b_0,b_1 real), N and L must factor over the
reals, and the recovered c_r^2 must be positive. Everything is then verified on
the full 2n x 2n matrix.
"""
import numpy as np
from itertools import combinations
from math import cos, pi
from verification.nullity_period import build, pattern_ok


def pts(n, k):
    m, kap = n//2, k//2
    return [(cos(2*pi*l/m), 2*cos(2*pi*kap*l/m)) for l in range(m)]


def recover(coef, mu):
    """coef = (G,H,K, muG-L0, muH-L1, muK-L2) -> parameters or None."""
    G, H, K, d0, d1, d2 = coef
    if abs(K) < 1e-9:
        return None
    L0, L1, L2 = mu*G - d0, mu*H - d1, mu*K - d2
    # b from mu:  t^2 - 2 mu t + 1 = 0,  t = b0/b1
    if abs(mu) < 1.0:
        return None
    t = mu + np.sqrt(mu*mu - 1.0)
    b1 = 1.0; b0 = t*b1
    scale = 2*b0*b1
    # factor N(w) = K w^2 + H w + G = (f0 w + e0)(f1 w + e1)
    disc = H*H - 4*K*G
    if disc < 0:
        return None
    r1 = (-H + np.sqrt(disc))/(2*K); r2 = (-H - np.sqrt(disc))/(2*K)
    f0, f1 = 1.0, K
    e0, e1 = -r1, -K*r2
    # factor scale*L'(w) = L(w) = (Q w + P)(S w + R)
    LK, LH, LG = L2*scale, L1*scale, L0*scale
    if abs(LK) < 1e-12:
        return None
    dl = LH*LH - 4*LK*LG
    if dl < 0:
        return None
    s1 = (-LH + np.sqrt(dl))/(2*LK); s2 = (-LH - np.sqrt(dl))/(2*LK)
    Q, S = 1.0, LK
    P, R = -s1, -LK*s2
    a0 = Q/f0; a1 = S/f1
    c0sq = a0*e0 - P; c1sq = a1*e1 - R
    if c0sq <= 1e-9 or c1sq <= 1e-9:
        return None
    return np.array([a0, a1, b0, b1, np.sqrt(c0sq), np.sqrt(c1sq),
                     e0, e1, f0, f1])


def try_fit(n, k, tol=1e-7):
    P = pts(n, k)
    uniq = {}
    for l, (x, w) in enumerate(P):
        uniq.setdefault((round(x, 10), round(w, 10)), []).append(l)
    keys = list(uniq)
    if len(keys) < 5:
        return 0, None
    best, bestp = 0, None
    for five in combinations(keys, 5):
        M = np.array([[x, x*w, x*w*w, 1.0, w, w*w] for (x, w) in five])
        _, sv, Vt = np.linalg.svd(M)
        v = Vt[-1]
        G, H, K = v[0], v[1], v[2]
        d0, d1, d2 = v[3], v[4], v[5]
        for mu in (1.0, 1.05, 1.25, 1.6, 2.0, 3.0, 5.0, -1.05, -1.6, -3.0):
            p = recover((G, H, K, d0, d1, d2), mu)
            if p is None:
                continue
            # reorder to build()'s layout: a_r, b_r, c_r, e_r(inner diag), f_r
            pp = np.array([p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9]])
            A = build(n, k, 2, pp)
            if not pattern_ok(n, k, A):
                continue
            sc = np.max(np.abs(A))
            if min(abs(p[2]), abs(p[3]), abs(p[4]), abs(p[5]),
                   abs(p[8]), abs(p[9])) < 0.02*sc:
                continue
            ev = np.sort(np.abs(np.linalg.eigvalsh(A)))
            nul = int(np.sum(ev < 1e-9*sc))
            if 0 < nul < len(ev) and ev[nul] < 1e5*ev[nul-1]:
                continue
            if nul > best:
                best, bestp = nul, pp
    return best, bestp


if __name__ == "__main__":
    known = {(12,2):6,(14,2):6,(18,4):10,(20,4):10,(24,4):10,(28,6):14,(24,6):12}
    print(f"{'graph':>9} {'Z':>3} {'d=1 (prev)':>11} {'d=2 (new)':>10}  status")
    print("-"*46)
    prev = {(12,2):6,(14,2):6,(18,4):6,(20,4):6,(24,4):6,(28,6):6,(24,6):6}
    for (n,k),Z in sorted(known.items()):
        b,_ = try_fit(n,k)
        st = "VALID" if b<=Z else "*** EXCEEDS Z"
        gain = "  <-- improves" if b > prev.get((n,k),0) else ""
        print(f"P({n},{k})".rjust(9)+f" {Z:>3} {prev.get((n,k),0):>11} {b:>10}  {st}{gain}",flush=True)
