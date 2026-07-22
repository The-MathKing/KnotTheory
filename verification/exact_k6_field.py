"""
Search for a k=6 certificate whose weights LIE IN a quadratic field, by
parametrising inside the field rather than hoping a generic solution lands there.

Two facts make this tractable.

(1) If the weights lie in K = Q(zeta_m)^H and the root set S is H-stable, then
    sigma in H sends det M_l to det M_{sigma l}, so the conditions come in
    H-ORBITS and one member of each orbit implies the rest.  For the realisable
    sets found at (k,d,n) = (6,3,72) that is 4 or 5 independent conditions, not 7.

(2) Writing each weight as w_j = p_j + q_j sqrt(D) gives 2*5d rational
    unknowns against those few conditions -- an enormous solution space.

So: fix all but a handful of the (p_j, q_j) at small rationals, solve the rest
at high precision, and test the result for rationality.  A rational solution
gives weights exactly in K, and the exact check in Q(zeta_m) then settles it.
"""
import sys
from fractions import Fraction

import mpmath as mp
import numpy as np

sys.path.insert(0, "/Volumes/2TB/scifair/verification")
from exact_certifier import Cyclo
from exact_subfield_verify import field_basis, det_exact, blocks_exact, to_field
from verify_period_d_cert import verify

k, d, n = 6, 3, 72
m = n // d


def h_orbit_reps(H, S):
    Hs = set()
    for h in H:
        Hs.add(h % m); Hs.add((-h) % m)
    seen, reps = set(), []
    for l in S:
        if l in seen:
            continue
        o = {min((h * l) % m, (-(h * l)) % m) for h in Hs} & set(S)
        seen |= o
        reps.append(l)
    return reps


def M_mp(pq, D, ell):
    """Block with weights p_j + q_j*sqrt(D), in mpmath."""
    sq = mp.sqrt(D)
    w = [pq[2 * j] + pq[2 * j + 1] * sq for j in range(5 * d)]
    b, c, e, aO, aI = (w[j * d:(j + 1) * d] for j in range(5))
    z = mp.expjpi(2 * mp.mpf(ell) / m)
    N = 2 * d
    M = mp.zeros(N, N)
    for r in range(d):
        M[r, r] += aO[r]; M[d + r, d + r] += aI[r]
        rp, de = (r + 1) % d, (r + 1) // d
        M[r, rp] += b[r] * z ** de; M[rp, r] += b[r] * mp.conj(z) ** de
        rq, dk = (r + k) % d, (r + k) // d
        M[d + r, d + rq] += e[r] * z ** dk
        M[d + rq, d + r] += e[r] * mp.conj(z) ** dk
        M[r, d + r] += c[r]; M[d + r, r] += c[r]
    return M


def run(H, S, D, prec=50, trials=60, seed=0):
    mp.mp.dps = prec
    reps = h_orbit_reps(H, S)
    nfree = len(reps)
    rng = np.random.default_rng(seed)
    print(f"H={H}  S={S}  K=Q(sqrt {D})")
    print(f"  {nfree} independent conditions (H-orbit representatives {reps})")
    pool = [Fraction(a, b) for a in range(-3, 4) for b in (1, 2, 3) if a]
    for t in range(trials):
        pq = [mp.mpf(0)] * (10 * d)
        base = [rng.choice(pool) for _ in range(10 * d)]
        for i, fr in enumerate(base):
            pq[i] = mp.mpf(fr.numerator) / fr.denominator
        free = sorted(rng.choice(10 * d, size=nfree, replace=False).tolist())

        def F(*xs):
            v = list(pq)
            for j, x in zip(free, xs):
                v[j] = x
            return [mp.re(mp.det(M_mp(v, D, l))) for l in reps]

        try:
            sol = mp.findroot(F, [pq[j] + mp.mpf(1) / 7 for j in free],
                              tol=mp.mpf(10) ** (-(prec - 10)))
        except Exception:
            continue
        v = list(pq)
        for j, x in zip(free, [sol[i] for i in range(nfree)]):
            v[j] = x
        # rationality test on the solved coordinates
        rats = []
        for j in free:
            rel = mp.pslq([v[j], mp.mpf(1)], maxcoeff=10**7, maxsteps=20000)
            rats.append(Fraction(-int(rel[1]), int(rel[0]))
                        if rel and rel[0] else None)
        if any(r is None for r in rats):
            continue
        for j, r in zip(free, rats):
            v[j] = mp.mpf(r.numerator) / r.denominator
        res = max(abs(mp.re(mp.det(M_mp(v, D, l)))) for l in S)
        wnum = np.array([float(v[2*j] + v[2*j+1] * mp.sqrt(D))
                         for j in range(5 * d)])
        ok, nul, gap, minoff = verify(wnum, n, k, d, verbose=False)
        print(f"  trial {t:>3}: all solved coords RATIONAL, residual "
              f"{mp.nstr(res,4)}, nullity {nul}, min|req| {minoff:.4f}"
              f"  {'REALISABLE' if ok else ''}", flush=True)
        if ok and res < mp.mpf(10) ** (-(prec - 15)):
            return v, wnum
    return None, None


if __name__ == "__main__":
    cases = [([1, 7], (1, 2, 3, 6, 7, 9, 10), 2),
             ([1, 5], (1, 2, 3, 5, 8, 9, 10), 6),
             ([1, 11], (1, 2, 3, 6, 8, 9, 11), 3)]
    for (H, S, D) in cases:
        v, wnum = run(H, S, D)
        if v is not None:
            print(f"\n*** rational-in-K solution found for H={H}, D={D} ***")
            np.save(f"/Volumes/2TB/scifair/results/zero_forcing/"
                    f"exactK_k6_D{D}.npy", wnum)
            break
        print()
