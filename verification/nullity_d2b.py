"""
d=2 certificates, fitting FOUR points instead of five.

Fitting five points determines the curve uniquely and, empirically, always
forces a spoke weight c_r^2 <= 0 -- i.e. the outer and inner halves decouple
and the matrix leaves S(G). Fitting four leaves a one-parameter pencil
alpha*v1 + beta*v2 of admissible curves, and we search the pencil for a member
whose recovered parameters are realisable (c_r^2 > 0, all required entries
nonzero). Four points give eight singular blocks, versus six for d=1.
"""
import numpy as np
from itertools import combinations
from math import cos, pi
from verification.nullity_d2 import pts, recover
from verification.nullity_period import build, pattern_ok


def try_fit(n, k, ngrid=400):
    P = pts(n, k)
    uniq = {}
    for l, (x, w) in enumerate(P):
        uniq.setdefault((round(x, 10), round(w, 10)), []).append(l)
    keys = list(uniq)
    if len(keys) < 4:
        return 0, None
    best, bestp = 0, None
    for four in combinations(keys, 4):
        M = np.array([[x, x*w, x*w*w, 1.0, w, w*w] for (x, w) in four])
        _, sv, Vt = np.linalg.svd(M)
        v1, v2 = Vt[-1], Vt[-2]          # 2-dim nullspace
        for th in np.linspace(0, np.pi, ngrid, endpoint=False):
            v = np.cos(th)*v1 + np.sin(th)*v2
            for mu in (1.02, 1.15, 1.4, 1.8, 2.5, 4.0, -1.15, -1.8, -2.5):
                p = recover((v[0], v[1], v[2], v[3], v[4], v[5]), mu)
                if p is None:
                    continue
                A = build(n, k, 2, p)
                if not pattern_ok(n, k, A):
                    continue
                sc = np.max(np.abs(A))
                if min(abs(p[2]), abs(p[3]), abs(p[4]), abs(p[5]),
                       abs(p[8]), abs(p[9])) < 0.02*sc:
                    continue
                ev = np.sort(np.abs(np.linalg.eigvalsh(A)))
                nul = int(np.sum(ev < 1e-9*sc))
                if nul == 0:
                    continue
                if nul < len(ev) and ev[nul] < 1e5*ev[nul-1]:
                    continue
                if nul > best:
                    best, bestp = nul, p.copy()
    return best, bestp


if __name__ == "__main__":
    known = {(12,2):6,(14,2):6,(18,4):10,(20,4):10,(24,4):10,(24,6):12,(28,6):14}
    prev  = {(12,2):6,(14,2):6,(18,4):6,(20,4):6,(24,4):6,(24,6):6,(28,6):6}
    print(f"{'graph':>9} {'Z':>3} {'d=1':>5} {'d=2':>5}  status")
    print("-"*40)
    for (n,k),Z in sorted(known.items()):
        b,_ = try_fit(n,k)
        st = "VALID" if b<=Z else "*** EXCEEDS Z"
        gain = "  <-- IMPROVES" if b > prev[(n,k)] else ""
        print(f"P({n},{k})".rjust(9)+f" {Z:>3} {prev[(n,k)]:>5} {b:>5}  {st}{gain}",flush=True)
