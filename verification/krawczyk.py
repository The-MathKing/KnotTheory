"""Rigorous existence proof for a nullity-(2k+2) matrix on P(n,k).

The system f(z) = A(w) K(X) = 0 is BILINEAR in z = (w, X), so f is quadratic,
its Jacobian J is affine in z, and the Lipschitz constant of J is an explicit
integer.  That makes the Krawczyk test computable from three norms instead of an
interval matrix product:

  with  Y ~ J(z0)^{-1},  delta the box radius,
        alpha = ||I - Y J(z0)||_inf + ||Y||_inf * L * delta
  if    alpha < 1   and   ||Y f(z0)||_inf + alpha * delta <= delta
  then  K(B) is contained in the interior of B = z0 + [-delta, delta]^m,
  so f has a (unique) true zero in B.

Choosing WHICH 244 equations is not free.  A K = 0 is 272 equations of rank 244,
and the 28 dependencies are structural: K^T A K is automatically symmetric
because A is symmetric, and 28 = C(8,2) is exactly its antisymmetric part.
Concretely, with K in graph form and P = perm, if the 208 equations on the
non-pivot rows P[r:] vanish then K^T A K equals the r x r block (A K)[P[:r]],
which must therefore be symmetric; so setting its upper triangle to zero
(36 equations) forces the lower triangle too.  The square system

    208 equations  (A K)[P[r+m], t] = 0        (all non-pivot rows)
  +  36 equations  (A K)[P[s], t] = 0, s <= t  (upper triangle of the pivot block)

is therefore EXACTLY equivalent to A K = 0, not merely a rank-244 selection of
it.  Picking rows by QR pivoting instead would leave 28 equations unproved.

L bound: for row (i,t) of f, d/dw_j is nonzero only for the <= 4 weights whose
cells touch row i (one diagonal and three edges), each contributing at most 2
entries of K; and d/dX[m,t'] is nonzero only for the <= 4 columns adjacent to i.
So ||J(z1) - J(z2)||_inf <= 12 ||z1 - z2||_inf, and we use L = 12.

A zero of f gives A(w) K = 0 with K of graph form, hence rank K = 2k+2 exactly,
hence null A >= 2k+2.  With cor:ceiling giving null A <= 2k+2, the nullity is
exactly 2k+2, so M(P(n,k)) = Z(P(n,k)) = 2k+2.
"""
import sys
from fractions import Fraction

import numpy as np
import scipy.linalg as sla
from mpmath import mp, mpf, matrix as mpm

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from certify_general import pattern_cells, assemble, graph_form, build_K, jac

L_LIP = 12


def load(n, k):
    wg = np.load(f"/Volumes/2TB/scifair/results/zero_forcing/w_{n}_{k}.npy")
    b, c, e = wg[:n], wg[n:2*n], wg[2*n:3*n]
    a, d = wg[3*n:4*n], wg[4*n:5*n]
    return np.concatenate([a, d, b, c, e])


def resid_mp(z, cells, perm, N, r, nw):
    w = z[:nw]; X = z[nw:]
    Ac = [[mpf(0)] * N for _ in range(N)]
    for j, (_, cl) in enumerate(cells):
        for (i, l) in cl: Ac[i][l] = w[j]
    Kr = [[mpf(0)] * r for _ in range(N)]
    for t, p in enumerate(perm[:r]): Kr[p][t] = mpf(1)
    for m, p in enumerate(perm[r:]):
        for t in range(r): Kr[p][t] = X[m * r + t]
    out = []
    for i in range(N):
        for t in range(r):
            acc = mpf(0)
            for l in range(N):
                if Ac[i][l] != 0: acc += Ac[i][l] * Kr[l][t]
            out.append(acc)
    return out


def main():
    n, k = int(sys.argv[1]), int(sys.argv[2])
    digits = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    mp.dps = 60
    N, r = 2 * n, 2 * k + 2
    cells = pattern_cells(n, k)
    nw = len(cells)
    w = load(n, k)
    A = assemble(w, cells, N)
    K0 = np.linalg.svd(A)[2][-r:].T
    perm, X = graph_form(K0, r)
    z0 = np.concatenate([w, X.ravel()])
    J = jac(w, X, cells, perm, N, r)
    sv = np.linalg.svd(J, compute_uv=False)
    rk = int(np.sum(sv > 1e-8 * sv.max()))
    # STRUCTURAL choice of equations (see the module docstring): all non-pivot
    # rows, plus the upper triangle of the pivot block.  Equation index for
    # (row i, kernel column t) is i*r + t.
    eqs = [perm[r + m] * r + t for m in range(N - r) for t in range(r)]
    eqs += [perm[s] * r + t for s in range(r) for t in range(r) if s <= t]
    excess = [perm[s] * r + t for s in range(r) for t in range(r) if s > t]
    eqs = sorted(eqs)
    assert len(eqs) == rk, (len(eqs), rk)
    assert len(eqs) + len(excess) == N * r
    _, _, Pc = sla.qr(J[eqs], pivoting=True)
    free = sorted(Pc[:rk]); fixed = sorted(Pc[rk:])
    print(f"P({n},{k}): {len(z0)} unknowns, {N*r} equations, Jacobian rank {rk}")
    print(f"  square system: {rk} equations x {rk} unknowns; "
          f"{len(fixed)} unknowns FIXED at exact rationals "
          f"(denominator 10^{digits})")

    # fix the non-free unknowns at exact rationals
    zf = [Fraction(round(float(z0[i]) * 10**digits), 10**digits) for i in fixed]
    zcur = [mpf(z0[i]) for i in range(len(z0))]
    for i, v in zip(fixed, zf):
        zcur[i] = mpf(v.numerator) / mpf(v.denominator)

    # high-precision Newton on the square system
    for it in range(80):
        F = resid_mp(zcur, cells, perm, N, r, nw)
        zn = np.array([float(x) for x in zcur])
        Jn = jac(zn[:nw], zn[nw:].reshape(N - r, r), cells, perm, N, r)
        Js = Jn[np.ix_(eqs, free)]
        Fs = np.array([float(F[i]) for i in eqs])
        step = np.linalg.solve(Js, -Fs)
        for idx, s in zip(free, step):
            zcur[idx] = zcur[idx] + mpf(s)
        if np.abs(Fs).max() < mpf(10) ** (-45): break
    F = resid_mp(zcur, cells, perm, N, r, nw)
    fmax = max(abs(F[i]) for i in eqs)
    fexc = max(abs(F[i]) for i in excess)
    print(f"  Newton: max|f| on the {len(eqs)} structural equations = "
          f"{mp.nstr(fmax, 5)}")
    print(f"          max|f| on the {len(excess)} DEPENDENT equations = "
          f"{mp.nstr(fexc, 5)}  (implied, not solved for)")

    zn = np.array([float(x) for x in zcur])
    Jn = jac(zn[:nw], zn[nw:].reshape(N - r, r), cells, perm, N, r)
    Js = Jn[np.ix_(eqs, free)]
    Y = np.linalg.inv(Js)
    Ynorm = np.abs(Y).sum(axis=1).max()
    Fs = np.array([float(F[i]) for i in eqs])
    eta = np.abs(Y @ Fs).max()
    R = np.eye(rk) - Y @ Js
    alpha0 = np.abs(R).sum(axis=1).max()
    print(f"  ||Y||_inf = {Ynorm:.4e}   ||I - Y J||_inf = {alpha0:.4e}   "
          f"||Y f||_inf = {eta:.4e}")
    ok = False
    for delta in [10**p for p in range(-12, 0)]:
        alpha = alpha0 + Ynorm * L_LIP * delta
        if alpha < 1 and eta + alpha * delta <= delta:
            print(f"  KRAWCZYK PASSES at delta = {delta:g}: "
                  f"alpha = {alpha:.4e} < 1 and "
                  f"{eta + alpha*delta:.4e} <= {delta:g}")
            ok = True
            break
    if not ok:
        print("  Krawczyk test did not pass at any tested delta")
    A2 = assemble(zn[:nw], cells, N)
    sv2 = np.linalg.svd(A2, compute_uv=False)
    nul = int(np.sum(sv2 < 1e-9 * sv2.max()))
    edges = np.abs(zn[2*n:5*n])
    print(f"  the certified matrix: nullity {nul}, gap to the next singular "
          f"value {sv2[-r-1]/sv2.max():.4f}, min|edge|/scale "
          f"{edges.min()/np.abs(zn[:nw]).max():.4f}")
    print(f"  VERDICT: {'null A = ' + str(2*k+2) + ' PROVED' if ok and nul == r else 'not proved'}")


if __name__ == "__main__":
    main()
