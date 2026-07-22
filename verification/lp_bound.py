"""
How strong is the fort LP relaxation for Z(P(n,k))?

Z = min integer hitting set over ALL forts. Its LP relaxation has value
LP <= Z. If LP is close to Z, a fractional fort certificate could prove
lower bounds; if there is a large integrality gap, LP-based methods cannot
prove the open lower bound and should be abandoned.

We compute the exact LP value by cutting planes: solve the LP over the forts
found so far, then separate by finding a MINIMUM-WEIGHT fort under the current
fractional x. If its weight is >= 1 no fort is violated and the LP is optimal.
"""
import sys, os
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from zero_forcing.zf import generalized_petersen


def fort_constraint_matrix(adj):
    """Rows encoding 'F is a fort': for each v and each w in N(v),
       f_w - f_v - sum_{u in N(v)\\{w}} f_u <= 0."""
    N = len(adj)
    rows, cols, vals = [], [], []
    r = 0
    for v in range(N):
        nbrs = [u for u in range(N) if (adj[v] >> u) & 1]
        for w in nbrs:
            rows.append(r); cols.append(w); vals.append(1.0)
            rows.append(r); cols.append(v); vals.append(-1.0)
            for u in nbrs:
                if u != w:
                    rows.append(r); cols.append(u); vals.append(-1.0)
            r += 1
    return csr_matrix((vals, (rows, cols)), shape=(r, N)), r


def min_weight_fort(adj, w, A, r):
    """Minimum-weight fort under vertex weights w (nonempty)."""
    N = len(adj)
    cons = [LinearConstraint(A, lb=np.full(r, -np.inf), ub=np.zeros(r)),
            LinearConstraint(csr_matrix(np.ones((1, N))), lb=np.ones(1),
                             ub=np.array([np.inf]))]
    res = milp(c=w, constraints=cons, integrality=np.ones(N),
               bounds=Bounds(lb=np.zeros(N), ub=np.ones(N)))
    if not res.success:
        return None, None
    F = [v for v in range(N) if res.x[v] > 0.5]
    return F, float(res.fun)


def lp_bound(adj, max_rounds=400, tol=1e-6):
    N = len(adj)
    A, r = fort_constraint_matrix(adj)
    forts = []
    rows, cols = [], []
    val = 0.0
    for rnd in range(max_rounds):
        if forts:
            M = csr_matrix((np.ones(len(rows)), (rows, cols)),
                           shape=(len(forts), N))
            res = linprog(c=np.ones(N), A_ub=-M, b_ub=-np.ones(len(forts)),
                          bounds=[(0, 1)] * N, method="highs")
            if not res.success:
                raise RuntimeError("LP failed")
            x = res.x; val = res.fun
        else:
            x = np.zeros(N); val = 0.0
        F, wt = min_weight_fort(adj, x, A, r)
        if F is None:
            break
        if wt >= 1 - tol:
            return val, len(forts), rnd          # LP optimal
        i = len(forts); forts.append(F)
        for v in F:
            rows.append(i); cols.append(v)
    return val, len(forts), max_rounds


if __name__ == "__main__":
    known = [(10, 2, 6), (12, 2, 6), (11, 3, 7), (12, 3, 7), (14, 3, 8),
             (16, 3, 8), (9, 4, 6), (12, 4, 6), (16, 4, 8), (18, 4, 10),
             (11, 5, 6), (17, 5, 10)]
    print(f"{'graph':>10} {'Z':>3} {'LP':>8} {'gap':>7} {'ratio':>7} {'forts':>6}")
    print("-" * 48)
    for (n, k, Z) in known:
        adj = generalized_petersen(n, k)
        val, nf, rnd = lp_bound(adj)
        print(f"P({n},{k})".rjust(10) + f" {Z:>3} {val:>8.3f} {Z-val:>7.3f} "
              f"{val/Z:>7.3f} {nf:>6}", flush=True)
