"""
Zero forcing number computation, with generalized Petersen graphs P(n,k).

Zero forcing rule: given a set S of filled vertices, if a filled vertex has
exactly one unfilled neighbor, that neighbor becomes filled. Iterate to
closure. S is a zero forcing set (ZFS) if the closure is all of V.
Z(G) = min |S| over zero forcing sets S.

Exact computation uses the fort formulation (Fast-Hicks):
  A fort is a nonempty F subset V such that every v not in F has either 0 or
  >= 2 neighbors in F. S is a ZFS iff S meets every fort.
So Z(G) = minimum hitting set of the fort hypergraph. We solve this by ILP
with lazy constraint generation: solve, test the candidate, and if it stalls,
the stalled (unfilled) set is itself a fort -- add it as a new constraint.

Graphs are represented as a list of neighbor bitmasks.
"""
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


def generalized_petersen(n, k):
    """P(n,k): outer cycle u_0..u_{n-1}, inner v_0..v_{n-1}, spokes u_i~v_i,
    inner edges v_i ~ v_{i+k}. Vertices 0..n-1 outer, n..2n-1 inner."""
    if not (n >= 3 and 1 <= k < n / 2):
        raise ValueError(f"P({n},{k}) requires n>=3 and 1<=k<n/2")
    N = 2 * n
    adj = [0] * N
    def link(a, b):
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    for i in range(n):
        link(i, (i + 1) % n)          # outer cycle
        link(i, n + i)                # spoke
        link(n + i, n + (i + k) % n)  # inner
    return adj


def closure(adj, S_mask):
    """Run the forcing rule to closure; return the final filled bitmask."""
    N = len(adj)
    filled = S_mask
    full = (1 << N) - 1
    changed = True
    while changed and filled != full:
        changed = False
        f = filled
        while f:
            v = (f & -f).bit_length() - 1
            f &= f - 1
            white = adj[v] & ~filled
            if white and (white & (white - 1)) == 0:   # exactly one white nbr
                filled |= white
                changed = True
    return filled


def is_zfs(adj, S_mask):
    return closure(adj, S_mask) == (1 << len(adj)) - 1


def stalled_fort(adj, S_mask):
    """If S is not a ZFS, the complement of its closure is a fort."""
    return ((1 << len(adj)) - 1) & ~closure(adj, S_mask)


def is_fort(adj, F):
    """F nonempty, and every v outside F has 0 or >=2 neighbours in F."""
    if F == 0:
        return False
    N = len(adj)
    for v in range(N):
        if not (F >> v) & 1:
            c = adj[v] & F
            if c and (c & (c - 1)) == 0:
                return False
    return True


def minimal_fort(adj, F, order=None):
    """Greedily shrink F to a minimal fort. A different removal `order` yields
    a different minimal fort, which is how we harvest many cuts per round."""
    verts = mask_to_list(F) if order is None else order
    changed = True
    while changed:
        changed = False
        for v in verts:
            if not (F >> v) & 1:
                continue
            cand = F & ~(1 << v)
            if cand and is_fort(adj, cand):
                F = cand
                changed = True
    return F


def harvest_forts(adj, F, rng, count=40):
    """Extract several distinct minimal forts from one stalled set. Adding many
    cuts per round is what makes the lazy ILP converge in few rounds."""
    out = set()
    base = mask_to_list(F)
    for _ in range(count):
        order = base[:]
        rng.shuffle(order)
        out.add(minimal_fort(adj, F, order))
    return out


def mask_to_list(m):
    out = []
    while m:
        v = (m & -m).bit_length() - 1
        out.append(v)
        m &= m - 1
    return out


def seed_forts(adj, rng, n_samples=400, per_sample=6):
    """Build a diverse library of minimal forts up front. Strong (small) cuts
    found before the ILP loop starts are what make it converge in few rounds."""
    N = len(adj)
    forts = set()
    for _ in range(n_samples):
        size = rng.randint(1, max(2, N // 3))
        S = 0
        for v in rng.sample(range(N), size):
            S |= 1 << v
        st = stalled_fort(adj, S)
        if st == 0:
            continue
        base = mask_to_list(st)
        for _ in range(per_sample):
            order = base[:]
            rng.shuffle(order)
            forts.add(minimal_fort(adj, st, order))
    return forts


def zero_forcing_number(adj, max_iters=400, seed=0, verbose=False):
    """Exact Z(G). Returns (Z, witness_set).

    Correctness: with any subset of the true fort family the ILP is a
    relaxation of the exact fort-hitting-set problem, so its optimum is a
    valid LOWER bound on Z. If the returned set also forces, it is a valid
    zero forcing set, giving a matching UPPER bound -- so the value is exact.
    """
    import random
    from scipy.sparse import csr_matrix
    rng = random.Random(seed)
    N = len(adj)
    forts = list(seed_forts(adj, rng))
    seen = set(forts)
    c = np.ones(N)
    integrality = np.ones(N)
    bounds = Bounds(lb=np.zeros(N), ub=np.ones(N))

    rows, cols = [], []
    for r, F in enumerate(forts):
        for v in mask_to_list(F):
            rows.append(r); cols.append(v)

    for it in range(max_iters):
        if forts:
            A = csr_matrix((np.ones(len(rows)), (rows, cols)),
                           shape=(len(forts), N))
            cons = [LinearConstraint(A, lb=np.ones(len(forts)),
                                     ub=np.full(len(forts), np.inf))]
        else:
            cons = []
        res = milp(c=c, constraints=cons, integrality=integrality, bounds=bounds)
        if not res.success:
            raise RuntimeError("ILP failed")
        S = 0
        for v in range(N):
            if res.x[v] > 0.5:
                S |= 1 << v
        lower = bin(S).count("1")
        if is_zfs(adj, S):
            if verbose:
                print(f"    converged round {it}, forts={len(forts)}")
            return lower, S
        st = stalled_fort(adj, S)
        base = mask_to_list(st)
        added = 0
        for _ in range(60):
            order = base[:]
            rng.shuffle(order)
            F = minimal_fort(adj, st, order)
            if F not in seen:
                seen.add(F)
                r = len(forts)
                forts.append(F)
                for v in mask_to_list(F):
                    rows.append(r); cols.append(v)
                added += 1
        if added == 0:
            for _ in range(200):
                size = rng.randint(lower, min(N - 1, lower + 3))
                T = 0
                for v in rng.sample(range(N), size):
                    T |= 1 << v
                st2 = stalled_fort(adj, T)
                if st2 == 0:
                    continue
                b2 = mask_to_list(st2)
                rng.shuffle(b2)
                F = minimal_fort(adj, st2, b2)
                if F not in seen:
                    seen.add(F)
                    r = len(forts)
                    forts.append(F)
                    for v in mask_to_list(F):
                        rows.append(r); cols.append(v)
                    added += 1
            if added == 0:
                raise RuntimeError(f"stalled: no new forts (lower bound {lower})")
    raise RuntimeError("did not converge")


def zf_bruteforce(adj, cap=9):
    """Independent exact Z(G) by increasing subset size -- validation only."""
    from itertools import combinations
    N = len(adj)
    for size in range(1, cap + 1):
        for combo in combinations(range(N), size):
            S = 0
            for v in combo:
                S |= 1 << v
            if is_zfs(adj, S):
                return size
    return None
