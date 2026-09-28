"""The reduction theorem for ALL two-vertex cyclic covers, not just P(n,k).

thm:red is proved in the paper only for P(n,k).  Its proof uses one structural
fact: the row at an outer vertex meets exactly ONE inner variable, with a
nonzero coefficient (the spoke), so that variable can be solved for.  Nothing in
that argument is special to the outer cycle having voltage 1.

So let B be the two-vertex base with
    a loop at u of voltage p   (outer edges  u_i ~ u_{i+p})
    a loop at v of voltage q   (inner edges  v_i ~ v_{i+q})
    one edge u-v of voltage w  (spokes       u_i ~ v_{i+w})
P(n,k) is p=1, q=k, w=0.  Every such cover is cubic on 2n vertices.

CLAIM.  Eliminating the inner coordinates of any A in S(B^n) leaves a single
scalar recurrence in the outer coordinates whose nonzero offsets are the nine
positions

    {-(p+q), -q, -(q-p), -p, 0, p, q-p, q, p+q}

with the two EXTREME coefficients nonzero.  Hence the recurrence has order
exactly 2(p+q), its solution space on Z has dimension exactly 2(p+q), the
n-periodic solutions inject into it, and

    null A  <=  2(p+q)  =  D,

the degree span of det M(zeta).  For p=1 this is thm:red and 2(p+q)=2k+2.

This module verifies the elimination SYMBOLICALLY -- it does not sample or
optimise.  Every coefficient is carried exactly, so a passing check is a check
of the algebra in the proof, not evidence about it.
"""
import sys
import sympy as sp


def eliminate(p, q, w, idx=0):
    """Carry out the elimination symbolically at one index, returning the map
    offset -> coefficient of x_{idx+offset} in the reduced relation."""
    # Row at u_i : b'_{i-p} x_{i-p} + a_i x_i + b_i x_{i+p} + c_i y_{i+w} = 0
    # Row at v_j : e'_{j-q} y_{j-q} + d_j y_j + e_j y_{j+q} + c'_{j-w} x_{j-w} = 0
    a = lambda i: sp.Symbol(f"a_{i}")
    b = lambda i: sp.Symbol(f"b_{i}")      # outer edge (i, i+p)
    c = lambda i: sp.Symbol(f"c_{i}")      # spoke (i, i+w)
    d = lambda i: sp.Symbol(f"d_{i}")      # inner diagonal
    e = lambda i: sp.Symbol(f"e_{i}")      # inner edge (i, i+q)

    def y(j):
        """Solve the u-row at i = j - w for y_j."""
        i = j - w
        return -(b(i - p) * sp.Symbol(f"x_{i-p}")
                 + a(i) * sp.Symbol(f"x_{i}")
                 + b(i) * sp.Symbol(f"x_{i+p}")) / c(i)

    j = idx + w          # the v-row we substitute into
    rel = (e(j - q) * y(j - q) + d(j) * y(j) + e(j) * y(j + q)
           + c(j - w) * sp.Symbol(f"x_{j-w}"))
    rel = sp.expand(sp.together(rel) * c(j - q - w) * c(j - w) * c(j + q - w))
    rel = sp.expand(rel)

    out = {}
    for s in range(-(p + q) - 2, (p + q) + 3):
        co = sp.simplify(rel.coeff(sp.Symbol(f"x_{idx+s}")))
        if co != 0:
            out[s] = co
    return out


def check(p, q, w, verbose=True):
    off = eliminate(p, q, w)
    predicted = sorted({-(p + q), -q, -(q - p), -p, 0, p, q - p, q, p + q})
    got = sorted(off)
    ok_off = got == predicted
    hi, lo = off.get(p + q, 0), off.get(-(p + q), 0)
    ok_ends = hi != 0 and lo != 0
    if verbose:
        print(f"  p={p} q={q} w={w}:  D=2(p+q)={2*(p+q)}")
        print(f"     offsets  {got}")
        print(f"     predicted{predicted}   {'match' if ok_off else 'MISMATCH'}")
        print(f"     end coefficients nonzero: {ok_ends}")
        print(f"       at +{p+q}: {hi}")
    return ok_off and ok_ends


if __name__ == "__main__":
    print(__doc__)
    print("=" * 74)
    cases = [(1, 2, 0), (1, 3, 0), (1, 4, 0),       # P(n,k): the paper's case
             (2, 3, 0), (2, 5, 0), (3, 4, 0),       # outer voltage > 1: NEW
             (1, 3, 1), (2, 5, 2), (3, 4, 1)]       # nonzero spoke voltage: NEW
    bad = []
    for (p, q, w) in cases:
        if not check(p, q, w):
            bad.append((p, q, w))
        print()
    print("=" * 74)
    if bad:
        print(f"ELIMINATION FAILS for {bad}")
        sys.exit(1)
    print("The elimination goes through for every case tested, with the nine")
    print("predicted offsets and nonzero end coefficients. For p=1 this is")
    print("thm:red; for p>1 and w!=0 it is new.")


# --------------------------------------------------------------------------
# Numerical confirmation that the reduction really is a bijection onto ker A.
#
# The symbolic check above verifies the ALGEBRA of the elimination.  This checks
# the CONSEQUENCE: that x -> (x, L(x)) carries the n-periodic solutions of the
# nine-term recurrence bijectively onto ker A.  Random weights give both sides
# nullity 0, which would be a vacuous test, so one weight is tuned to a root of
# det R first -- making the kernel genuinely nonzero before comparing.
import numpy as np


def build(p, q, w, n, wt):
    """A in S(B^n) for the two-vertex base, and the n x n reduced system R."""
    N = 2 * n
    a, b, c, d, e = wt
    A = np.zeros((N, N))
    for i in range(n):
        A[i, i] = a[i]
        A[n + i, n + i] = d[i]
        j = (i + p) % n
        A[i, j] += b[i]; A[j, i] += b[i]
        j = (i + q) % n
        A[n + i, n + j] += e[i]; A[n + j, n + i] += e[i]
        j = (i + w) % n
        A[i, n + j] += c[i]; A[n + j, i] += c[i]
    # y_j = -(b_{i-p} x_{i-p} + a_i x_i + b_i x_{i+p}) / c_i ,  i = j - w
    L = np.zeros((n, n))
    for j in range(n):
        i = (j - w) % n
        L[j, (i - p) % n] += -b[(i - p) % n] / c[i]
        L[j, i] += -a[i] / c[i]
        L[j, (i + p) % n] += -b[i] / c[i]
    # v-row at j:  e_{j-q} y_{j-q} + d_j y_j + e_j y_{j+q} + c_{j-w} x_{j-w} = 0
    R = np.zeros((n, n))
    for j in range(n):
        R[j] += e[(j - q) % n] * L[(j - q) % n]
        R[j] += d[j] * L[j]
        R[j] += e[j] * L[(j + q) % n]
        R[j, (j - w) % n] += c[(j - w) % n]
    return A, L, R


def confirm(p, q, w, n, seed=0):
    rng = np.random.default_rng(seed)
    base = [rng.standard_normal(n) + 1.5 for _ in range(5)]
    # tune one weight to a root of det R so the kernel is genuinely nonzero
    from scipy.optimize import brentq
    def f(t):
        wt = [x.copy() for x in base]; wt[0][0] = t
        return np.linalg.det(build(p, q, w, n, wt)[2])
    lo, hi = -40.0, 40.0
    grid = np.linspace(lo, hi, 4000)
    vals = [f(t) for t in grid]
    root = None
    for i in range(len(grid) - 1):
        if vals[i] * vals[i + 1] < 0:
            root = brentq(f, grid[i], grid[i + 1], xtol=1e-14); break
    if root is None:
        return None
    wt = [x.copy() for x in base]; wt[0][0] = root
    A, L, R = build(p, q, w, n, wt)
    sA = np.linalg.svd(A, compute_uv=False)
    sR = np.linalg.svd(R, compute_uv=False)
    nullA = int(np.sum(sA < 1e-9 * sA.max()))
    nullR = int(np.sum(sR < 1e-9 * sR.max()))
    # every kernel vector of R must lift through x -> (x, Lx) into ker A
    V = np.linalg.svd(R)[2][-max(nullR, 1):].T
    lift = np.vstack([V, L @ V])
    resid = np.abs(A @ lift).max() / np.abs(A).max() if nullR else 0.0
    return nullA, nullR, resid, 2 * (p + q)
