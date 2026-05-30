"""
Exact topological engine for positive braid closures.

signature() implements the Seifert-matrix algorithm of J. Collins,
"An algorithm for computing the Seifert matrix of a link from a braid
representation" (2007), specialised to all-positive words (every crossing
right-handed). Given a braid word, it builds an explicit basis for
H_1(Seifert surface) from adjacent same-generator crossings and computes
their pairwise linking numbers case-by-case (Collins Sec. 3.1-3.3), then
reads the knot signature off the symmetrized Seifert form V + V^T.

This replaces an earlier version of this file whose signature routine was
restricted to 3-strand braids and, by construction, could only ever output
sigma = -(e - 2) -- i.e. it algebraically forced |s| = |sigma| for every
input and was incapable of finding a signature defect. See
verification/refute_3braid_claim.py and manuscript/log.tex Log Entry 16 for
the audit that found this.

The new implementation is validated in `self_test()` below against:
  (a) the closed-form Brieskorn/Hirzebruch signature of 34 torus knots
      T(p,q), 2 <= p <= 6, spanning strand counts n = p = 2..6, and
  (b) all 17 knots in KnotInfo (<=12 crossings) that carry an authentic
      positive-braid word in their `positive_braid_notation` column.
Both checks must pass with zero mismatches before this module is used.
"""
import numpy as np


class BraidKnot:
    """
    num_strands: int (n)
    word: list of POSITIVE integers in {1, ..., n-1}, e.g. [1, 1, 2, 1, 2]
          for sigma_1^2 sigma_2 sigma_1 sigma_2. Only positive (right-handed)
          crossings are supported -- this engine is for positive braids.
    """

    def __init__(self, num_strands, word):
        self.n = num_strands
        self.word = list(word)
        self.crossing_number = len(word)

    def is_knot(self):
        """True iff the closed braid has exactly 1 component."""
        perm = list(range(self.n))
        for gen in self.word:
            idx = gen - 1
            if idx < 0 or idx >= self.n - 1:
                return False
            perm[idx], perm[idx + 1] = perm[idx + 1], perm[idx]
        visited = [False] * self.n
        num_cycles = 0
        for i in range(self.n):
            if not visited[i]:
                num_cycles += 1
                curr = i
                while not visited[curr]:
                    visited[curr] = True
                    curr = perm[curr]
        return num_cycles == 1

    def rasmussen_s(self):
        """For positive braids, s(K) = 2g_4(K) = 2g_3(K) = e(beta) - n + 1
        (Rasmussen 2010 / Kronheimer-Mrowka 1993 slice-Bennequin equality)."""
        if all(x > 0 for x in self.word):
            return len(self.word) - self.n + 1
        return None

    def seifert_genus(self):
        if all(x > 0 for x in self.word):
            return (len(self.word) - self.n + 1) / 2.0
        return None

    def seifert_matrix(self):
        """Collins (2007) algorithm, Sec. 3.1-3.3, specialised to an
        all-positive word (every x_i > 0, so every crossing is right-handed).
        Returns the Seifert matrix M as a numpy array."""
        word = self.word
        l = len(word)
        x = [None] + word  # 1-indexed to match the paper's convention
        h = [0] * (l + 1)
        for i in range(1, l + 1):
            hi = 0
            for j in range(i + 1, l + 1):
                if x[j] == x[i]:
                    hi = j
                    break
            h[i] = hi

        gens = [i for i in range(1, l + 1) if h[i] != 0]
        idx = {g: k for k, g in enumerate(gens)}
        m = len(gens)
        M = np.zeros((m, m))

        for i in gens:
            M[idx[i], idx[i]] = -1.0  # both crossings of the generator are positive

        for a in range(m):
            i = gens[a]
            for b in range(a + 1, m):
                j = gens[b]
                if h[i] > h[j] or h[j] == 0:
                    continue  # Case 1: no interaction
                elif h[i] < j:
                    continue  # Case 2: generator i closes before j opens
                elif h[i] == j:
                    # Case 3: shared crossing; x_j > 0 always (positive braid)
                    M[idx[j], idx[i]] += 1.0
                else:
                    # Case 4/5: i < j < h(i) < h(j) -- interleaved generators
                    diff = x[i] - x[j]
                    if abs(diff) > 1:
                        continue  # Case 4: strands not adjacent
                    elif diff == -1:
                        M[idx[i], idx[j]] += 1.0
                    elif diff == 1:
                        M[idx[j], idx[i]] += -1.0
        return M

    def signature(self):
        """Knot signature sigma(K) = sign(V + V^T) for the Seifert matrix V."""
        if not all(x > 0 for x in self.word):
            return None
        M = self.seifert_matrix()
        if M.shape[0] == 0:
            return 0
        S = M + M.T
        eig = np.linalg.eigvalsh(S)
        pos = int(np.sum(eig > 1e-7))
        neg = int(np.sum(eig < -1e-7))
        return pos - neg


def evaluate_braid_defect(word, n):
    bk = BraidKnot(n, word)
    if not bk.is_knot():
        return None
    s = bk.rasmussen_s()
    sig = bk.signature()
    g3 = bk.seifert_genus()
    if s is None or sig is None:
        return None
    return {
        "word": word,
        "n": n,
        "crossings": len(word),
        "s": s,
        "sig": sig,
        "g3": g3,
        "defect": abs(s) - abs(sig),
    }


# ---------------------------------------------------------------------------
# Self-test / validation harness. Run directly: python braid_topology.py
# ---------------------------------------------------------------------------

def _sigma_torus_closed_form(p, q):
    """Brieskorn/Hirzebruch closed form for the signature of the torus knot
    T(p,q): each eigenvalue of the symmetrized Seifert form is indexed by
    (i,j), 1<=i<p, 1<=j<q, and is negative iff i/p + j/q (mod 2) in (1/2,3/2)."""
    return sum(
        -1 if 0.5 < (i / p + j / q) % 2 < 1.5 else 1
        for i in range(1, p) for j in range(1, q)
    )


def _torus_word(p, q):
    return list(range(1, p)) * q


def self_test(verbose=True):
    from math import gcd
    failures = []

    # (a) torus knots against the closed-form Brieskorn/Hirzebruch signature
    torus_tested = 0
    for p in range(2, 7):
        for q in range(2, 14):
            if gcd(p, q) != 1:
                continue
            torus_tested += 1
            truth = _sigma_torus_closed_form(p, q)
            got = BraidKnot(p, _torus_word(p, q)).signature()
            if got != truth:
                failures.append(f"T({p},{q}): truth={truth} got={got}")

    # (b) all KnotInfo knots with an authentic positive-braid word
    import os
    import ast
    knotinfo_tested = 0
    csv_path = os.path.join(os.path.dirname(__file__), "..", "..",
                             "data", "processed", "knotinfo_invariants.csv")
    if os.path.exists(csv_path):
        import pandas as pd
        df = pd.read_csv(csv_path, low_memory=False)
        pbn = df["positive_braid_notation"].astype(str)
        real = df[pbn.str.startswith("[")]
        for _, row in real.iterrows():
            word = ast.literal_eval(row["positive_braid_notation"])
            n = max(word) + 1
            truth = int(float(row["signature"]))
            got = BraidKnot(n, word).signature()
            knotinfo_tested += 1
            if got != truth:
                failures.append(f"{row['name']}: truth={truth} got={got}")

    if verbose:
        print(f"Torus-knot validation: {torus_tested} knots tested, "
              f"{sum(1 for f in failures if f.startswith('T('))} mismatches.")
        print(f"KnotInfo positive-braid validation: {knotinfo_tested} knots tested, "
              f"{sum(1 for f in failures if not f.startswith('T('))} mismatches.")
        for f in failures:
            print("  MISMATCH:", f)
        print("PASSED" if not failures else "FAILED")
    return not failures


if __name__ == "__main__":
    ok = self_test()
    raise SystemExit(0 if ok else 1)
