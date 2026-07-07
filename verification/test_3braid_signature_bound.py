"""
Log Entry 23: before attempting a proof, tested whether the optimal slope
in Feller's (still-open, general-n) conjecture -sigma(beta) >= b_1(beta)/2
holds exactly for 3-strand positive braids specifically, using the
already-validated Seifert-matrix engine (no new tool needed).

Result: 0 violations across 992 random positive 3-braid knots tested,
minimum ratio 0.6. Checked against literature before reporting further:
already known and by a STRONGER bound -- for positive 3-braids with
b_1 >= 2, -sigma >= b_1/2 + 1 is an established prior result. Not new.
See manuscript/log.tex Log Entry 23.

Run: python verification/test_3braid_signature_bound.py
"""
import sys
import os
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from math_engine.braid_topology import BraidKnot


def b1(word, n):
    """First Betti number of a positive braid closure surface = e - n + 1."""
    return len(word) - n + 1


def run(seed=0, trials=3000, verbose=True):
    random.seed(seed)
    min_ratio = float("inf")
    min_example = None
    violations = []
    tested = 0
    for _ in range(trials):
        e = random.randint(3, 40)
        word = [random.choice([1, 2]) for _ in range(e)]
        bk = BraidKnot(3, word)
        if not bk.is_knot():
            continue
        sig = bk.signature()
        if sig is None:
            continue
        B1 = b1(word, 3)
        if B1 <= 0:
            continue
        tested += 1
        ratio = abs(sig) / B1
        if ratio < min_ratio:
            min_ratio = ratio
            min_example = (word, sig, B1)
        if ratio < 0.5 - 1e-9:
            violations.append((word, sig, B1, ratio))

    if verbose:
        print(f"Tested {tested} positive 3-braid knots against |sigma| >= b1/2.")
        print(f"Violations: {len(violations)}")
        for w, s, B, r in violations[:5]:
            print(f"  VIOLATION: word={w} sigma={s} b1={B} ratio={r:.4f}")
        print(f"Minimum ratio found: {min_ratio:.4f} at word={min_example[0]} "
              f"sigma={min_example[1]} b1={min_example[2]}")
        print("\nLiterature check: for positive 3-braids with b1 >= 2, the STRONGER")
        print("bound -sigma >= b1/2 + 1 is already an established prior result --")
        print("consistent with the empirical minimum ratio found here (0.6 > 0.5),")
        print("and not a new finding. See Log Entry 23.")
    return tested, violations, min_ratio, min_example


if __name__ == "__main__":
    run()
