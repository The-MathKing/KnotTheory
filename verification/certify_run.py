"""Certify null A = 2k+2 rigorously, from a numerical solution.

Pipeline: numerical w  ->  kernel in graph form  ->  square bilinear system
->  high-precision Newton  ->  Krawczyk interval test  ->  proof.
"""
import sys

import numpy as np
from mpmath import iv, mp

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from certify_general import pattern_cells, assemble, graph_form, build_K, jac


def setup(n, k, w):
    N, r = 2 * n, 2 * k + 2
    cells = pattern_cells(n, k)
    A = assemble(w, cells, N)
    U, sv, Vt = np.linalg.svd(A)
    K0 = Vt[-r:].T
    perm, X = graph_form(K0, r)
    nw, nx = len(cells), (N - r) * r
    J = jac(w, X, cells, perm, N, r)
    # choose which nw+nx-(N*r) unknowns to FIX so the rest is square & regular
    _, _, piv = np.linalg.qr(J, mode="complete"), None, None
    import scipy.linalg as sla
    Q, R, P = sla.qr(J, pivoting=True)
    nfix = nw + nx - N * r
    free = sorted(P[:N * r]); fixed = sorted(P[N * r:])
    return cells, perm, X, A, sv, free, fixed, nw, nx, N, r


def f_and_J(z, zfix, free, fixed, cells, perm, N, r, nw, interval=False):
    lib = iv if interval else np
    full = [None] * (nw + (N - r) * r)
    for i, v in zip(free, z): full[i] = v
    for i, v in zip(fixed, zfix): full[i] = v
    w = full[:nw]; Xf = full[nw:]
    X = [[Xf[m * r + t] for t in range(r)] for m in range(N - r)]
    # A K, computed as lists so it works for both float and interval types
    Acells = [[None] * N for _ in range(N)]
    zero = iv.mpf(0) if interval else 0.0
    for i in range(N):
        for j in range(N): Acells[i][j] = zero
    for wj, (_, cl) in zip(w, cells):
        for (i, j) in cl: Acells[i][j] = wj
    Krow = [[zero] * r for _ in range(N)]
    for t, p in enumerate(perm[:r]):
        for tt in range(r):
            Krow[p][tt] = (iv.mpf(1) if interval else 1.0) if tt == t else zero
    for m, p in enumerate(perm[r:]):
        for tt in range(r): Krow[p][tt] = X[m][tt]
    out = []
    for i in range(N):
        for t in range(r):
            acc = zero
            for j in range(N):
                if Acells[i][j] is not zero:
                    acc = acc + Acells[i][j] * Krow[j][t]
            out.append(acc)
    return out


def main():
    n, k = int(sys.argv[1]), int(sys.argv[2])
    wg = np.load(f"/Volumes/2TB/scifair/results/zero_forcing/w_{n}_{k}.npy")
    # general_n.py packs (b, c, e, a, d); pattern_cells wants (a, d, b, c, e)
    b, c, e = wg[:n], wg[n:2*n], wg[2*n:3*n]
    a, d = wg[3*n:4*n], wg[4*n:5*n]
    w = np.concatenate([a, d, b, c, e])
    cells, perm, X, A, sv, free, fixed, nw, nx, N, r = setup(n, k, w)
    print(f"P({n},{k})  N = {N}  target nullity r = {r}")
    print(f"  weights {nw} + kernel entries {nx} = {nw+nx} unknowns, "
          f"{N*r} equations")
    print(f"  fixing {len(fixed)} unknowns at rationals -> square {len(free)}x{len(free)}")
    print(f"  numerical singular values near zero: "
          f"{np.array2string(sv[-r-1:], precision=3)}")
    z0 = np.concatenate([w, X.ravel()])
    res = np.array(f_and_J(z0[free], z0[fixed], free, fixed, cells, perm, N, r, nw))
    print(f"  starting max|A K| = {np.abs(res).max():.3e}")
    # float Newton on the square system
    z = z0.copy()
    for it in range(60):
        J = jac(z[:nw], z[nw:].reshape(N - r, r), cells, perm, N, r)
        F = (assemble(z[:nw], cells, N) @ build_K(z[nw:].reshape(N-r, r), perm, N, r)).ravel()
        Js = J[:, free]
        step = np.linalg.lstsq(Js, -F, rcond=None)[0]
        z[free] += step
        if np.abs(F).max() < 1e-14: break
    J = jac(z[:nw], z[nw:].reshape(N - r, r), cells, perm, N, r)
    F = (assemble(z[:nw], cells, N) @ build_K(z[nw:].reshape(N-r, r), perm, N, r)).ravel()
    A2 = assemble(z[:nw], cells, N)
    sv2 = np.linalg.svd(A2, compute_uv=False)
    print(f"  after Newton: max|A K| = {np.abs(F).max():.3e}   "
          f"cond(square J) = {np.linalg.cond(J[:, free]):.3e}")
    print(f"  nullity of the refined A (1e-9 rel): "
          f"{int(np.sum(sv2 < 1e-9*sv2.max()))}")
    print(f"  smallest non-kernel sv / scale = {sv2[-r-1]/sv2.max():.4f}")
    b = z[:nw][2*n:3*n]; c = z[:nw][3*n:4*n]; e = z[:nw][4*n:5*n]
    print(f"  min |edge weight| / scale = "
          f"{min(np.abs(b).min(),np.abs(c).min(),np.abs(e).min())/np.abs(z[:nw]).max():.4f}")
    np.save(f"/Volumes/2TB/scifair/results/zero_forcing/certz_{n}_{k}.npy", z)
    np.save(f"/Volumes/2TB/scifair/results/zero_forcing/certperm_{n}_{k}.npy",
            np.array(perm))
    print(f"  saved refined solution")


if __name__ == "__main__":
    main()
