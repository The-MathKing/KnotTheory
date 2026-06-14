"""
Log Entry 20: exploratory (NOT a proof) check of whether Log Entry 18's
n=3 closed form for cyclic-alternation braid diagrams generalizes to more
strands. Reports the period and growth rate of g_T(D) for n = 3..9,
generators cycling 1,2,...,n-1,1,2,... . Explicitly flagged in the log as
a conjecture with computational support only -- not checked against
literature with the rigor applied elsewhere in this project, and not
proved for n >= 5.

Run: python verification/explore_n_strand_pattern.py
"""
import sys
import os
from math import gcd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from math_engine.turaev_diagram import turaev_genus_of_diagram


def cyclic_word(k, ngens):
    return [(i % ngens) + 1 for i in range(k)]


print(f"{'n':>3}{'ngens':>7}{'period':>8}{'sum/period':>12}{'growth=floor(ngens/2)/ngens':>30}")
for n in range(3, 10):
    ngens = n - 1
    vals = []
    for k in range(ngens, ngens + 30):
        w = cyclic_word(k, ngens)
        gt, _, _ = turaev_genus_of_diagram(w, n)
        vals.append(gt)
    diffs = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
    tail = diffs[6:]
    period = None
    for p in range(1, 12):
        if all(tail[i] == tail[i % p] for i in range(len(tail) - p)):
            period = p
            break
    s = sum(tail[:period]) if period else None
    predicted_rate = (ngens // 2) / ngens
    actual_rate = s / period if period else None
    match = "OK" if period and abs(actual_rate - predicted_rate) < 1e-9 else "?"
    print(f"{n:>3}{ngens:>7}{period:>8}{s:>12.1f}{predicted_rate:>30.4f}  [{match}]")

print("\nThis is exploratory evidence for a conjecture (see manuscript/log.tex")
print("Log Entry 20), not a proof, and has not been checked against the")
print("literature with the same rigor as Log Entries 17 and 19.")
