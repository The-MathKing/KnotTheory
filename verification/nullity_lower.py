"""
Rigorous lower bounds on Z(P(n,k)) via maximum nullity.

Z(G) >= M(G) = max nullity over symmetric A with A_ij != 0 iff ij in E(G)
(i != j; diagonal free). So exhibiting ONE such A of nullity r proves Z >= r.

For P(n,k) take A equivariant under the rotation rho:
    outer block  U = a I + b (P + P^{-1})
    inner block  V = d I + e (P^k + P^{-k})
    spokes       C = c I                       (b, c, e nonzero: correct pattern)
P is the cyclic shift, so Fourier diagonalisation splits A into n blocks
    M_m = [[ a + b s_m , c ], [ c , d + e t_m ]],
    s_m = 2cos(2 pi m / n),  t_m = 2cos(2 pi k m / n).
Hence nullity(A) = #{ m : (a + b s_m)(d + e t_m) = c^2 }.

Setting b=1, the singular m are those whose point (s_m,t_m) lies on the curve
    t = A/(s + B) - C,        A = c^2/e,  B = a,  C = d/e,
a three-parameter family, so any three points can be fitted exactly. Points
with m and n-m coincide, so each fitted point contributes 2 to the nullity.
"""
import numpy as np
from itertools import combinations
from math import cos, pi, gcd


def points(n, k):
    s = [2*cos(2*pi*m/n) for m in range(n)]
    t = [2*cos(2*pi*k*m/n) for m in range(n)]
    return s, t


def fit_and_count(n, k, tol=1e-7):
    """Max nullity obtainable from a rho-equivariant matrix, with certificate.

    (a + b s)(d + e t) = c^2 with b=1 expands to
        e*(s t) + d*s + (a e)*t + (a d - c^2) = 0,
    linear and homogeneous in (e, d, ae, ad-c^2). Three distinct points
    determine the coefficient vector up to scale (nullspace of a 3x4 matrix);
    we then count every point satisfying it. Admissibility requires e != 0 and
    c^2 = (ae)(d)/e - (ad-c^2) > 0 so that c is real and nonzero.
    """
    s_, t_ = points(n, k)
    uniq = {}
    for m in range(n):
        uniq.setdefault((round(s_[m], 10), round(t_[m], 10)), []).append(m)
    keys = list(uniq)
    best, info = 0, None
    for tri in combinations(keys, 3):
        M = np.array([[sx*tx, sx, tx, 1.0] for (sx, tx) in tri])
        _, sv, Vt = np.linalg.svd(M)
        if sv[-1] > 1e-8 and M.shape[0] >= 4:
            continue
        v = Vt[-1]                      # nullspace vector (e, d, ae, ad-c^2)
        e_, d_, ae_, w_ = v
        if abs(e_) < 1e-9:
            continue
        a_ = ae_ / e_
        c2 = a_*d_ - w_
        if c2 <= 1e-9:                  # need c real and nonzero
            continue
        cnt, hit = 0, []
        for (sx, tx), ms in uniq.items():
            if abs(e_*sx*tx + d_*sx + ae_*tx + w_) < tol:
                cnt += len(ms); hit.append(((sx, tx), len(ms)))
        if cnt > best:
            best, info = cnt, dict(a=a_, b=1.0, c2=c2, d=d_, e=e_, hits=hit)
    return best, info


if __name__ == "__main__":
    known = {(10,2):6,(12,2):6,(14,2):6,(16,3):8,(18,3):8,(20,3):8,
             (18,4):10,(20,4):10,(24,4):10,(23,5):12,(24,5):12,(28,6):14}
    print(f"{'graph':>9} {'Z (exact)':>10} {'nullity LB':>11} {'gcd(n,k)':>9}  status")
    print("-"*52)
    for (n,k),Z in sorted(known.items()):
        lb,_ = fit_and_count(n,k)
        ok = "VALID" if lb<=Z else "*** EXCEEDS Z -- BUG ***"
        print(f"P({n},{k})".rjust(9)+f" {Z:>10} {lb:>11} {gcd(n,k):>9}  {ok}")
