"""EXACT lower bound on the rank of the tile differential, over a prime field.

The tile map w -> P_l(w) is a rational function of the weights with integer
coefficients.  Its Jacobian at a rational point w* therefore has rational
entries; if the denominators are units mod p, the rank of the Jacobian over Q
is at least its rank over F_p (reduction can only create dependencies).  So a
rank computation mod p at a point with small-integer weights is a PROOF that
the generic rank over Q is at least that number -- and when it equals
dim Sp(2k+2) = (k+1)(2k+3), hypothesis (F) of tile_controllability.py holds.

Derivatives are taken exactly by forward-mode differentiation: every gamma
coefficient of the recurrence is a sum of monomial ratios in the weights, so
d(gamma)/dw is read off the exponents, and the chain rule through
T_i = shift + row(-gamma/lead) and P = T_{l-1} ... T_0 is carried mod p.
Only weights in the window of T_i affect it, so the cost is O(l * r^3 * window).

Usage: python tile_rank_exact.py k l [p]
"""
import sys
import numpy as np

P_DEFAULT = 33554393          # prime < 2^25: r*p^2 fits in int64 for r <= 2^13


def inv(x, p):
    return pow(int(x) % p, p - 2, p)


def gamma_terms(i, k, n):
    """Row R_i as a list of (position p, [(sign, [(name, idx, exp), ...])]):
    each term is sign * prod name_idx^exp, exps in {+1,-1}.  Mirrors
    recurrence_order.gamma_row."""
    terms = {}

    def add(pos, sign, mons):
        terms.setdefault(pos, []).append((sign, mons))

    def addL(j_off, e_mon):
        j = (i + j_off) % n
        # y_j = -(b_{j-1} x_{j-1} + a_j x_j + b_j x_{j+1}) / c_j, multiplied by e_mon
        add(j_off - 1, -1, e_mon + [("b", (j - 1) % n, 1), ("c", j, -1)])
        add(j_off,     -1, e_mon + [("a", j, 1), ("c", j, -1)])
        add(j_off + 1, -1, e_mon + [("b", j, 1), ("c", j, -1)])

    addL(-k, [("e", (i - k) % n, 1)])
    addL(0, [("d", i, 1)])
    addL(k, [("e", i, 1)])
    add(0, +1, [("c", i, 1)])
    return terms


def tile_jacobian_rank_modp(k, l, dock, interior_ints, p=P_DEFAULT):
    """dock = (a0, c0, d0, e0) small integers (b0 = 1); interior_ints = dict
    name -> list of nint integers.  Returns (rank mod p, dim Sp)."""
    r = 2 * k + 2
    m = k + 1
    nint = l - 2 * m
    a0, c0, d0, e0 = dock
    D = dict(b=[1] * m, c=[c0] * m, e=[e0] * m, a=[a0] * m, d=[d0] * m)
    tile = {nm: D[nm] + list(interior_ints[nm]) + D[nm] for nm in "bcead"}
    W = {nm: [v % p for v in tile[nm] + tile[nm]] for nm in "bcead"}   # doubled for wrap-around
    n = 2 * l
    # free weight index: (name, position in tile interior) -> column
    names = "bcead"
    col = {}
    for ci, nm in enumerate(names):
        for t in range(nint):
            col[(nm, m + t)] = ci * nint + t
    nw = 5 * nint

    def val(mons):
        v = 1
        for nm, idx, ex in mons:
            x = W[nm][idx % n]
            if ex == 1:
                v = v * x % p
            else:
                if x == 0:
                    raise ZeroDivisionError("zero edge weight in a denominator")
                v = v * inv(x, p) % p
        return v

    def dval(mons, nm0, idx0):
        """d/d(nm0_idx0) of the monomial prod x_s^{e_s}, mod p (product rule)."""
        total = 0
        for t, (nm, idx, ex) in enumerate(mons):
            if nm != nm0 or idx % n != idx0 % n:
                continue
            x = W[nm][idx % n]
            rest = 1
            for u, (nm2, idx2, ex2) in enumerate(mons):
                if u == t:
                    continue
                y = W[nm2][idx2 % n]
                rest = rest * (y if ex2 == 1 else inv(y, p)) % p
            if ex == 1:
                term = rest
            else:
                term = (-rest * inv(x, p) % p) * inv(x, p) % p
            total = (total + term) % p
        return total

    P = np.eye(r, dtype=np.int64)
    dP = np.zeros((nw, r, r), dtype=np.int64)
    for i in range(l):
        terms = gamma_terms(i, k, n)
        # which free weights touch this row?
        touched = set()
        for pos, lst in terms.items():
            for sign, mons in lst:
                for nm, idx, ex in mons:
                    key = (nm, idx % n)
                    if key in col:
                        touched.add(key)
        g = {pos: sum(sign * val(mons) for sign, mons in lst) % p for pos, lst in terms.items()}
        lead = g[k + 1]
        ilead = inv(lead, p)
        T = np.zeros((r, r), dtype=np.int64)
        T[:r - 1, 1:] = np.eye(r - 1, dtype=np.int64)
        for pos, v in g.items():
            if pos != k + 1:
                T[r - 1, pos + k + 1] = (-v * ilead) % p
        # derivatives of T wrt touched weights
        dT = {}
        for key in touched:
            nm0, idx0 = key
            dg = {pos: sum(sign * dval(mons, nm0, idx0) for sign, mons in lst) % p for pos, lst in terms.items()}
            dlead = dg[k + 1]
            M = np.zeros((r, r), dtype=np.int64)
            for pos in g:
                if pos == k + 1:
                    continue
                # d(-g/lead) = -(dg*lead - g*dlead)/lead^2
                num = (dg[pos] * lead - g[pos] * dlead) % p
                M[r - 1, pos + k + 1] = (-num * ilead % p) * ilead % p
            dT[key] = M
        # chain rule: P <- T P ; dP_j <- T dP_j + dT_j P
        newdP = np.einsum("ab,jbc->jac", T, dP) % p
        for key, M in dT.items():
            j = col[key]
            newdP[j] = (newdP[j] + M @ P) % p
        dP = newdP % p
        P = (T @ P) % p
    # Lie-algebra columns: dP_j P^{-1}; rank unaffected by the right factor, so skip it
    J = dP.reshape(nw, r * r).T % p          # (r^2, nw)
    return rank_modp(J, p), (k + 1) * (2 * k + 3)


def rank_modp(A, p):
    A = A.copy() % p
    rows, cols = A.shape
    rank = 0
    for c in range(cols):
        piv = None
        for rr in range(rank, rows):
            if A[rr, c] != 0:
                piv = rr
                break
        if piv is None:
            continue
        A[[rank, piv]] = A[[piv, rank]]
        A[rank] = (A[rank] * inv(A[rank, c], p)) % p
        nz = np.nonzero(A[:, c])[0]
        for rr in nz:
            if rr != rank:
                A[rr] = (A[rr] - A[rr, c] * A[rank]) % p
        rank += 1
        if rank == rows:
            break
    return rank


def explicit_dock_int(k):
    """Integer dock (a0,c0,d0,e0) with b0=1 whose step matrix is elliptic:
    scaled version of (0.17,0.3,-0.11,+-1) is not integral, so use the sign
    pattern with c0 = 1, a0 = 1, d0 = -1 and verify ellipticity numerically."""
    e0 = (1 if ((k - 1) // 2) % 2 == 0 else -1) if k % 2 == 1 else 1
    return (1, 1, -1, e0)


def exact_elliptic(k, dock):
    """(E) decided EXACTLY: the dock symbol F(s) = (a0+s)(d0+e0 t_k(s)) - c0^2 has
    k+1 distinct real roots in (-2,2) -- Sturm root isolation over Q."""
    import sympy as sp
    s_ = sp.symbols("s")
    a0, c0, d0, e0 = dock
    tk = sp.expand(2 * sp.chebyshevt(k, s_ / 2))
    F = sp.Poly(sp.expand((a0 + s_) * (d0 + e0 * tk) - c0 ** 2), s_)
    ivals = F.intervals(inf=-2, sup=2)
    roots_in = [iv for iv in ivals if iv[1] == 1]        # multiplicity 1
    n_total = sum(m for _, m in ivals)
    return len(roots_in) == k + 1 and n_total == k + 1 and F.degree() == k + 1


def integer_elliptic_dock(k):
    """Small-integer dock with an elliptic step matrix, found by scanning and
    certified by exact_elliptic."""
    for e0 in (1, -1, 2, -2, 3, -3, 5, -5, 10, -10):
        for a0 in (0, 1, -1):
            for d0 in (0, -1, 1):
                for c0 in (1, 2):
                    if exact_elliptic(k, (a0, c0, d0, e0)):
                        return (a0, c0, d0, e0)
    return None


if __name__ == "__main__":
    k = int(sys.argv[1]); l = int(sys.argv[2]); p = int(sys.argv[3]) if len(sys.argv) > 3 else P_DEFAULT
    dock = integer_elliptic_dock(k)
    if dock is None:
        print(f"k={k}: no small integer elliptic dock"); sys.exit(1)
    rng = np.random.default_rng(k)
    nint = l - 2 * k - 2
    interior = {nm: [int(x) for x in rng.integers(-3, 4, nint)] for nm in "bcead"}
    for nm in "bce":                      # edge weights nonzero
        interior[nm] = [x if x != 0 else 1 for x in interior[nm]]
    rank, need = tile_jacobian_rank_modp(k, l, dock, interior, p)
    print(f"k={k} l={l} p={p}: dock {dock} (E) exact: True; rank of Jacobian mod p = {rank}, dim Sp = {need}  ->  {'(F) CERTIFIED' if rank >= need else 'not full'}")
