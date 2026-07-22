"""
Lower bounds on Z(P(n,k)) from rho^d-equivariant matrices, via block Fourier.

Index vertices by i = q*d + r. rho^d acts as q -> q+1, so Fourier over
Z/(n/d) splits A into n/d Hermitian blocks of size 2d, one per
zeta = exp(2 pi i l / (n/d)):

  U(zeta)[r,r+1] = b_r   (r < d-1),   U(zeta)[d-1,0] = b_{d-1} * zeta
  V(zeta)[r,r'] += f_r * zeta^{q'}    where r+k = q'*d + r'
  spokes C = diag(c_r);  diagonals a_r (outer), e_r (inner)

nullity(A) = sum_l nullity(M(zeta_l)). We drive chosen block determinants to
zero, then VERIFY on the full matrix (eigenvalues + zero pattern).
"""
import numpy as np
from scipy.optimize import least_squares
from verification.nullity_period import build, pattern_ok


def blocks(n, k, d, p):
    a, b, c, e, f = p[0:d], p[d:2*d], p[2*d:3*d], p[3*d:4*d], p[4*d:5*d]
    m = n // d
    out = []
    for l in range(m):
        z = np.exp(2j*np.pi*l/m)
        U = np.zeros((d, d), complex); V = np.zeros((d, d), complex)
        for r in range(d):
            U[r, r] = a[r]; V[r, r] = e[r]
        for r in range(d):
            if d == 1:
                U[0, 0] += b[0]*z + np.conj(b[0]*z)
            elif r < d-1:
                U[r, r+1] += b[r]; U[r+1, r] += b[r]
            else:
                U[d-1, 0] += b[d-1]*z; U[0, d-1] += np.conj(b[d-1]*z)
            rp, qp = (r+k) % d, (r+k)//d
            val = f[r]*(z**qp)
            V[r, rp] += val; V[rp, r] += np.conj(val)
        C = np.diag(c.astype(complex))
        out.append(np.block([[U, C], [C, V]]))
    return out


def nullity_from_blocks(n, k, d, p, tol=1e-7):
    return sum(int(np.sum(np.abs(np.linalg.eigvalsh(M)) < tol))
               for M in blocks(n, k, d, p))


def search(n, k, d, target, tries=40, seed=0):
    rng = np.random.default_rng(seed)
    m = n // d
    best, bestp = 0, None
    for _ in range(tries):
        p0 = rng.normal(size=5*d)
        for sl in (slice(d, 2*d), slice(2*d, 3*d), slice(4*d, 5*d)):
            p0[sl] = np.abs(p0[sl]) + 0.5
        tgt = rng.choice(m, size=min(target, m), replace=False)

        def resid(p):
            Bs = blocks(n, k, d, p)
            out = []
            for l in tgt:
                ev = np.linalg.eigvalsh(Bs[l])
                out.append(ev[np.argmin(np.abs(ev))])
            return np.array(out)

        try:
            sol = least_squares(resid, p0, max_nfev=1500)
        except Exception:
            continue
        p = sol.x
        A = build(n, k, d, p)
        if not pattern_ok(n, k, A):
            continue
        scale = np.max(np.abs(A))
        # Required-nonzero entries must be bounded away from 0 RELATIVE to the
        # matrix scale. Otherwise the optimiser shrinks an edge weight toward 0,
        # numerically deleting that edge and manufacturing fake zero eigenvalues.
        if min(np.min(np.abs(p[d:2*d])), np.min(np.abs(p[2*d:3*d])),
               np.min(np.abs(p[4*d:5*d]))) < 0.05*scale:
            continue
        ev = np.sort(np.abs(np.linalg.eigvalsh(A)))
        nul = int(np.sum(ev < 1e-9*scale))
        # demand a clear spectral gap: the first nonzero must exceed the last
        # "zero" by many orders of magnitude, else the count is not meaningful
        if 0 < nul < len(ev) and not (ev[nul] > 1e5*max(ev[nul-1], 1e-300)):
            continue
        if nul > best:
            best, bestp = nul, p
    return best, bestp


if __name__ == "__main__":
    import sys
    known = {(12,2):6,(14,2):6,(18,3):8,(20,3):8,(18,4):10,(20,4):10,
             (24,5):12,(28,6):14}
    print(f"{'graph':>9} {'Z':>3} {'d=1':>5} {'d=2':>5} {'d=4':>5}   verified nullity")
    print("-"*50)
    for (n,k),Z in sorted(known.items()):
        row=[]
        for d in (1,2,4):
            if n % d: row.append("-"); continue
            b,_=search(n,k,d,target=min(Z,5*d+2),tries=15,seed=3)
            row.append(str(b))
        bad = any(r!="-" and int(r)>Z for r in row)
        print(f"P({n},{k})".rjust(9)+f" {Z:>3} {row[0]:>5} {row[1]:>5} {row[2]:>5}"
              + ("   *** EXCEEDS Z (BUG)" if bad else ""),flush=True)
