"""Is the nullity ceiling a property of the COVER, or only of equivariant matrices?

The paper proves null A <= 2k+2 for EVERY matrix carrying the P(n,k) pattern,
but on a general base it proves the ceiling only for matrices that commute with
the Z_n action.  Whether the bound survives for arbitrary (non-equivariant)
matrices on an arbitrary cyclic cover is stated as open.  Closing it would turn
the headline from a fact about P(n,k) into a theorem about cyclic covers.

This is an attempt to break it, not to confirm it.  Confirmations are cheap:
a random matrix on a cover is generically nonsingular, so sampling proves
nothing.  What is informative is MAXIMISING the nullity over fully
non-equivariant weights -- one free weight per lift of each base edge, plus a
free diagonal per lift -- and asking whether the optimum can exceed the degree
span D of det M(zeta), which is read off the base alone.

Method.  For a target nullity d, minimise the sum of the d smallest squared
singular values of A(w) over the weights, with the weights held away from zero
so the pattern stays genuine, from many random starts.  If that infimum is
driven to ~0 for d = D+1 on any base, the conjecture is false and we have a
counterexample.  If it stalls at D on every base while reaching exactly D
whenever the cover is large enough, that is real evidence.
"""
import itertools
import math
import os
import sys

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sympy as sp


# ---------------------------------------------------------------------------
# the base library: (name, edges as (x, y, voltage), number of base vertices)
# deliberately wider than the paper's four -- different sizes, different
# degrees, loops and parallel edges, Hamiltonian and non-Hamiltonian
# ---------------------------------------------------------------------------
BASES = {
    "P(n,2) two-loop":   ([(0, 0, 1), (1, 1, 2), (0, 1, 0)], 2),
    "P(n,3) two-loop":   ([(0, 0, 1), (1, 1, 3), (0, 1, 0)], 2),
    "theta (0,1,2)":     ([(0, 1, 0), (0, 1, 1), (0, 1, 2)], 2),
    "theta (0,1,3)":     ([(0, 1, 0), (0, 1, 1), (0, 1, 3)], 2),
    "4-edge theta":      ([(0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 1, 3)], 2),
    "path-3 (0,1)":      ([(0, 1, 0), (1, 2, 1)], 3),
    "path-3 loops":      ([(0, 1, 0), (1, 2, 1), (0, 0, 1), (2, 2, 2)], 3),
    "triangle (0,1,2)":  ([(0, 1, 0), (1, 2, 1), (0, 2, 2)], 3),
    "star-4 (no ham.)":  ([(0, 1, 0), (0, 2, 1), (0, 3, 2)], 4),
    "star-4 + loop":     ([(0, 1, 0), (0, 2, 1), (0, 3, 2), (1, 1, 1)], 4),
    "K4 assorted":       ([(0, 1, 0), (0, 2, 1), (0, 3, 0),
                           (1, 2, 2), (1, 3, 0), (2, 3, 1)], 4),
    "C4 cycle base":     ([(0, 1, 0), (1, 2, 1), (2, 3, 0), (0, 3, 2)], 4),
    "path-5":            ([(0, 1, 0), (1, 2, 1), (2, 3, 0), (3, 4, 2)], 5),
}


def degree_span(base_edges, nV):
    """D = span of exponents in det M(zeta), from the voltages alone.

    Computed symbolically with independent symbolic weights, so the answer is
    the GENERIC span and not an artefact of a particular weight choice.
    """
    z = sp.symbols("z")
    w = sp.symbols("w0:%d" % len(base_edges))
    d = sp.symbols("d0:%d" % nV)
    M = sp.zeros(nV, nV)
    for e, (x, y, v) in enumerate(base_edges):
        if x == y:
            M[x, x] += w[e] * (z ** v + z ** (-v))
        else:
            M[x, y] += w[e] * z ** v
            M[y, x] += w[e] * z ** (-v)
    for x in range(nV):
        M[x, x] += d[x]
    det = sp.simplify(sp.expand(M.det()))
    det = sp.together(det)
    num, den = sp.fraction(det)
    pn = sp.Poly(sp.expand(num), z)
    # den is a power of z; shifting by it does not change the SPAN
    exps = [m[0] for m in pn.monoms() if pn.coeff_monomial(z ** m[0]) != 0]
    return max(exps) - min(exps)


def cover_connected(base_edges, nV, n):
    """A tree base has trivial cycle space, so its cover is n disjoint copies.
    Those are outside the theory -- the ceiling question is about connected
    covers -- and including them manufactures fake counterexamples."""
    import scipy.sparse.csgraph as csg
    from scipy.sparse import csr_matrix
    N = nV * n
    A = np.zeros((N, N))
    for (x, y, v) in base_edges:
        for i in range(n):
            p, q = x * n + i, y * n + ((i + v) % n)
            A[p, q] = 1.0
            A[q, p] = 1.0
    return csg.connected_components(csr_matrix(A))[0] == 1


def build(base_edges, nV, n, w, diag):
    """A(w): one FREE weight per lift of each base edge, free diagonal per lift."""
    N = nV * n
    A = np.zeros((N, N))
    idx = 0
    for (x, y, v) in base_edges:
        for i in range(n):
            j = (i + v) % n
            p, q = x * n + i, y * n + j
            A[p, q] += w[idx]
            A[q, p] += w[idx]
            idx += 1
    for x in range(nV):
        for i in range(n):
            A[x * n + i, x * n + i] = diag[x * n + i]
    return A


def max_nullity(base_edges, nV, n, d, restarts=14, seed=0, floor=0.25):
    """Infimum over weights of the sum of the d smallest squared singular
    values, with every edge weight pushed to have magnitude >= floor."""
    ne = len(base_edges) * n
    nd = nV * n
    rng = np.random.default_rng(seed)

    def unpack(p):
        return p[:ne], p[ne:]

    def obj(p):
        w, diag = unpack(p)
        A = build(base_edges, nV, n, w, diag)
        sv = np.sort(np.linalg.svd(A, compute_uv=False))
        # The d-th smallest singular value, RELATIVE to the matrix scale.  An
        # earlier version minimised the sum of the d smallest squares, which is
        # the wrong statistic: it reports success when one value is tiny and the
        # rest are merely small, since sum-of-squares hides a 1e-6 behind a
        # 1e-10.  That produced a false counterexample.  sigma_d -> 0 is the
        # actual question -- it forces ALL d of them down.
        scale = max(np.abs(A).max(), 1e-12)
        pen = np.sum(np.clip(floor - np.abs(w), 0, None) ** 2)
        return float(sv[d - 1] / scale + 50.0 * pen)

    best = np.inf
    for _ in range(restarts):
        p0 = np.concatenate([rng.standard_normal(ne) + np.sign(rng.standard_normal(ne)),
                             rng.standard_normal(nd) * 0.5])
        r = minimize(obj, p0, method="Nelder-Mead",
                     options=dict(maxiter=20000, maxfev=20000,
                                  xatol=1e-10, fatol=1e-14))
        best = min(best, r.fun)
    return best


def attack(n=7, verbose=True):
    """For each base: can non-equivariant weights beat the degree span?"""
    rows = []
    for name, (be, nV) in BASES.items():
        D = degree_span(be, nV)
        if nV * n > 40 or not cover_connected(be, nV, n):
            continue
        at_D = max_nullity(be, nV, n, D) if D >= 1 else 0.0
        over = max_nullity(be, nV, n, D + 1)
        rows.append((name, nV, D, at_D, over))
        if verbose:
            verdict = "BROKEN" if over < 1e-7 else "holds"
            print("  %-20s nV=%d  D=%-3d  inf@D=%.2e  inf@D+1=%.2e   %s"
                  % (name, nV, D, at_D, over, verdict))
    return rows


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    print("Attacking the non-equivariant cover ceiling at n = %d" % n)
    print("  inf@D   : can nullity D be attained?      (small = yes)")
    print("  inf@D+1 : can nullity D+1 be attained?    (small = CONJECTURE FALSE)")
    print()
    rows = attack(n)
    broken = [r for r in rows if r[4] < 1e-7]
    print()
    if broken:
        print("COUNTEREXAMPLES FOUND:", [r[0] for r in broken])
    else:
        print("No counterexample at n = %d over %d bases." % (n, len(rows)))
        reach = sum(1 for r in rows if r[3] < 1e-7)
        print("The ceiling D was ATTAINED on %d of %d." % (reach, len(rows)))


# ---------------------------------------------------------------------------
# thm:redpath -- the chained elimination on a path-with-loops base
# ---------------------------------------------------------------------------

def path_loops_base(ps, ws):
    """Base x_1 - ... - x_m with a loop of voltage ps[t] at x_t and a single
    connecting edge of voltage ws[t] between x_t and x_{t+1}."""
    m = len(ps)
    be = [(t, t, p) for t, p in enumerate(ps)]
    be += [(t, t + 1, w) for t, w in enumerate(ws)]
    return be, m


PATH_CASES = [((1, 2), (0,)), ((1, 3), (0,)), ((2, 3), (1,)),
              ((1, 1, 2), (2, 0)), ((1, 1, 1), (0, 1)), ((1, 2, 1), (0, 1)),
              ((1, 2, 3), (0, 1)), ((1, 2, 1, 3), (0, 1, 2))]


def check_path_span():
    """The theorem's span claim: D = 2 sum(p_t), from the voltages alone."""
    bad = []
    for ps, ws in PATH_CASES:
        be, m = path_loops_base(ps, ws)
        if degree_span(be, m) != 2 * sum(ps):
            bad.append((ps, ws))
    return len(PATH_CASES), bad


def check_path_ceiling(restarts=8):
    """Adversarial: can non-equivariant weights beat 2 sum(p) on a path base?"""
    rows = []
    for ps, ws in PATH_CASES[:5]:
        be, m = path_loops_base(ps, ws)
        D = 2 * sum(ps)
        n = D + 3
        while m * n > 44 and n > D + 1:
            n -= 1
        if m * n > 44 or not cover_connected(be, m, n):
            continue
        over = max_nullity(be, m, n, D + 1, restarts=restarts)
        rows.append((ps, ws, n, D, over))
    return rows


# ---------------------------------------------------------------------------
# thm:redcycle -- cycle bases, where the cover degenerates to a union of cycles
# ---------------------------------------------------------------------------

def cycle_base(ws):
    """Base x_0 - x_1 - ... - x_{m-1} - x_0 with edge t -> t+1 of voltage ws[t]."""
    m = len(ws)
    return [(t, (t + 1) % m, w) for t, w in enumerate(ws)], m


CYCLE_CASES = [(0, 1, -2), (1, 1, 1), (2, 3, -1), (0, 1, 2),
               (1, 2, 3, -5), (0, 1, 0, -2), (0, 0, 1)]


def check_cycle_span():
    """The span claim: D = 2|W| with W the holonomy."""
    bad = []
    for ws in CYCLE_CASES:
        be, m = cycle_base(ws)
        W = sum(ws)
        if W == 0:
            continue
        if degree_span(be, m) != 2 * abs(W):
            bad.append(ws)
    return len(CYCLE_CASES), bad


def check_cycle_structure(ns=(6, 7, 8, 9, 10, 12)):
    """The cover is 2-regular, with exactly gcd(|W|,n) components."""
    import math
    import scipy.sparse.csgraph as csg
    from scipy.sparse import csr_matrix
    bad, total = [], 0
    for ws in CYCLE_CASES:
        W = sum(ws)
        if W == 0:
            continue
        be, m = cycle_base(ws)
        for n in ns:
            N = m * n
            A = np.zeros((N, N))
            for (x, y, v) in be:
                for i in range(n):
                    p, q = x * n + i, y * n + ((i + v) % n)
                    A[p, q] += 1
                    A[q, p] += 1
            if A.max() > 1:
                continue                      # not a simple graph
            total += 1
            ncomp = csg.connected_components(csr_matrix(A))[0]
            two_reg = bool(np.all(A.sum(axis=0) == 2))
            if ncomp != math.gcd(abs(W), n) or not two_reg:
                bad.append((ws, n, ncomp, math.gcd(abs(W), n), two_reg))
    return total, bad
