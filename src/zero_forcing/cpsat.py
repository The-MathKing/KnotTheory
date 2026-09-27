"""
Exact zero forcing number via CP-SAT, using the time-indexed formulation.

s_v = 1 iff v is in the initial forcing set
x_v = time step at which v becomes filled
y[u,v] = 1 iff u performs the force that fills v

Each vertex is either seeded or filled by exactly one neighbour:
    s_v + sum_{u in N(v)} y[u,v] = 1
and u can only force v if u is already filled and v is u's ONLY unfilled
neighbour, i.e. every other neighbour of u is filled strictly earlier:
    y[u,v]=1  ->  x_u < x_v  and  x_w < x_v for all w in N(u)\\{v}

Minimising sum s_v gives Z(G) exactly. Results are independently re-verified
by running the forcing process on the returned set.
"""
from ortools.sat.python import cp_model


def zero_forcing_number(adj, workers=8, verbose=False, max_seconds=None,
                       require_optimal=True):
    """Z(G) by CP-SAT.

    With max_seconds set, returns None if the solver stops before PROVING
    optimality.  A feasible-but-unproved answer is an upper bound on Z, not Z,
    and returning it as if it were Z is exactly the kind of silent weakening a
    cross-check exists to prevent.
    """
    N = len(adj)
    nbr = [[u for u in range(N) if (adj[v] >> u) & 1] for v in range(N)]
    m = cp_model.CpModel()
    s = [m.NewBoolVar(f"s{v}") for v in range(N)]
    x = [m.NewIntVar(0, N, f"x{v}") for v in range(N)]
    y = {}
    for v in range(N):
        for u in nbr[v]:
            y[u, v] = m.NewBoolVar(f"y_{u}_{v}")
    for v in range(N):
        m.Add(s[v] + sum(y[u, v] for u in nbr[v]) == 1)
    for v in range(N):
        for u in nbr[v]:
            m.Add(x[u] < x[v]).OnlyEnforceIf(y[u, v])
            for w in nbr[u]:
                if w != v:
                    m.Add(x[w] < x[v]).OnlyEnforceIf(y[u, v])
    m.Minimize(sum(s))
    sol = cp_model.CpSolver()
    sol.parameters.num_search_workers = workers
    if max_seconds is not None:
        sol.parameters.max_time_in_seconds = float(max_seconds)
    st = sol.Solve(m)
    if require_optimal and st != cp_model.OPTIMAL:
        return None
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError("no solution")
    S = 0
    for v in range(N):
        if sol.Value(s[v]):
            S |= 1 << v
    return bin(S).count("1"), S
