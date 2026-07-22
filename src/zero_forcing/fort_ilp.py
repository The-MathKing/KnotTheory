"""
Exact zero forcing number via fort-based cutting planes.

Theory (Fast-Hicks): S is a zero forcing set iff S meets every fort, where a
fort is a nonempty F such that every v outside F has 0 or >=2 neighbours in F.
So Z(G) = minimum hitting set over forts.

Master problem: min sum x_v  s.t.  sum_{v in F} x_v >= 1 for each known fort F.
With only SOME forts this is a relaxation, so its optimum is a valid LOWER
bound on Z. Separation: given the master's solution S, find a MINIMUM fort
disjoint from S (an ILP); that is the strongest possible violated cut.

Exactness: we never trust the solver's claim that a set forces -- we run the
forcing process directly. So the upper bound is independently certified, and
when it meets the relaxation's lower bound the value is exact.
"""
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix


def closure(adj, S):
    N = len(adj); full = (1 << N) - 1; filled = S; ch = True
    while ch and filled != full:
        ch = False; f = filled
        while f:
            v = (f & -f).bit_length() - 1; f &= f - 1
            w = adj[v] & ~filled
            if w and not (w & (w - 1)):
                filled |= w; ch = True
    return filled


def is_zfs(adj, S):
    return closure(adj, S) == (1 << len(adj)) - 1


def min_fort_avoiding(adj, S):
    """Minimum-cardinality fort F with F disjoint from S. Returns bitmask."""
    N = len(adj)
    rows, cols, vals = [], [], []
    r = 0
    for v in range(N):
        nbrs = [u for u in range(N) if (adj[v] >> u) & 1]
        for w in nbrs:
            # f_w - f_v - sum_{u in N(v)\{w}} f_u <= 0
            rows.append(r); cols.append(w); vals.append(1.0)
            rows.append(r); cols.append(v); vals.append(-1.0)
            for u in nbrs:
                if u != w:
                    rows.append(r); cols.append(u); vals.append(-1.0)
            r += 1
    A = csr_matrix((vals, (rows, cols)), shape=(r, N))
    cons = [LinearConstraint(A, lb=np.full(r, -np.inf), ub=np.zeros(r)),
            LinearConstraint(csr_matrix(np.ones((1, N))), lb=np.ones(1),
                             ub=np.array([np.inf]))]           # nonempty
    ub = np.ones(N)
    for v in range(N):
        if (S >> v) & 1:
            ub[v] = 0.0                                        # disjoint from S
    res = milp(c=np.ones(N), constraints=cons, integrality=np.ones(N),
               bounds=Bounds(lb=np.zeros(N), ub=ub))
    if not res.success:
        return None
    F = 0
    for v in range(N):
        if res.x[v] > 0.5:
            F |= 1 << v
    return F


def zero_forcing_number(adj, max_rounds=3000, verbose=False):
    N = len(adj)
    forts = []
    rows, cols = [], []
    for rnd in range(max_rounds):
        if forts:
            A = csr_matrix((np.ones(len(rows)), (rows, cols)),
                           shape=(len(forts), N))
            cons = [LinearConstraint(A, lb=np.ones(len(forts)),
                                     ub=np.full(len(forts), np.inf))]
        else:
            cons = []
        res = milp(c=np.ones(N), constraints=cons, integrality=np.ones(N),
                   bounds=Bounds(lb=np.zeros(N), ub=np.ones(N)))
        if not res.success:
            raise RuntimeError("master ILP failed")
        S = 0
        for v in range(N):
            if res.x[v] > 0.5:
                S |= 1 << v
        lower = bin(S).count("1")
        if is_zfs(adj, S):                      # independently verified
            if verbose:
                print(f"    converged in {rnd} rounds, {len(forts)} forts")
            return lower, S, rnd
        F = min_fort_avoiding(adj, S)
        if F is None or F == 0:
            raise RuntimeError("separation failed")
        r = len(forts); forts.append(F)
        for v in range(N):
            if (F >> v) & 1:
                rows.append(r); cols.append(v)
    raise RuntimeError("max rounds")
