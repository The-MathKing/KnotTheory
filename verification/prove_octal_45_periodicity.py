"""
Periodicity of the octal game 0.45: the correct argument, and an audit.

STATUS.  This game is NOT open.  A. Flammenkamp's octal-game database
lists .45 in its table of "Nontrivial Octal-Games with known Structure"
with period 20, preperiod 498, and a "solved" date of 1956 -- i.e. it was
settled by Guy and Smith in the paper that introduced the notation.  An
earlier version of this file presented a bespoke argument (a bounded value
set S = {1,2,4,7,8}, a ten-index exceptional set R, and an XOR-closure
lemma) with one gap left open.  That whole apparatus is unnecessary: the
Guy-Smith shift argument below closes the game completely and uses none of
it.  Both facts -- that the game was already solved, and that the standard
theorem settles it in half a page -- are recorded in manuscript/octal_log.tex.

THE ARGUMENT (Guy-Smith periodicity theorem, specialised to 0.45).

Rules.  From a heap of n: (i) remove 1 token and split the remaining n-1
into two nonempty heaps (needs n >= 3); (ii) remove 2 tokens, either
ending the heap outright (only when n = 2) or splitting the remaining n-2
into two nonempty heaps (needs n >= 4).  So for n >= 4,

    Reach(n) = { G(a)^G(b) : a+b = n-i, a,b >= 1, i in {1,2} },
    G(n)     = mex Reach(n).

Note the game has no move leaving exactly one heap, and its largest
nonzero code digit has index t = 2.

Let l = 20 and p = 498, and suppose G(m) = G(m-l) has been verified for
every m with p+l <= m <= 2p+2l+t.  Let n > 2p+2l+t and assume inductively
that G(m) = G(m-l) for all p+l <= m < n.  Then Reach(n) = Reach(n-l):

  (subset)  Let a+b = n-i with a <= b, a,b >= 1.  Then
            b >= (n-i)/2 >= (n-t)/2 >= p+l, and b <= n-i-1 < n, so the
            inductive hypothesis gives G(b) = G(b-l).  Also b-l >= p >= 1.
            Hence {a, b-l} is a pair of nonempty heaps summing to
            (n-l)-i with G(a)^G(b-l) = G(a)^G(b).  (No ordering condition
            is needed: a pair of heaps is unordered.)

  (superset) Let a+b = (n-l)-i with a <= b, a,b >= 1.  Then
            b >= (n-l-i)/2 >= p, and b+l <= n-i-1 < n, so the inductive
            hypothesis gives G(b+l) = G(b).  Hence {a, b+l} sums to n-i
            with the same XOR.

  The terminal move (ii) contributes the value 0 only at n = 2, and
  neither n nor n-l equals 2 in this range, so no asymmetry arises.

Equal reachable sets have equal mex, so G(n) = G(n-l), completing the
induction.  With p = 498, l = 20, t = 2 the finite verification runs only
to 2p+2l+t = 1038.

This script checks: the finite hypothesis window; the two inclusions of
the shift argument directly, pair by pair; that the last exception to
G(n) = G(n-20) is at n = 517 (so 498 is exactly the preperiod); and
Flammenkamp's four tabulated statistics for .45, as an engine validation.

Run: python verification/prove_octal_45_periodicity.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from octal_games.grundy import grundy_sequence

CODE, PERIOD, PREPERIOD, T_LAST = "0.45", 20, 498, 2
GS_BOUND = 2 * PREPERIOD + 2 * PERIOD + T_LAST      # 1038


def reachable(G, n):
    s = set()
    for i in (1, 2):
        rem = n - i
        if rem == 0:
            s.add(0)                                 # remove the whole heap
        for a in range(1, rem // 2 + 1):
            s.add(G[a] ^ G[rem - a])
    return s


def self_test(N=20000, verbose=True):
    G = grundy_sequence(CODE, N)
    p, l, t = PREPERIOD, PERIOD, T_LAST
    fail = []

    # 1. the finite hypothesis window of the Guy-Smith theorem
    window_ok = all(G[n] == G[n - l] for n in range(p + l, GS_BOUND + 1))
    if not window_ok:
        fail.append(f"hypothesis window [{p+l},{GS_BOUND}] fails")

    # 2. 498 is exactly the preperiod: last exception is at n = 517
    exc = [n for n in range(l, N + 1) if G[n] != G[n - l]]
    if max(exc) != p + l - 1:
        fail.append(f"last exception at {max(exc)}, expected {p+l-1}")

    # 3. the two inclusions of the shift argument, checked pair by pair
    #    on every n in a band above the bound (the inductive step's claim)
    for n in range(GS_BOUND + 1, GS_BOUND + 120):
        for i in (1, 2):
            for a in range(1, (n - i) // 2 + 1):
                b = n - i - a
                if not (b >= p + l and b - l >= 1):
                    fail.append(f"subset step invalid at n={n}, i={i}, a={a}")
                    break
                if G[b] != G[b - l]:
                    fail.append(f"IH fails for b={b}")
                    break
            for a in range(1, (n - l - i) // 2 + 1):
                b = n - l - i - a
                if not (b >= p and b + l <= n - i - 1):
                    fail.append(f"superset step invalid at n={n}, i={i}, a={a}")
                    break
                if G[b + l] != G[b]:
                    fail.append(f"IH fails for b+l={b+l}")
                    break
        if reachable(G, n) != reachable(G, n - l):
            fail.append(f"Reach({n}) != Reach({n-l})")

    # 4. engine validation against Flammenkamp's tabulated statistics for .45
    rare = [n for n in range(N + 1) if bin(G[n]).count("1") % 2 == 0]
    stats = {"rare": (len(rare), 11), "miss": (len(exc), 67),
             "last+t": (max(rare) + t, 200), "maxG": (max(G), 8)}
    for name, (got, want) in stats.items():
        if got != want:
            fail.append(f"statistic {name}: got {got}, table says {want}")

    if verbose:
        print(f"Guy-Smith bound 2p+2l+t = 2*{p}+2*{l}+{t} = {GS_BOUND}")
        print(f"hypothesis window G(n)=G(n-{l}) for {p+l} <= n <= {GS_BOUND}: "
              f"{'PASS' if window_ok else 'FAIL'}")
        print(f"last exception to G(n)=G(n-{l}) up to N={N}: n={max(exc)} "
              f"(so the preperiod is exactly {max(exc)-l+1}) -- "
              f"{'PASS' if max(exc)==p+l-1 else 'FAIL'}")
        print(f"shift argument, both inclusions, every pair, "
              f"n in [{GS_BOUND+1},{GS_BOUND+119}]: "
              f"{'PASS' if not any('step' in f or 'Reach' in f for f in fail) else 'FAIL'}")
        print("engine validation against Flammenkamp's .45 row:")
        for name, (got, want) in stats.items():
            print(f"   {name:>7}: computed {got:>4}   table {want:>4}   "
                  f"{'match' if got == want else 'MISMATCH'}")
        for f in fail:
            print("  FAIL:", f)
        print("\nALL CHECKS PASSED" if not fail else "\nSOME CHECKS FAILED")
    return not fail


if __name__ == "__main__":
    raise SystemExit(0 if self_test() else 1)
