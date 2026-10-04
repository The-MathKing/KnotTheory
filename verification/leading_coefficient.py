"""The leading-coefficient criterion, PROVED (thm:leading): if the top
coefficient c_max of det M(zeta) is a nonzero monomial in the edge weights
alone, then null A <= D for every A in S(B^n) and every n.

Mechanism (two gradings on the strip).  Let (p, q) be integer optimal
potentials of the top-degree assignment problem: p_i + q_j >= v for every
monomial zeta^v of entry (i,j), with sum p + sum q = V_max = D/2.  Grade the
strip twice:
  top:     row (i,t) at level t + p_i,   unknown (j,s) at level s - q_j,
  bottom:  row (i,t) at level t - q_i,   unknown (j,s) at level s + p_j.
Every entry of a row lies at top-level <= the row's and bottom-level >= the
row's, with equality exactly on the tight entries, whose matrix L (top) has
det L = c_max as a polynomial identity.  Monomial c_max  <=>  the tight
bipartite graph has a unique perfect matching sigma* and it has no fixed point;
then every sub-block L[S, sigma*(S)] is a product of nonzero weights.

Count.  Fix b >> beta.  U = unknowns with top-level <= b and bottom-level >= beta,
R = rows with top-level <= b and bottom-level >= beta.  Every row in R has all
its unknowns in U; the rows of R are independent (block-triangular in the top
grading with invertible diagonal sub-blocks); every x on U satisfying R
extends uniquely to a kernel sequence on the whole strip (downwards by the
bottom grading, upwards by the top grading), and the restriction is injective.
Hence  dim K = |U| - |R| = sum_j (p_j + q_j) + sum_i (p_i + q_i) = 2 V_max = D,
for EVERY choice of nonzero weights and any diagonal.  Periodic kernel vectors
of A in S(B^n) inject into K, so null A <= D.

This file checks every step on the bases of the paper and on random bases:
  * monomial c_max  <=>  unique max permutation without fixed point;
  * the window count |U| - |R| = D and the independence of R, with random
    non-equivariant weights, by exact rank over F_p and numerically;
  * dim K = D via the forward-transfer monodromy (number of nonzero eigenvalues)
    at the forward-state count sum_j m_j, which can EXCEED D (so a single
    grading does not suffice -- the 3-vertex base below has sum m_j = 13, D = 12).
"""
import itertools
import sys

import numpy as np
import sympy as sp

P_MOD = 33554393


# ----------------------------------------------------------------- symbol
def entries(be, nV):
    """(i,j) -> set of degrees v of zeta appearing in entry (i,j) of M(zeta)."""
    E = {(i, i): {0} for i in range(nV)}
    for (x, y, v) in be:
        if x == y:
            E[(x, x)].update({v, -v})
        else:
            E.setdefault((x, y), set()).add(v)
            E.setdefault((y, x), set()).add(-v)
    return E


def top_coefficient(be, nV):
    """(c_max factored, is it a nonzero monomial in edge weights alone?, D)."""
    z = sp.symbols("z")
    ws = sp.symbols("w0:%d" % len(be))
    ds = sp.symbols("d0:%d" % nV)
    M = sp.zeros(nV, nV)
    for e, (x, y, v) in enumerate(be):
        if x == y:
            M[x, x] += ws[e] * (z ** v + z ** (-v))
        else:
            M[x, y] += ws[e] * z ** v
            M[y, x] += ws[e] * z ** (-v)
    for i in range(nV):
        M[i, i] += ds[i]
    num, _ = sp.fraction(sp.together(sp.expand(M.det())))
    P = sp.Poly(sp.expand(num), z)
    degs = [m[0] for m in P.monoms()]
    top, bot = max(degs), min(degs)
    c = sp.expand(P.coeff_monomial(z ** top))
    mono = len(sp.Add.make_args(c)) == 1 and not any(c.has(d) for d in ds)
    return sp.factor(c), mono, top - bot


# ------------------------------------------------------------- potentials
def max_permutations(be, nV):
    """V_max and the list of permutations attaining it (degree-weighted assignment)."""
    E = entries(be, nV)
    vp = {k: max(s) for k, s in E.items()}
    best, arg = None, []
    for sig in itertools.permutations(range(nV)):
        if any((i, sig[i]) not in vp for i in range(nV)):
            continue
        val = sum(vp[(i, sig[i])] for i in range(nV))
        if best is None or val > best:
            best, arg = val, [sig]
        elif val == best:
            arg.append(sig)
    return best, arg


def optimal_potentials(be, nV, sig):
    """Integer (p, q) with p_i + q_j >= v for every monomial, tight on sig.
    Longest-path potentials (Bellman-Ford) on the exchange digraph; exists iff
    sig is optimal (no nonnegative alternating cycle)."""
    E = entries(be, nV)
    vp = {k: max(s) for k, s in E.items()}
    a = [vp[(i, sig[i])] for i in range(nV)]
    inv = {sig[l]: l for l in range(nV)}
    # p_i - p_l >= vp(i, sig(l)) - a_l   for every entry (i, sig(l)), i != l
    arcs = [(inv[j], i, vp[(i, j)] - a[inv[j]]) for (i, j) in vp if inv[j] != i]
    p = [0] * nV
    for _ in range(nV + 1):
        changed = False
        for (u, v, w) in arcs:
            if p[u] + w > p[v]:
                p[v] = p[u] + w
                changed = True
        if not changed:
            break
    else:
        raise ValueError("positive cycle: sig is not optimal")
    q = [a[inv[j]] - p[inv[j]] for j in range(nV)]
    for (i, j), s in E.items():
        assert p[i] + q[j] >= max(s), "infeasible potential"
    return tuple(p), tuple(q)


def forward_state_count(be, nV, p, q):
    """sum_j m_j, m_j = max slack in column j: the size of the forward state."""
    E = entries(be, nV)
    return sum(max(p[i] + q[j] - v for (i, jj) in E if jj == j for v in E[(i, jj)])
               for j in range(nV))


# ------------------------------------------------- strip rows, two gradings
def strip_row(be, nV, i, t, W, dg, n):
    """Terms ((j, s), coefficient) of the strip equation at row (i,t); weights
    are n-periodic in the fibre index (so the strip operator is the lift of a
    matrix on B^n with free, non-equivariant weights)."""
    terms = [((i, t), dg[i][t % n])]
    for e, (x, y, v) in enumerate(be):
        if x == i:
            terms.append(((y, t + v), W[e][t % n]))
        if y == i:
            terms.append(((x, t - v), W[e][(t - v) % n]))
    return terms


def window_count(be, nV, p, q, W, dg, n, beta=0, b=None, modp=True):
    """|U| - |R| and rank R for U = {unknowns: top<=b, bottom>=beta},
    R = {rows: top<=b, bottom>=beta}.  Returns (|U|-|R|, rank R, |R|)."""
    pq = [p[i] + q[i] for i in range(nV)]
    if b is None:
        b = beta + 2 * max(pq) + 2
    U = {}
    for j in range(nV):
        for lam in range(beta - pq[j], b + 1):          # top-level lam = s - q_j
            U[(j, lam + q[j])] = len(U)
    rows = []
    for i in range(nV):
        for tau in range(beta + pq[i], b + 1):          # top-level tau = t + p_i
            rows.append((i, tau - p[i]))
    A = np.zeros((len(rows), len(U)), dtype=object if modp else float)
    for r, (i, t) in enumerate(rows):
        for ((j, s), c) in strip_row(be, nV, i, t, W, dg, n):
            assert (j, s) in U, "row of R leaves U -- grading error"
            A[r, U[(j, s)]] += c
    if modp:
        rk = rank_modp([[int(x) % P_MOD for x in row] for row in A.tolist()], P_MOD)
    else:
        rk = np.linalg.matrix_rank(A.astype(float))
    return len(U) - len(rows), rk, len(rows)


def rank_modp(M, p):
    M = [row[:] for row in M]
    rows, cols = len(M), len(M[0]) if M else 0
    r = 0
    for c in range(cols):
        piv = next((k for k in range(r, rows) if M[k][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [(x * inv) % p for x in M[r]]
        for k in range(rows):
            if k != r and M[k][c] % p:
                f = M[k][c]
                M[k] = [(x - f * y) % p for x, y in zip(M[k], M[r])]
        r += 1
    return r


def monodromy_zero_count(be, nV, p, q, W, dg, n, tol=1e-9):
    """Forward transfer over one period in the top grading; returns
    (state size, number of eigenvalues of modulus < tol*max)."""
    E = entries(be, nV)
    m = [max(p[i] + q[j] - v for (i, jj) in E if jj == j for v in E[(i, jj)]) for j in range(nV)]
    mtot = sum(m)

    def idx(tau):
        d, c = {}, 0
        for j in range(nV):
            for lam in range(tau - m[j], tau):
                d[(j, lam)] = c
                c += 1
        return d

    Phi = np.eye(mtot)
    for tau in range(n):
        I0, I1 = idx(tau), idx(tau + 1)
        L = np.zeros((nV, nV))
        R = np.zeros((nV, mtot))
        for i in range(nV):
            for ((j, s), c) in strip_row(be, nV, i, tau - p[i], W, dg, n):
                lam = s - q[j]
                if lam == tau:
                    L[i, j] += c
                else:
                    R[i, I0[(j, lam)]] += c
        X = -np.linalg.solve(L, R)
        T = np.zeros((mtot, mtot))
        for (j, lam), c in I1.items():
            if lam == tau:
                T[c, :] = X[j, :]
            else:
                T[c, I0[(j, lam)]] = 1.0
        Phi = T @ Phi
    ev = np.abs(np.linalg.eigvals(Phi))
    return mtot, int(np.sum(ev < tol * ev.max()))


def random_weights(be, nV, n, rng, integer=True):
    if integer:
        W = [[int(x) for x in rng.integers(1, 7, n) * rng.choice([-1, 1], n)] for _ in be]
        dg = [[int(x) for x in rng.integers(-3, 4, n)] for _ in range(nV)]
    else:
        W = [list(rng.standard_normal(n) + 2 * np.sign(rng.standard_normal(n))) for _ in be]
        dg = [list(0.5 * rng.standard_normal(n)) for _ in range(nV)]
    return W, dg


# ------------------------------------------------------------------ checks
def check_base(be, nV, n=7, seed=0, verbose=True):
    rng = np.random.default_rng(seed)
    c, mono, D = top_coefficient(be, nV)
    Vmax, args = max_permutations(be, nV)
    uniq_nofix = len(args) == 1 and all(args[0][i] != i or any(x == y == i for (x, y, v) in be)
                                        for i in range(nV))
    # a fixed point of sigma* at a vertex WITH a loop is the loop monomial, not d_i
    assert mono == uniq_nofix, (be, mono, args)
    assert D == 2 * Vmax
    out = dict(D=D, mono=mono)
    if mono:
        p, q = optimal_potentials(be, nV, args[0])
        W, dg = random_weights(be, nV, n, rng)
        diff, rk, nR = window_count(be, nV, p, q, W, dg, n)
        assert diff == D and rk == nR, (be, diff, rk, nR, D)
        Wf, dgf = random_weights(be, nV, n, rng, integer=False)
        mtot, zeros = monodromy_zero_count(be, nV, p, q, Wf, dgf, n)
        assert mtot - zeros == D, (be, mtot, zeros, D)
        out.update(p=p, q=q, state=mtot, window=diff)
    if verbose:
        print(f"  {str(be):<70} nV={nV} D={D:>2} c_max={c} mono={mono}"
              + (f"  (p,q)={p},{q} forward state={mtot} -> dim K={mtot - zeros}" if mono else ""))
    return out


BASES = [
    ([(0, 0, 1), (1, 1, 2), (0, 1, 0)], 2),
    ([(0, 0, 1), (1, 1, 3), (0, 1, 0)], 2),
    ([(0, 1, 0), (0, 1, 1), (0, 1, 3)], 2),
    ([(0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 1, 3)], 2),
    ([(0, 1, 0), (1, 2, 1), (0, 0, 1), (1, 1, 2), (2, 2, 3)], 3),
    ([(0, 1, 0), (1, 2, 1), (0, 2, 2)], 3),
    ([(0, 1, 0), (1, 2, 1), (2, 3, 0), (0, 3, 2)], 4),
    ([(0, 1, 0), (0, 2, 1), (0, 3, 0), (1, 2, 0), (1, 3, 1), (2, 3, 0)], 4),
    ([(0, 2, 0), (0, 1, 3), (2, 2, 3), (1, 1, 1), (1, 2, 2), (0, 0, 2)], 3),   # sum m_j = 13 > D = 12
    ([(1, 1, 2), (0, 2, 4), (2, 2, 1), (0, 3, 2), (3, 3, 4), (1, 2, 1), (0, 1, -1)], 4),  # 17 > 16
    # the three bases where the ceiling fails: c_max contains a diagonal
    ([(0, 1, 0), (0, 2, 1), (0, 3, 2), (1, 1, 1)], 4),
    ([(0, 2, 0), (0, 3, 1), (0, 4, 2), (1, 2, 0), (1, 3, 1), (1, 4, 2)], 5),
    ([(0, 1, 0), (0, 2, 1), (0, 3, 0), (1, 2, 2), (1, 3, 0), (2, 3, 1)], 4),
]


def random_base(rng):
    nV = int(rng.choice([3, 4, 4, 5]))
    pairs = [(i, j) for i in range(nV) for j in range(i, nV)]
    k = int(rng.integers(nV - 1, min(len(pairs), nV + 4) + 1))
    sel = [pairs[t] for t in rng.choice(len(pairs), k, replace=False)]
    be = [(i, j, int(rng.integers(1, 5)) if i == j else int(rng.integers(-4, 5))) for (i, j) in sel]
    adj = {i: set() for i in range(nV)}
    for (i, j, v) in be:
        adj[i].add(j); adj[j].add(i)
    seen, st = {0}, [0]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y); st.append(y)
    return (be, nV) if len(seen) == nV else None


def run(n_random=60, seed=0):
    print("Paper bases:")
    for be, nV in BASES:
        check_base(be, nV)
    rng = np.random.default_rng(seed)
    cnt = dict(total=0, mono=0, excess=0)
    print(f"Random bases ({n_random}):")
    while cnt["total"] < n_random:
        rb = random_base(rng)
        if rb is None:
            continue
        be, nV = rb
        _, _, D = top_coefficient(be, nV)
        if D == 0:
            continue
        r = check_base(be, nV, seed=int(rng.integers(1 << 30)), verbose=False)
        cnt["total"] += 1
        if r["mono"]:
            cnt["mono"] += 1
            if r["state"] > D:
                cnt["excess"] += 1
    print(f"  {cnt['total']} random bases, {cnt['mono']} with monomial c_max, all with "
          f"dim K = D; in {cnt['excess']} of them the forward state exceeds D.")
    return cnt


if __name__ == "__main__":
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 60)
