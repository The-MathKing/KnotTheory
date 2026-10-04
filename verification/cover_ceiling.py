"""
Is the degree span a ceiling for NON-equivariant matrices on a cyclic cover?

For P(n,k) we proved null A <= 2k+2 for EVERY matrix carrying the pattern, by
eliminating the inner coordinates (the spokes have nonzero weights) to get a
recurrence of order 2k+2.  For an equivariant matrix on a general cover the
ceiling is the degree span D of det M(zeta).  Whether D bounds NON-equivariant
matrices on a general cover is open.

Random matrices are generically nonsingular, so sampling proves nothing.  This
searches for the largest attainable nullity by direct optimisation -- minimising
the sum of squares of the r smallest eigenvalues, over fully non-equivariant
weights -- and reports the largest r attained.  If that equals D, the span is
tight; if it exceeds D, the conjecture is false and we learn so immediately.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import sys
import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, f"{_REPO}/verification")
from cyclic_covers import blocks


def cover_slots(be, nV, n):
    """One free weight per EDGE OF THE COVER (no symmetry), plus one per vertex."""
    rows, cols, owner = [], [], []
    j = 0
    for (x, y, v) in be:
        for i in range(n):
            p, q = x * n + i, y * n + ((i + v) % n)
            rows += [p, q]; cols += [q, p]; owner += [j, j]
            j += 1
    nedge = j
    for x in range(nV):
        for i in range(n):
            p = x * n + i
            rows += [p]; cols += [p]; owner += [j]; j += 1
    return (np.array(rows), np.array(cols), np.array(owner), j, nedge)


def assemble(w, rows, cols, owner, N):
    A = np.zeros((N, N))
    np.add.at(A, (rows, cols), w[owner])
    return A


def obj(w, rows, cols, owner, N, r, nedge, tau, mu):
    A = assemble(w, rows, cols, owner, N)
    lam, Q = np.linalg.eigh(A)
    idx = np.argsort(np.abs(lam))[:r]
    vals, V = lam[idx], Q[:, idx]
    f = float(np.sum(vals ** 2))
    contrib = 2.0 * vals[None, :] * (V[rows, :] * V[cols, :])
    g = np.zeros(len(w)); np.add.at(g, owner, contrib.sum(axis=1))
    viol = np.maximum(0.0, tau - np.abs(w[:nedge]))
    f += mu * float(np.sum(viol ** 2))
    g[:nedge] += -2.0 * mu * viol * np.sign(w[:nedge])
    pen = w @ w / len(w) - 1.0
    f += pen ** 2; g += 4.0 * pen * w / len(w)
    return f, g


def max_nullity(be, nV, n, rmax, tries=60, seed=0, tau=0.1, mu=30.0):
    rows, cols, owner, P, nedge = cover_slots(be, nV, n)
    N = nV * n
    rng = np.random.default_rng(seed)
    best = 0
    for r in range(rmax, 0, -1):
        hit = False
        for t in range(tries):
            w0 = rng.standard_normal(P); w0 *= np.sqrt(P) / np.linalg.norm(w0)
            res = minimize(obj, w0, jac=True, method="L-BFGS-B",
                           args=(rows, cols, owner, N, r, nedge, tau, mu),
                           options=dict(maxiter=1500, ftol=1e-18, gtol=1e-14))
            A = assemble(res.x, rows, cols, owner, N)
            lam = np.sort(np.abs(np.linalg.eigvalsh(A)))
            sc = np.abs(A).max()
            if lam[r - 1] < 1e-9 * sc and lam[r] > 1e-4 * sc \
               and np.abs(res.x[:nedge]).min() > 1e-2 * sc:
                hit = True; break
        if hit:
            best = r; break
    return best


if __name__ == "__main__":
    cases = [
        ("P(n,2) cover", [(0, 0, 1), (1, 1, 2), (0, 1, 0)], 2, 9, 6),
        ("P(n,3) cover", [(0, 0, 1), (1, 1, 3), (0, 1, 0)], 2, 9, 8),
        ("theta 0,1,2",  [(0, 1, 0), (0, 1, 1), (0, 1, 2)], 2, 9, 4),
        ("theta 0,1,3",  [(0, 1, 0), (0, 1, 1), (0, 1, 3)], 2, 10, 6),
    ]
    print("Largest nullity attainable by a NON-equivariant matrix on a cover\n")
    print(f"{'cover':>16} {'n':>4} {'deg span D':>11} {'max nullity found':>18}"
          f"  verdict")
    for (nm, be, nV, n, span) in cases:
        m = max_nullity(be, nV, n, rmax=span + 2, tries=40)
        if m > span:
            v = "EXCEEDS D -- span is not a ceiling"
        elif m == span:
            v = "equals D -- span is tight here"
        else:
            v = f"below D by {span - m}"
        print(f"{nm:>16} {n:>4} {span:>11} {m:>18}  {v}", flush=True)
