"""
Search for pairwise DISJOINT forts in P(n,k).

Why this matters: any zero forcing set must intersect every fort. If F_1..F_t
are pairwise disjoint forts, a forcing set needs a distinct vertex in each, so
Z >= t. This is a lower-bound CERTIFICATE requiring no case analysis.

The open problem (arXiv 2607.19412) is exactly a lower bound valid for all
large n. If a disjoint family of size 2k+2 exists with uniform structure in n,
it would combine with the known Z <= 2k+2 to give Z = 2k+2 exactly.

Greedy construction: repeatedly take a MINIMUM fort avoiding all vertices used
so far (an ILP). Greedy need not be optimal, but if it already reaches 2k+2
that suffices -- we only need existence.
"""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from zero_forcing.zf import generalized_petersen
from zero_forcing.fort_ilp import min_fort_avoiding, is_zfs


def describe(F, n):
    """Render a fort bitmask as u/v labels."""
    out = []
    for v in range(2 * n):
        if (F >> v) & 1:
            out.append(f"u{v}" if v < n else f"v{v-n}")
    return "{" + ",".join(out) + "}"


def greedy_disjoint_forts(adj, n, limit=40):
    used, fam = 0, []
    for _ in range(limit):
        F = min_fort_avoiding(adj, used)
        if F is None or F == 0:
            break
        fam.append(F)
        used |= F
    return fam


def main():
    cases = [(10, 2, 6), (12, 2, 6), (14, 3, 8), (16, 3, 8), (18, 3, 8),
             (18, 4, 10), (20, 4, 10), (22, 4, 10), (23, 5, 12), (24, 5, 12)]
    for (n, k, Z) in cases:
        adj = generalized_petersen(n, k)
        t = time.time()
        fam = greedy_disjoint_forts(adj, n)
        sizes = sorted(bin(F).count("1") for F in fam)
        target = 2 * k + 2
        verdict = "REACHES 2k+2" if len(fam) >= target else f"short by {target-len(fam)}"
        print(f"P({n},{k}): Z={Z} target 2k+2={target} | disjoint forts found={len(fam)} "
              f"-> lower bound Z>={len(fam)}  [{verdict}]  sizes={sizes}  {time.time()-t:.1f}s",
              flush=True)
        for F in fam[:4]:
            print(f"      {describe(F, n)}", flush=True)


if __name__ == "__main__":
    main()
