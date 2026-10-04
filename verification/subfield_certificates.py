"""
Exact certificates over a SUBFIELD: relaxing the rational obstruction.

Proposition (verification/rational_obstruction.py): if the period-d weights are
rational then sigma_j(det M_l) = det M_{jl}, so the set of singular blocks is a
union of full Galois orbits of Gamma_m.  Every Galois-closed set we tried at
k = 6 degenerates, so no RATIONAL certificate exists there.

But the same argument run over a subfield is weaker, and that is the opening.
Let G = (Z/m)^* / {+-1} act on Gamma_m.  If the weights lie in the fixed field
K = Q(zeta_m)^{H} of a SUBGROUP H <= G, then only sigma in H fix them, so the
singular set need only be H-stable -- a union of H-orbits.  H-orbits are smaller
than G-orbits, so there are strictly more admissible root sets, and the smaller
H is, the more freedom.  The price is that the weights live in a degree-[G:H]
extension of Q rather than in Q itself; for [G:H] = 2 that is a quadratic field,
where exact verification is still entirely routine.

This enumerates the subgroups H, forms the H-stable root sets of size k+1, and
tests each for realisability -- looking for the largest H (smallest field) that
admits a non-degenerate certificate.
"""

import os as _os
_REPO = _os.path.abspath(_os.path.join(
    _os.path.dirname(__file__), ".."))
import itertools
import sys
from math import gcd

import numpy as np

sys.path.insert(0, f"{_REPO}/verification")
from prescribe_symbol import solve_for, grid_interior
from verify_period_d_cert import verify


def galois_group(m):
    """(Z/m)^* modulo +-1, as a list of representatives."""
    units = [j for j in range(1, m) if gcd(j, m) == 1]
    seen, reps = set(), []
    for j in units:
        if j in seen:
            continue
        reps.append(j)
        seen.add(j); seen.add((-j) % m)
    return reps, units


def subgroups(m):
    """All subgroups of (Z/m)^*/{+-1}, as frozensets of representatives."""
    reps, units = galois_group(m)
    def norm(j):
        return min(j % m, (-j) % m)
    out = set()
    # generate by taking all subsets of generators up to size 3 (enough here)
    for r in range(0, 4):
        for gens in itertools.combinations(reps, r):
            H = {1}
            changed = True
            while changed:
                changed = False
                for a in list(H):
                    for g in gens:
                        v = norm(a * g)
                        if v not in H:
                            H.add(v); changed = True
            out.add(frozenset(H))
    return sorted(out, key=len, reverse=True)


def orbits(H, m):
    """H-orbits on the interior indices of Gamma_m."""
    G0 = grid_interior(m)
    idx = [l for (l, s) in G0]
    def norm(j):
        return min(j % m, (-j) % m)
    seen, out = set(), []
    for l in idx:
        if l in seen:
            continue
        o = sorted({norm(h * l) for h in H} & set(idx))
        if not o:
            continue
        seen |= set(o)
        out.append(tuple(o))
    return out


if __name__ == "__main__":
    k = int(sys.argv[1]); d = int(sys.argv[2]); n = int(sys.argv[3])
    tries = int(sys.argv[4]) if len(sys.argv) > 4 else 12
    m = n // d
    reps, units = galois_group(m)
    G0 = grid_interior(m)
    print(f"k={k} d={d} n={n} m={m}:  Galois group (Z/{m})*/(+-1) has order "
          f"{len(reps)}; representatives {reps}")
    print(f"{'|H|':>4} {'index':>6} {'H':>22} {'orbit sizes':>22} "
          f"{'sets':>5} {'result':>30}")
    best = None
    for H in subgroups(m):
        orb = orbits(H, m)
        sizes = [len(o) for o in orb]
        # unions of H-orbits totalling k+1
        good = []
        for r in range(1, len(orb) + 1):
            for combo in itertools.combinations(range(len(orb)), r):
                if sum(sizes[i] for i in combo) == k + 1:
                    good.append(tuple(sorted(l for i in combo for l in orb[i])))
        if not good:
            continue
        verdict = "all degenerate"
        for ls in good[:14]:
            roots = [s for (l, s) in G0 if l in ls]
            w, err, _ = solve_for(n, k, d, roots, tries=tries, push=0.0)
            if err > 1e-9:
                continue
            okc, r, gap, minoff = verify(w, n, k, d, verbose=False)
            if okc:
                verdict = f"REALISABLE  l={ls}"
                if best is None or len(H) > len(best[0]):
                    best = (set(H), ls, w, len(reps) // len(H))
                break
        print(f"{len(H):>4} {len(reps)//len(H):>6} {str(sorted(H)):>22} "
              f"{str(sizes):>22} {len(good):>5} {verdict:>30}", flush=True)
    if best:
        H, ls, w, index = best
        print(f"\nBEST: H of index {index} -> weights lie in a degree-{index} "
              f"field over Q")
        print(f"  root set l = {ls}")
        np.save(f"{_REPO}/results/zero_forcing/"
                f"subfield_cert_k{k}_d{d}_n{n}.npy", w)
    else:
        print("\nno H-stable realisable set found")
