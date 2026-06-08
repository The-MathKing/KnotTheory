"""
Computes the Turaev genus of the STANDARD closed-braid diagram of a braid
word: g_T(D) = (c(D) + 2 - |s_A(D)| - |s_B(D)|) / 2, where s_A(D) and s_B(D)
are the circle counts of the all-A and all-B Kauffman states of D (Turaev
1987; see Champanerkar-Kofman-Stoltzfus for a survey, and Jin-Lowrance-
Polston-Zheng arXiv:1703.02506 Eq. 2.1, which this module's formula matches).

Because g_T(K) = min over ALL diagrams D of K of g_T(D), this module gives
an UPPER BOUND on the true Turaev genus of the knot, not the true value --
it can equal the true value (the diagram happens to be genus-minimizing) or
exceed it, but by definition can never be strictly less than it. That
mathematical fact is exactly what self_test() checks at scale: sampling
600 real KnotInfo knots, it must never see g_T(diagram) < tabulated g_T(K).

Algorithm: a positive crossing's A-resolution is the identity ("pass
through": strands i, i+1 stay in their tracks) and its B-resolution is the
Temperley-Lieb cap-cup generator e_i (this is the standard fact that, for a
crossing whose sign is positive with respect to some orientation, the
A-smoothing coincides with the oriented/Seifert smoothing -- see e.g.
Lickorish, "An Introduction to Knot Theory," Ch. 3). For a negative
crossing the roles are swapped. Composing a sequence of "pass"/"cap-cup"
operations along a braid word, then closing the braid (identifying bottom
position j with top position j for every j), and counting the resulting
number of connected components via a union-find over every node the
composition ever creates, gives the circle count of that Kauffman state.
This is exactly Temperley-Lieb diagram composition; it is validated below
against alternating knots (where g_T must be exactly 0, a strong two-sided
check since it depends on both s_A and s_B being computed correctly
simultaneously) and against 600 knots with a real tabulated braid word.
"""
import os
import ast
import random


class _DSU:
    __slots__ = ("parent",)

    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.parent[rx] = ry


def _state_circles(word, n, resolution):
    """resolution(sign) -> 'pass' or 'cap', for a crossing of the given sign."""
    dsu = _DSU()
    top = [("TOP", j) for j in range(n)]
    for t in top:
        dsu.find(t)
    frontier = list(top)
    fresh = [0]
    for gen in word:
        idx = abs(gen) - 1
        sign = 1 if gen > 0 else -1
        i, ip1 = idx, idx + 1
        if resolution(sign) == "pass":
            continue
        dsu.union(frontier[i], frontier[ip1])
        fresh[0] += 1
        z = ("Z", fresh[0])
        dsu.find(z)
        frontier[i] = z
        frontier[ip1] = z
    for j in range(n):
        dsu.union(frontier[j], top[j])
    roots = {dsu.find(x) for x in dsu.parent}
    return len(roots)


def s_A(word, n):
    """Circle count of the all-A Kauffman state of the standard braid diagram."""
    return _state_circles(word, n, lambda sign: "pass" if sign > 0 else "cap")


def s_B(word, n):
    """Circle count of the all-B Kauffman state of the standard braid diagram."""
    return _state_circles(word, n, lambda sign: "cap" if sign > 0 else "pass")


def turaev_genus_of_diagram(word, n):
    """Returns (g_T(D), s_A(D), s_B(D)) for the standard closed-braid diagram
    of `word` on `n` strands. This is an upper bound on g_T(K)."""
    c = len(word)
    sa, sb = s_A(word, n), s_B(word, n)
    return (c + 2 - sa - sb) / 2, sa, sb


def self_test(verbose=True, sample_size=600, seed=0):
    failures = []

    # (a) alternating knots must give g_T(D) = 0 exactly, both directions at once
    alternating_cases = [
        ("Hopf link", [1, 1], 2, 0),
        ("Trefoil", [1, 1, 1], 2, 0),
        ("Figure-8", [1, -2, 1, -2], 3, 0),
    ]
    for name, word, n, expected in alternating_cases:
        gt, sa, sb = turaev_genus_of_diagram(word, n)
        if gt != expected:
            failures.append(f"{name}: expected g_T={expected}, got {gt} (sa={sa}, sb={sb})")

    # (b) upper-bound sanity across real KnotInfo braid words: g_T(D) must
    #     NEVER be strictly less than the tabulated (minimized) true value.
    n_tested = n_tight = n_impossible = 0
    csv_path = os.path.join(os.path.dirname(__file__), "..", "..",
                             "data", "processed", "knotinfo_invariants.csv")
    if os.path.exists(csv_path):
        import pandas as pd
        df = pd.read_csv(csv_path, low_memory=False)
        df["_tg"] = pd.to_numeric(df["turaev_genus"], errors="coerce")
        bn = df["braid_notation"].astype(str)
        sub = df[bn.str.startswith("[") & df["_tg"].notna()]
        idxs = list(sub.index)
        random.Random(seed).shuffle(idxs)
        for i in idxs[:sample_size]:
            row = df.loc[i]
            try:
                word = ast.literal_eval(row["braid_notation"])
                if not all(isinstance(x, int) for x in word):
                    continue
            except Exception:
                continue
            n = max(abs(x) for x in word) + 1
            true_gt = row["_tg"]
            gt, _, _ = turaev_genus_of_diagram(word, n)
            n_tested += 1
            if gt == true_gt:
                n_tight += 1
            elif gt < true_gt:
                n_impossible += 1
                failures.append(f"{row['name']}: diagram g_T={gt} < tabulated true g_T={true_gt} "
                                 f"(mathematically impossible if correct)")

    if verbose:
        print(f"Alternating-knot check: {len(alternating_cases)} cases, "
              f"{sum(1 for f in failures if 'g_T=' in f and 'expected' in f)} mismatches.")
        print(f"KnotInfo upper-bound check: {n_tested} knots with a real braid word and "
              f"tabulated Turaev genus, {n_tight} exactly tight, {n_impossible} impossible "
              f"(g_T(diagram) < true g_T -- must be 0 for a correct implementation).")
        for f in failures:
            print("  FAIL:", f)
        print("PASSED" if not failures else "FAILED")
    return not failures


if __name__ == "__main__":
    ok = self_test()
    raise SystemExit(0 if ok else 1)
