"""
Lower bounds on Z(P(n,k)) from matrices commuting only with rho^d.

Relaxing equivariance from rho to rho^d (d | n) lets the entries vary with
period d: 5d parameters (outer diagonal, outer edge, spoke, inner diagonal,
inner edge, each a function of i mod d) instead of 5. We solve numerically for
parameters making as many blocks singular as possible, then VERIFY by building
the full 2n x 2n matrix, computing its nullity from eigenvalues, and checking
its off-diagonal zero pattern against E(P(n,k)). Only the verified nullity is
reported -- the solve is a search heuristic, the certificate is the proof.
"""
import numpy as np
from scipy.optimize import least_squares


def build(n, k, d, p):
    """p = [a_0..a_{d-1}, b_.., c_.., e_.., f_..] (period-d entries)."""
    a, b, c, e, f = (p[0:d], p[d:2*d], p[2*d:3*d], p[3*d:4*d], p[4*d:5*d])
    N = 2*n
    A = np.zeros((N, N))
    for i in range(n):
        r = i % d
        A[i, i] = a[r]
        A[n+i, n+i] = e[r]
        j = (i+1) % n
        A[i, j] += b[r]; A[j, i] += b[r]
        j2 = (i+k) % n
        A[n+i, n+j2] += f[r]; A[n+j2, n+i] += f[r]
        A[i, n+i] = c[r]; A[n+i, i] = c[r]
    return A


def pattern_ok(n, k, A, tol=1e-12):
    N = 2*n
    E = set()
    for i in range(n):
        E.add(frozenset((i, (i+1) % n)))
        E.add(frozenset((n+i, n+((i+k) % n))))
        E.add(frozenset((i, n+i)))
    for u in range(N):
        for v in range(u+1, N):
            if (frozenset((u, v)) in E) != (abs(A[u, v]) > tol):
                return False
    return True


def verified_nullity(n, k, d, p, tol=1e-7):
    A = build(n, k, d, p)
    if not pattern_ok(n, k, A):
        return -1, A
    ev = np.linalg.eigvalsh(A)
    return int(np.sum(np.abs(ev) < tol)), A


def search(n, k, d, target, tries=60, seed=0):
    """Try to reach nullity >= target; return best VERIFIED nullity."""
    rng = np.random.default_rng(seed)
    best, bestp = 0, None
    for _ in range(tries):
        p0 = rng.normal(size=5*d)
        p0[d:2*d]  = np.abs(p0[d:2*d])  + 0.5     # b nonzero
        p0[2*d:3*d]= np.abs(p0[2*d:3*d])+ 0.5     # c nonzero
        p0[4*d:5*d]= np.abs(p0[4*d:5*d])+ 0.5     # f nonzero

        def resid(p):
            A = build(n, k, d, p)
            ev = np.linalg.eigvalsh(A)
            idx = np.argsort(np.abs(ev))[:target]   # push `target` eigenvalues to 0
            return ev[idx]

        try:
            sol = least_squares(resid, p0, max_nfev=4000)
        except Exception:
            continue
        p = sol.x
        # keep the pattern legal: reject if any required entry collapsed
        if (np.min(np.abs(p[d:2*d])) < 1e-6 or np.min(np.abs(p[2*d:3*d])) < 1e-6
                or np.min(np.abs(p[4*d:5*d])) < 1e-6):
            continue
        nul, _ = verified_nullity(n, k, d, p)
        if nul > best:
            best, bestp = nul, p
    return best, bestp


if __name__ == "__main__":
    known = {(12,2):6,(14,2):6,(18,3):8,(20,3):8,(18,4):10,(20,4):10,
             (24,5):12,(28,6):14}
    print(f"{'graph':>9} {'Z':>3} {'d=1':>5} {'d=2':>5} {'d=4':>5}  (verified nullity)")
    print("-"*46)
    for (n,k),Z in sorted(known.items()):
        row=[]
        for d in (1,2,4):
            if n % d: row.append("-"); continue
            b,_ = search(n,k,d,target=min(Z, 5*d+2), tries=25, seed=1)
            row.append(str(b))
        flag = "" if all(r=="-" or int(r)<=Z for r in row) else " *** EXCEEDS Z"
        print(f"P({n},{k})".rjust(9)+f" {Z:>3} {row[0]:>5} {row[1]:>5} {row[2]:>5}{flag}")
