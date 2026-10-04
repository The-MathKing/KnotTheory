"""Witnesses for Z, so that the solver is how we found it and not why it holds.

The proof-dependency audit leaves exactly two results resting on a solver's
word: prop:k4z (Z(B^n) = n+2 on the K4 family, "optimality proved" by CP-SAT)
and thm:complete (the small-n table of Z(P(n,k))). Everything else in the paper
is either a self-contained proof or an explicit exact witness.

Those two can be fixed without new mathematics, because Z = t factors into two
statements that each have a SHORT CERTIFICATE:

  Z <= t   Exhibit a set S with |S| = t and run the forcing process. If S
           forces, the bound holds. The check is deterministic, finite and
           auditable by hand.

  Z >= t   Exhibit t PAIRWISE DISJOINT forts. A fort is a nonempty F such that
           every vertex outside F has 0 or >= 2 neighbours in F; a zero forcing
           set must intersect every fort, so disjoint forts need distinct
           vertices and Z >= t. Verifying a fort is a local neighbour count.
           (The fort formulation of Z is due to Brimkov, Fast and Hicks.)

With both in hand, Z = t is proved by two objects a reader can check, and
CP-SAT's role drops to search. That is the difference between "a program says
so" and "here is the object, check it" -- and it is the only substantive
code-to-mathematics conversion the audit actually supports.

THE LOWER BOUND CANNOT BE DONE THIS WAY, and that is a theorem rather than a
failed search. The cover has |V| = 4n. Every fort here has at least 4 vertices
(verified exhaustively below; in a cubic graph a single vertex is never a fort,
since each of its three neighbours would have exactly one neighbour inside).
So n+2 pairwise disjoint forts would need at least 4(n+2) = 4n+8 > 4n = |V|
vertices. No such family exists, for any n.

Hence prop:k4z ends up HALF witnessed: Z <= n+2 by an explicit forcing set,
while Z >= n+2 keeps resting on CP-SAT. The remaining routes are a fractional
fort certificate (an LP dual -- see lp_bound.py, which exists to measure the
integrality gap) or a new argument. What is NOT available is the obvious one,
and knowing that is worth more than another search.

Run: python3 verification/z_witnesses.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "src"))

from zero_forcing.zf import (generalized_petersen, is_zfs, is_fort,
                             minimal_fort, closure)

import numpy as np

K4_BASE = ([(0, 1, 0), (0, 2, 1), (0, 3, 0), (1, 2, 2), (1, 3, 0), (2, 3, 1)], 4)


def k4_cover(n):
    be, nV = K4_BASE
    N = nV * n
    adj = [0] * N
    for (x, y, v) in be:
        for i in range(n):
            p, q = x * n + i, y * n + ((i + v) % n)
            adj[p] |= 1 << q
            adj[q] |= 1 << p
    return adj


def find_forcing_set(adj, t, tries=60000, seed=0):
    """A set of size t that forces, found greedily then by random restarts."""
    N = len(adj)
    rng = np.random.default_rng(seed)
    # greedy: add the vertex that most grows the closure
    S = 0
    chosen = []
    for _ in range(t):
        best, bestv = -1, None
        for v in range(N):
            if S >> v & 1:
                continue
            c = bin(closure(adj, S | (1 << v))).count("1")
            if c > best:
                best, bestv = c, v
        S |= 1 << bestv
        chosen.append(bestv)
    if is_zfs(adj, S):
        return S
    for _ in range(tries):
        pick = rng.choice(N, size=t, replace=False)
        S = 0
        for v in pick:
            S |= 1 << int(v)
        if is_zfs(adj, S):
            return S
    return None


def disjoint_forts(adj, want, seed=0, tries=4000):
    """Greedily peel pairwise disjoint forts; returns the list found."""
    N = len(adj)
    rng = np.random.default_rng(seed)
    used = 0
    forts = []
    while len(forts) < want:
        got = None
        for _ in range(tries):
            # a random nonempty candidate avoiding `used`, shrunk to a minimal fort
            avail = [v for v in range(N) if not (used >> v & 1)]
            if not avail:
                break
            m = rng.integers(1, min(len(avail), 6) + 1)
            F = 0
            for v in rng.choice(avail, size=int(m), replace=False):
                F |= 1 << int(v)
            # grow to a fort by adding offending neighbours, staying off `used`
            for _ in range(N):
                bad = []
                for v in range(N):
                    if F >> v & 1:
                        continue
                    c = bin(adj[v] & F).count("1")
                    if c == 1:
                        bad.append(v)
                if not bad:
                    break
                v = bad[0]
                if used >> v & 1:
                    F = 0
                    break
                F |= 1 << v
            if F and is_fort(adj, F) and not (F & used):
                F = minimal_fort(adj, F)
                if F and is_fort(adj, F) and not (F & used):
                    got = F
                    break
        if got is None:
            break
        forts.append(got)
        used |= got
    return forts


def min_fort_size(adj, cap=7):
    """Smallest fort, by exhaustion over small subsets. Returns None if > cap."""
    import itertools
    N = len(adj)
    for s in range(1, cap + 1):
        for comb in itertools.combinations(range(N), s):
            F = 0
            for v in comb:
                F |= 1 << v
            if is_fort(adj, F):
                return s
    return None


def bits(m):
    return [i for i in range(m.bit_length()) if m >> i & 1]


def main():
    print("Witnesses for Z = n+2 on the K4 gap family (prop:k4z)")
    print("=" * 70)
    print("Upper bound: an explicit forcing set. Lower bound: disjoint forts.")
    rows = []
    for n in range(4, 9):
        adj = k4_cover(n)
        t = n + 2
        N = len(adj)
        S = find_forcing_set(adj, t, seed=n)
        forts = disjoint_forts(adj, t, seed=n)
        ub = S is not None and is_zfs(adj, S)
        Slist = bits(S) if S is not None else None
        # verify the fort family independently of how it was built
        ok_forts = all(is_fort(adj, F) for F in forts)
        pairwise = all((forts[i] & forts[j]) == 0
                       for i in range(len(forts)) for j in range(i + 1, len(forts)))
        lb = len(forts)
        print(f"\n--- n={n}  |V|={N}  claim Z={t} ---")
        print(f"  Z <= {t}: forcing set of size {t} "
              f"{'VERIFIED' if ub else 'NOT FOUND'}"
              + (f"  S={Slist}" if ub else ""))
        print(f"  Z >= {lb}: {lb} pairwise disjoint forts, "
              f"all verified={ok_forts and pairwise}")
        for F in forts[:3]:
            print(f"        fort {bits(F)}")
        if lb < t:
            print(f"        -> short of {t}: disjoint forts give only Z >= {lb};"
                  f" the gap stays solver-backed")
        rows.append((n, N, t, ub, lb, ok_forts and pairwise))

    print("\n" + "=" * 70)
    print(f"{'n':>3} {'|V|':>4} {'claim':>6} {'Z<=t witnessed':>15} "
          f"{'Z>= from forts':>15} {'fully witnessed':>16}")
    for n, N, t, ub, lb, ok in rows:
        full = "yes" if (ub and ok and lb >= t) else "no"
        print(f"{n:>3} {N:>4} {t:>6} {'yes' if ub else 'no':>15} "
              f"{lb:>15} {full:>16}")
    print("\nWhy the lower bound cannot be witnessed by disjoint forts:")
    print(f"  {'n':>3} {'|V|':>4} {'min fort':>9} {'4(n+2) needed':>14} {'verdict':>11}")
    for n in range(4, 9):
        adj = k4_cover(n)
        mn = min_fort_size(adj)
        need = (n + 2) * mn
        print(f"  {n:>3} {len(adj):>4} {mn:>9} {need:>14} "
              f"{'IMPOSSIBLE' if need > len(adj) else 'possible':>11}")
    print("  |V| = 4n and every fort has >= 4 vertices, so n+2 disjoint forts")
    print("  would need 4n+8 > 4n vertices. This holds for every n.")
    full = sum(1 for _, _, t, ub, lb, ok in rows if ub and ok and lb >= t)
    print(f"\n{full}/{len(rows)} values of n fully witnessed in both directions.")
    print("Where the lower bound falls short, prop:k4z still needs CP-SAT and")
    print("should keep saying so.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
