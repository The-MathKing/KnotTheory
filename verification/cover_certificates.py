"""
Prescribed-symbol certificates on an ARBITRARY cyclic cover.

For P(n,k) we reach the ceiling by choosing k+1 interior grid values, forming
the monic symbol with exactly those roots, and solving for the weights.  Nothing
in that used the specific base graph: for any cover, det M(zeta) is a Laurent
polynomial of degree span D, and writing it in sigma = zeta + 1/zeta gives a
polynomial of degree D/2 whose roots on Gamma_n are the singular blocks.  So the
same move works in general -- prescribe D/2 interior grid values, solve for the
weights, and the nullity is D.

This module does that for any base graph, which serves two purposes: it is the
general form of the construction, and it produces the high-nullity examples
needed to test the ceiling sharply (a cover with nullity 2 against a window of
length 12 tests nothing).
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import sys

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, f"{_REPO}/verification")
from cyclic_covers import build_full, blocks


def symbol_coeffs(w, dg, be, nV, npts=None, D=None):
    """Monic coefficients of the symbol in sigma = zeta + 1/zeta."""
    if D is None:
        D = 2 * (sum(abs(v) for (_, _, v) in be) + nV)
    deg = D // 2
    th = np.linspace(0.097, np.pi - 0.083, deg + 1)
    sig = 2 * np.cos(th)
    vals = []
    for t in th:
        z = np.exp(1j * t)
        M = np.zeros((nV, nV), dtype=complex)
        for e, (x, y, v) in enumerate(be):
            M[x, y] += w[e] * z ** v
            M[y, x] += w[e] * np.conj(z) ** v
        for x in range(nV):
            M[x, x] += dg[x]
        vals.append(np.real(np.linalg.det(M)))
    V = np.vander(sig, deg + 1)
    c, *_ = np.linalg.lstsq(V, np.array(vals), rcond=None)
    if abs(c[0]) < 1e-13:
        return None
    return c / c[0]


def true_span(be, nV, rng):
    th = np.linspace(0.11, 2 * np.pi - 0.13, 120)
    w = rng.standard_normal(len(be)) + 1.6
    dg = rng.standard_normal(nV)
    vals = []
    for t in th:
        z = np.exp(1j * t)
        M = np.zeros((nV, nV), dtype=complex)
        for e, (x, y, v) in enumerate(be):
            M[x, y] += w[e] * z ** v
            M[y, x] += w[e] * np.conj(z) ** v
        for x in range(nV):
            M[x, x] += dg[x]
        vals.append(np.linalg.det(M))
    B = sum(abs(v) for (_, _, v) in be) + nV
    V = np.stack([np.exp(1j * j * th) for j in range(-B, B + 1)], axis=1)
    c, *_ = np.linalg.lstsq(V, np.array(vals), rcond=None)
    nz = np.flatnonzero(np.abs(c) > 1e-8 * np.abs(c).max())
    return int(nz.max() - nz.min())


def prescribe(be, nV, n, roots, tries=40, seed=0, tau=0.08, push=4.0, D=None):
    ne = len(be)
    tgt = np.poly(roots)[1:]
    rng = np.random.default_rng(seed)
    best = None
    for t in range(tries):
        x0 = rng.standard_normal(ne + nV)
        x0[:ne] += 1.2 * np.sign(x0[:ne])

        def res(x):
            c = symbol_coeffs(x[:ne], x[ne:], be, nV, D=D)
            if c is None:
                return np.full(len(tgt) + ne, 1e3)
            sc = max(np.abs(x).max(), 1e-12)
            bar = push * np.maximum(0.0, tau - np.abs(x[:ne]) / sc)
            return np.concatenate([1e3 * (c[1:] - tgt), bar])

        sol = least_squares(res, x0, method="trf", xtol=1e-15, ftol=1e-15,
                            gtol=1e-15, max_nfev=900)
        c = symbol_coeffs(sol.x[:ne], sol.x[ne:], be, nV, D=D)
        if c is None:
            continue
        err = np.abs(c[1:] - tgt).max()
        if err > 1e-9:
            continue
        A = build_full(be, nV, n, sol.x[:ne], sol.x[ne:])
        lam = np.sort(np.abs(np.linalg.eigvalsh(A)))
        sc = np.abs(A).max()
        nul = int(np.sum(lam < 1e-9 * sc))
        minw = np.abs(sol.x[:ne]).min() / sc
        if best is None or nul > best[1]:
            best = (A, nul, minw, sol.x)
    return best


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    cases = [
        ("P(n,2) base",   [(0, 0, 1), (1, 1, 2), (0, 1, 0)], 2, 20),
        ("P(n,3) base",   [(0, 0, 1), (1, 1, 3), (0, 1, 0)], 2, 40),
        ("theta 0,1,3",   [(0, 1, 0), (0, 1, 1), (0, 1, 3)], 2, 20),
        ("path 3-vertex", [(0, 0, 1), (1, 1, 2), (2, 2, 3),
                           (0, 1, 0), (1, 2, 0)], 3, 24),
        ("star 4-vertex", [(0, 1, 0), (0, 2, 0), (0, 3, 0),
                           (1, 1, 1), (2, 2, 2), (3, 3, 3)], 4, 24),
    ]
    print(f"{'base graph':>16} {'nV':>3} {'n':>4} {'span D':>7} {'target':>7} "
          f"{'nullity':>8} {'min|w|':>8}")
    for (nm, be, nV, n) in cases:
        D = true_span(be, nV, rng)
        deg = D // 2
        gs = sorted({round(2 * np.cos(2 * np.pi * l / n), 12)
                     for l in range(1, n // 2 + 1)})
        gs = [g for g in gs if abs(abs(g) - 2) > 1e-9]
        if len(gs) < deg:
            print(f"{nm:>16} {nV:>3} {n:>4} {D:>7} {deg:>7} "
                  f"{'grid too small':>8}")
            continue
        res = prescribe(be, nV, n, gs[:deg], tries=30, D=D)
        if res is None:
            print(f"{nm:>16} {nV:>3} {n:>4} {D:>7} {deg:>7} {'none':>8}")
            continue
        A, nul, minw, x = res
        np.save(f"{_REPO}/results/zero_forcing/"
                f"coverA_{nm.split()[0]}_{n}.npy", A)
        print(f"{nm:>16} {nV:>3} {n:>4} {D:>7} {deg:>7} {nul:>8} "
              f"{minw:>8.4f}", flush=True)
