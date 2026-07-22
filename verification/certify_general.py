"""Rigorous certification that a matrix on the pattern of P(n,k) has nullity 2k+2.

The numerical searches solve T = I, which is convenient to optimise but bad to
certify: the map w -> T has a 51-dimensional image inside the 64-dimensional
space of 8x8 matrices at k=3, so {T = I} is cut out by 13 local equations we
cannot identify, and no square subsystem is available.

Certify the nullity instead.  null A >= r if and only if there is a full-rank
K (2n x r) with A K = 0, and putting K in graph form after a row permutation,

    K = P [ I_r ; X ],     X of size (2n - r) x r,

makes rank K = r automatic.  Then A(w) K = 0 is a system of 2n*r equations,
BILINEAR in the weights w and the entries of X -- total degree 2, rational
coefficients.  Fixing enough unknowns at exact rationals leaves a square
system, and the Krawczyk test then proves a true real solution exists in a
small box:

    K(B) = x0 - Y f(x0) + (I - Y f'(B))(B - x0) subset int(B)   =>  unique zero.

That gives null A >= r rigorously; with null A <= 2k+2 from cor:ceiling, the
nullity is exactly 2k+2 and Z(P(n,k)) = 2k+2.
"""
import numpy as np
from mpmath import iv, mp, mpf, matrix as mpmatrix


def pattern_cells(n, k):
    """The 5n weight slots: (kind, list of (i,j))."""
    cells = []
    for i in range(n):
        cells.append(("a", [(i, i)]))
    for i in range(n):
        cells.append(("d", [(n + i, n + i)]))
    for i in range(n):
        j = (i + 1) % n
        cells.append(("b", [(i, j), (j, i)]))
    for i in range(n):
        cells.append(("c", [(i, n + i), (n + i, i)]))
    for i in range(n):
        p, q = n + i, n + (i + k) % n
        cells.append(("e", [(p, q), (q, p)]))
    return cells


def assemble(w, cells, N):
    A = np.zeros((N, N))
    for wj, (_, cl) in zip(w, cells):
        for (i, j) in cl:
            A[i, j] = wj
    return A


def graph_form(K0, r):
    """Row-permute K0 so the top r x r block is well conditioned; return P, X."""
    N = K0.shape[0]
    # greedy: add the row that most improves the smallest singular value, so the
    # top r x r block of the permuted K is as well conditioned as we can make it
    chosen, rest = [], list(range(N))
    B = np.zeros((0, r))
    for _ in range(r):
        best, bv = None, -1.0
        for i in rest:
            M = np.vstack([B, K0[i]])
            sv = np.linalg.svd(M, compute_uv=False)
            v = sv[-1]
            if v > bv:
                bv, best = v, i
        chosen.append(best); rest.remove(best); B = np.vstack([B, K0[best]])
    perm = chosen + rest
    Kp = K0[perm]
    top = Kp[:r]
    X = Kp[r:] @ np.linalg.inv(top)
    return perm, X


def build_K(X, perm, N, r):
    K = np.zeros((N, r))
    K[list(perm[:r])] = np.eye(r)
    K[list(perm[r:])] = X
    return K


def jac(w, X, cells, perm, N, r):
    """Exact Jacobian of vec(A(w) K) in (w, X).  The system is bilinear."""
    nw, nx = len(cells), (N - r) * r
    A = assemble(w, cells, N)
    J = np.zeros((N * r, nw + nx))
    for j, (_, cl) in enumerate(cells):
        for (i, l) in cl:
            J[i * r:(i + 1) * r, j] += build_K(X, perm, N, r)[l]
    lower = list(perm[r:])
    for m, lp in enumerate(lower):
        for t in range(r):
            col = nw + m * r + t
            J[np.arange(N) * r + t, col] += A[:, lp]
    return J


def residual_np(z, n, k, r, cells, perm, fixed_idx, fixed_val):
    N = 2 * n
    nw = len(cells)
    free = [i for i in range(nw + (N - r) * r) if i not in fixed_idx]
    full = np.zeros(nw + (N - r) * r)
    full[free] = z
    for i, v in zip(fixed_idx, fixed_val):
        full[i] = v
    w = full[:nw]
    X = full[nw:].reshape(N - r, r)
    A = assemble(w, cells, N)
    return (A @ build_K(X, perm, N, r)).ravel()


if __name__ == "__main__":
    print(__doc__)
    print("This module provides the machinery; see certify_run.py for a run.")
