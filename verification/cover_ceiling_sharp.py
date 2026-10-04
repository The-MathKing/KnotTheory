"""
The sharp test of the cover ceiling: certificates AT the ceiling, then
injectivity on a window of that exact length.

An earlier test checked whether ker A injects into a window of length D using
matrices of nullity 2 -- with D between 6 and 12 that is trivially true and
tests nothing.  The test only bites when the nullity EQUALS D.

So: build a certificate of nullity D on each cover (choosing among root sets
rather than taking the first, since a set with no slack degenerates), then ask
whether ker A -> (x_{a,i}) over a window of length D is injective.  Injectivity
at the ceiling is exactly the statement that no nonzero kernel vector vanishes
on D consecutive fibre coordinates, which is what bounds the nullity by D for
EVERY matrix carrying the pattern -- the general form of the P(n,k) theorem.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import itertools
import sys

import numpy as np

sys.path.insert(0, f"{_REPO}/verification")
from cyclic_covers import build_full
from cover_certificates import prescribe, true_span
from cover_elimination import has_hamiltonian_path, window_injective


def grid(n):
    gs = sorted({(l, round(2 * np.cos(2 * np.pi * l / n), 12))
                 for l in range(1, n // 2 + 1)}, key=lambda t: t[0])
    return [(l, s) for (l, s) in gs if abs(abs(s) - 2) > 1e-9]


if __name__ == "__main__":
    rng = np.random.default_rng(1)
    cases = [
        ("P(n,2) base",   [(0, 0, 1), (1, 1, 2), (0, 1, 0)], 2, 20),
        ("P(n,3) base",   [(0, 0, 1), (1, 1, 3), (0, 1, 0)], 2, 24),
        ("theta 0,1,3",   [(0, 1, 0), (0, 1, 1), (0, 1, 3)], 2, 20),
        ("theta 0,2,5",   [(0, 1, 0), (0, 1, 2), (0, 1, 5)], 2, 28),
        ("path 3-vertex", [(0, 0, 1), (1, 1, 2), (2, 2, 3),
                           (0, 1, 0), (1, 2, 0)], 3, 30),
        ("star 4-vertex", [(0, 1, 0), (0, 2, 0), (0, 3, 0),
                           (1, 1, 1), (2, 2, 2), (3, 3, 3)], 4, 30),
    ]
    print(f"{'base graph':>16} {'Ham':>5} {'D':>4} {'n':>4} {'nullity':>8} "
          f"{'at ceiling?':>12} {'window inj.':>12}")
    for (nm, be, nV, n) in cases:
        hp, _ = has_hamiltonian_path(be, nV)
        D = true_span(be, nV, rng)
        deg = D // 2
        G = grid(n)
        if len(G) < deg:
            print(f"{nm:>16} {str(hp):>5} {D:>4} {n:>4} {'grid small':>8}")
            continue
        combos = list(itertools.combinations(range(len(G)), deg))
        rng.shuffle(combos)
        hit = None
        for combo in combos[:10]:
            roots = [G[i][1] for i in combo]
            res = prescribe(be, nV, n, roots, tries=14, D=D)
            if res is None:
                continue
            A, nul, minw, x = res
            if nul == D and minw > 1e-2:
                hit = (A, nul, minw)
                break
        if hit is None:
            print(f"{nm:>16} {str(hp):>5} {D:>4} {n:>4} "
                  f"{'no ceiling certificate found':>30}", flush=True)
            continue
        A, nul, minw = hit
        inj, r = window_injective(A, n, 0, D)
        print(f"{nm:>16} {str(hp):>5} {D:>4} {n:>4} {nul:>8} "
              f"{str(nul == D):>12} {str(inj):>12}", flush=True)
