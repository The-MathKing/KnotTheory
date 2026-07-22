"""
Why an EXACT (rational) certificate is hard for k >= 6, and how to look for one.

PROPOSITION.  Let A be a period-d matrix with RATIONAL weights on P(n,k), and
m = n/d.  The Fourier blocks M_l have entries in Q(zeta_m), and a Galois
automorphism sigma_j : zeta_m -> zeta_m^j sends M_l to M_{jl}.  If the weights
are rational then sigma_j fixes them, so

    det M_l = 0  ==>  det M_{jl} = 0  for every j coprime to m,

i.e. the set of singular blocks is a union of FULL Galois orbits of Gamma_m.

Consequently a rational certificate of nullity 2k+2 exists only if some
Galois-CLOSED root set of size k+1 is realisable.  At (k,d,n) = (6,3,72) all
eight such sets degenerate (a weight collapses), so no rational certificate
exists there.  This script (a) verifies the proposition numerically, and
(b) searches Galois-closed sets across many (n,d) for a realisable one.
"""
import itertools
import sys
from math import gcd

import numpy as np

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from period_d_blocks import blocks
from prescribe_symbol import solve_for, grid_interior
from verify_period_d_cert import verify
from galois_closed_sets import galois_closed_sets, interior_orbits


def verify_proposition(k, d, n, trials=6, seed=0):
    """With rational weights, is the singular-block set Galois stable?"""
    m = n // d
    rng = np.random.default_rng(seed)
    ok = True
    for _ in range(trials):
        w = np.round(rng.standard_normal(5 * d) * 6) / 3.0      # rational
        w[:3 * d] += np.sign(w[:3 * d] + 1e-9) * 1.0
        dets = np.array([np.real(np.linalg.det(M))
                         for M in blocks(w, n, k, d)])
        sc = max(np.abs(dets).max(), 1e-12)
        sing = set(np.flatnonzero(np.abs(dets) < 1e-9 * sc).tolist())
        for j in range(1, m):
            if gcd(j, m) != 1:
                continue
            img = {(j * l) % m for l in sing}
            if not img <= sing:
                ok = False
    return ok


if __name__ == "__main__":
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    print(f"Proposition check (k={k}): with rational weights, is the set of")
    print("singular blocks closed under the Galois action?")
    for (d, n) in ((3, 60), (3, 72), (4, 64)):
        # force some singular blocks by construction is hard with rational w;
        # instead confirm the STRUCTURAL claim on det values under sigma_j
        m = n // d
        rng = np.random.default_rng(1)
        w = np.round(rng.standard_normal(5 * d) * 6) / 3.0
        w[:3 * d] += np.sign(w[:3 * d] + 1e-9)
        dets = np.array([np.real(np.linalg.det(M)) for M in blocks(w, n, k, d)])
        bad = 0
        for j in range(1, m):
            if gcd(j, m) != 1:
                continue
            perm = np.array([dets[(j * l) % m] for l in range(m)])
            if np.abs(perm - dets).max() > 1e-8 * max(np.abs(dets).max(), 1):
                bad += 1
        print(f"  d={d} n={n} m={m}: det M_l is Galois-invariant as a multiset "
              f"-> {'YES' if bad == 0 else f'NO ({bad} failures)'}")

    print(f"\nSearch for a realisable Galois-closed root set, k={k}")
    print(f"{'d':>3} {'n':>5} {'m':>4} {'sets':>5} {'result':>34}")
    found = []
    for d in (3, 4, 5):
        for n in (60, 72, 80, 84, 90, 96, 108, 120):
            if n % d or (n // d + 1) // 2 - 1 < k + 1:
                continue
            m = n // d
            sets, _ = galois_closed_sets(m, k + 1)
            if not sets:
                print(f"{d:>3} {n:>5} {m:>4} {0:>5} "
                      f"{'no Galois-closed set of that size':>34}")
                continue
            G0 = grid_interior(m)
            best = "all degenerate"
            for (orders, ls) in sets:
                roots = [s for (l, s) in G0 if l in ls]
                w, err, _ = solve_for(n, k, d, roots, tries=12, push=0.0)
                if err > 1e-9:
                    continue
                okc, r, gap, minoff = verify(w, n, k, d, verbose=False)
                if okc:
                    best = f"REALISABLE {orders}"
                    found.append((d, n, orders, w))
                    break
            print(f"{d:>3} {n:>5} {m:>4} {len(sets):>5} {best:>34}", flush=True)
    print(f"\nrealisable Galois-closed sets found: {len(found)}")
    for (d, n, orders, w) in found:
        np.save(f"/Volumes/2TB/scifair/results/zero_forcing/"
                f"rational_cert_k{k}_d{d}_n{n}.npy", w)
        print(f"   k={k} d={d} n={n} orders={orders}")
