"""The reduction on generalized theta covers: two vertices, only u-v edges.

thm:red2 covers two-vertex bases with loops and ONE connecting edge, because
there the outer row meets exactly one inner variable.  The theta base -- two
vertices joined by several edges, no loops -- fails that hypothesis: its outer
row meets every inner variable at once.  The paper records it as the first case
where nothing is known.

It is not actually out of reach; the elimination is just not single-step.  Let
the u-v edges have voltages t_1 < ... < t_m, so

    row u_i :  a_i x_i + sum_r w^r_i y_{i+t_r}           = 0
    row v_j :  d_j y_j + sum_r w^r_{j-t_r} x_{j-t_r}     = 0

The FIRST row solves for y at the TOP voltage, y_{i+t_m}, because w^m_i is an
edge weight and so nonvanishing.  The SECOND solves for x at the largest index
it contains, x_{j-t_1}, because w^1 is likewise nonvanishing.  Together they
advance the pair (x, y) by one step, so the system is a first-order recurrence
on the state

    s_i = (x_i, ..., x_{i+L-1}, y_i, ..., y_{i+L-1}),     L = t_m - t_1,

of dimension 2L.  And 2L is exactly the degree span of det M(zeta): with
f(zeta) = sum_r w_r zeta^{t_r},

    det M = a d - f(zeta) f(1/zeta),

whose span is 2(t_m - t_1).  So the ceiling should again be D, now for a family
the single-step argument cannot touch.

This module builds the transfer matrix explicitly and checks
null A = dim ker(T - I) <= D on covers of this type.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import sys
import numpy as np

sys.path.insert(0, f"{_REPO}/verification")


def build_A(volts, n, wt, diag):
    """A in S(B^n) for the two-vertex base whose u-v edges have these voltages."""
    N = 2 * n
    A = np.zeros((N, N))
    a, d = diag
    for i in range(n):
        A[i, i] = a[i]
        A[n + i, n + i] = d[i]
    for r, t in enumerate(volts):
        for i in range(n):
            j = (i + t) % n
            A[i, n + j] += wt[r][i]
            A[n + j, i] += wt[r][i]
    return A


def transfer(volts, n, wt, diag):
    """One-step transfer on s_i = (x_i..x_{i+L-1}, y_i..y_{i+L-1}), L = t_m - t_1.

    Shift t_1 to 0 without loss (relabelling the v-fibre), so voltages are
    0 = u_1 < ... < u_m = L.
    """
    a, d = diag
    t0 = volts[0]
    v = [t - t0 for t in volts]
    L = v[-1]
    dim = 2 * L
    Ts = []
    for i in range(n):
        # y_{i+L} from row u_i :  a_i x_i + sum_r w^r_i y_{i+v_r} = 0
        ynew = np.zeros(dim)
        ynew[0] = -a[i]                                   # x_i
        for r in range(len(v) - 1):
            ynew[L + v[r]] = -wt[r][i]                    # y_{i+v_r}
        ynew /= wt[-1][i]
        # x_{i+L} from row v_{i+L} (in shifted indexing):
        #   d_{i+L} y_{i+L} + sum_r w^r_{i+L-v_r} x_{i+L-v_r} = 0
        xnew = np.zeros(dim)
        xnew += -d[(i + L) % n] * ynew
        for r in range(1, len(v)):
            xnew[L - v[r]] += -wt[r][(i + L - v[r]) % n]
        xnew /= wt[0][(i + L) % n]
        T = np.zeros((dim, dim))
        for s in range(L - 1):
            T[s, s + 1] = 1.0                             # x shifts
            T[L + s, L + s + 1] = 1.0                     # y shifts
        T[L - 1] = xnew
        T[dim - 1] = ynew
        Ts.append(T)
    M = np.eye(dim)
    for i in range(n):
        M = Ts[i] @ M
    return M, dim


def check(volts, n, seed=0):
    rng = np.random.default_rng(seed)
    m = len(volts)
    wt = [rng.standard_normal(n) + 1.8 for _ in range(m)]
    diag = [rng.standard_normal(n), rng.standard_normal(n)]
    # tune one diagonal entry so the kernel is genuinely nonzero
    from scipy.optimize import brentq

    def f(t):
        dg = [diag[0].copy(), diag[1].copy()]
        dg[0][0] = t
        return np.linalg.det(build_A(volts, n, wt, dg))

    grid = np.linspace(-30, 30, 3000)
    vals = [f(t) for t in grid]
    root = None
    for i in range(len(grid) - 1):
        if vals[i] * vals[i + 1] < 0:
            root = brentq(f, grid[i], grid[i + 1], xtol=1e-14)
            break
    if root is not None:
        diag[0][0] = root
    A = build_A(volts, n, wt, diag)
    T, dim = transfer(volts, n, wt, diag)
    sA = np.linalg.svd(A, compute_uv=False)
    nullA = int(np.sum(sA < 1e-9 * sA.max()))
    sT = np.linalg.svd(T - np.eye(dim), compute_uv=False)
    nullT = int(np.sum(sT < 1e-9 * max(sT.max(), 1.0)))
    D = 2 * (volts[-1] - volts[0])
    return nullA, nullT, D, dim
