"""The cover-ceiling attack again, with a solver strong enough to be believed.

`cover_ceiling_attack` used Nelder-Mead.  That solver is too weak for this
problem: on P(10,2) it reported nullity 6 unreachable across sixty restarts when
a nullity-6 matrix exists, and on bases of degree span 6 and 8 it could not
reach the span at all.  Evidence of the form "a search failed" is worth exactly
as much as the search, so the earlier "no counterexample on ten bases" was a
weaker statement than it looked.

This version minimises the sum of squares of the d eigenvalues nearest zero with
an ANALYTIC gradient (d lambda_i = v_i v_i^T) under L-BFGS, which is what makes
the search strong enough that a failure means something.  Two things are
reported for every base: whether the span D is attained (the solver should
reach it -- if it cannot, the search is too weak to interpret) and whether D+1
is attainable (which would refute the conjecture).

The matrices here are fully non-equivariant: one free weight per lift of each
base edge, one free diagonal per lift.
"""
import math
import os
import sys

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from verification.cover_ceiling_attack import (BASES, cover_connected,
                                               degree_span)


def cover_pattern(base_edges, nV, n):
    """Index pairs (p,q), p<q, of the cover's edges, and its size."""
    N = nV * n
    seen = set()
    for (x, y, v) in base_edges:
        for i in range(n):
            p, q = x * n + i, y * n + ((i + v) % n)
            if p == q:
                continue
            seen.add((min(p, q), max(p, q)))
    return sorted(seen), N


def max_nullity(base_edges, nV, n, d, restarts=40, seed=0, floor=0.3):
    """Infimum of sum of squares of the d eigenvalues nearest zero.

    Returns (objective, relative |eigenvalues| nearest zero, min |edge weight|).
    An objective below ~1e-16 means nullity d is attainable.
    """
    cells, N = cover_pattern(base_edges, nV, n)
    ne = len(cells)
    I_ = np.array([c[0] for c in cells])
    J_ = np.array([c[1] for c in cells])
    rng = np.random.default_rng(seed)
    diag_idx = np.arange(N)

    def build(p):
        A = np.zeros((N, N))
        A[I_, J_] = p[:ne]
        A[J_, I_] = p[:ne]
        A[diag_idx, diag_idx] = p[ne:]
        return A

    def fg(p):
        A = build(p)
        lam, V = np.linalg.eigh(A)
        idx = np.argsort(np.abs(lam))[:d]
        f = float(np.sum(lam[idx] ** 2))
        G = np.zeros((N, N))
        for i in idx:
            v = V[:, i]
            G += 2 * lam[i] * np.outer(v, v)
        g = np.empty_like(p)
        g[:ne] = 2 * G[I_, J_]
        g[ne:] = np.diag(G)
        w = p[:ne]
        viol = np.clip(floor - np.abs(w), 0, None)
        f += 50.0 * float(np.sum(viol ** 2))
        g[:ne] += 50.0 * (-2 * viol * np.sign(w))
        return f, g

    best, bestp = np.inf, None
    for _ in range(restarts):
        p0 = np.concatenate([
            rng.standard_normal(ne) + np.sign(rng.standard_normal(ne)),
            rng.standard_normal(N)])
        r = minimize(fg, p0, jac=True, method="L-BFGS-B",
                     options=dict(maxiter=4000, ftol=1e-18, gtol=1e-14))
        if r.fun < best:
            best, bestp = r.fun, r.x
    A = build(bestp)
    lam = np.sort(np.abs(np.linalg.eigh(A)[0]))
    scale = max(np.abs(A).max(), 1e-12)
    return best, lam[:d + 1] / scale, float(np.abs(bestp[:ne]).min())


ATTAINED = 1e-16


def sweep(n=7, restarts=40, seeds=(0, 1, 2), maxN=60, verbose=True):
    """For every connected base: is D attained, and can D+1 be reached?"""
    rows = []
    for name, (be, nV) in BASES.items():
        if nV * n > maxN or not cover_connected(be, nV, n):
            continue
        D = degree_span(be, nV)
        if D < 1:
            continue
        atD = min(max_nullity(be, nV, n, D, restarts, s)[0] for s in seeds)
        over = min(max_nullity(be, nV, n, D + 1, restarts, s)[0] for s in seeds)
        rows.append((name, nV, D, atD, over))
        if verbose:
            if over < ATTAINED:
                verdict = "*** CONJECTURE FALSE ***"
            elif atD < ATTAINED:
                verdict = "holds, D attained"
            else:
                verdict = "holds, but D NOT attained (search too weak to read)"
            print("  %-20s nV=%d D=%-3d  at D=%.2e  at D+1=%.2e   %s"
                  % (name, nV, D, atD, over, verdict))
    return rows


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    print("Cover ceiling, gradient solver, n = %d" % n)
    print("  at D   : can nullity D be attained?   (< 1e-16 = yes)")
    print("  at D+1 : can nullity D+1 be attained? (< 1e-16 = CONJECTURE FALSE)")
    print()
    rows = sweep(n)
    broken = [r for r in rows if r[4] < ATTAINED]
    weak = [r for r in rows if r[3] >= ATTAINED]
    print()
    print("counterexamples: %s" % ([r[0] for r in broken] or "none"))
    print("bases where D itself was not reached (search too weak there): %s"
          % ([r[0] for r in weak] or "none"))
