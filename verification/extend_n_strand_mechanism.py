"""
Log Entry 21: after checking the n>=4 conjecture (Log Entry 20) against
literature (Baader-Feller-Lewark-Zentner, arXiv:1610.04534 -- same
technique, different specific word, confirming this is active mature
territory, not open) and recalibrating from "prove a new theorem" to
"understand and honestly characterize what is true," this script extends
the computational verification and checks the specific structural claim:
that the period-2-vs-period-(n-1) split corresponds exactly to the parity
of n, and that for every odd n the g_T(D) sequence is IDENTICAL to the
n=3 formula floor((k-(n-1))/2), independent of n.

This is evidence for a candidate mechanism (checkerboard-color matching of
the two ends of the generator chain at the wraparound step), not a proof.
See Log Entry 21 for the honest statement of what is and is not proven.

Run: python verification/extend_n_strand_mechanism.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from math_engine.turaev_diagram import turaev_genus_of_diagram


def cyclic_word(k, ngens):
    return [(i % ngens) + 1 for i in range(k)]


print("STEP 1 -- period vs parity of n, n=3..15")
mismatches = 0
for n in range(3, 16):
    ngens = n - 1
    vals = []
    for k in range(ngens, ngens + 50):
        w = cyclic_word(k, ngens)
        gt, _, _ = turaev_genus_of_diagram(w, n)
        vals.append(gt)
    diffs = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
    tail = diffs[10:]
    period = None
    for p in range(1, 15):
        if all(tail[i] == tail[i % p] for i in range(len(tail) - p)):
            period = p
            break
    predicted = 2 if n % 2 == 1 else ngens
    ok = period == predicted
    if not ok:
        mismatches += 1
    print(f"  n={n:3d}  n odd={n%2==1}  measured period={period}  "
          f"predicted (2 if n odd else n-1)={predicted}  {'OK' if ok else 'MISMATCH'}")
print(f"  {mismatches} mismatches out of 13 values of n tested.")

print("\nSTEP 2 -- for odd n, is the sequence IDENTICAL to floor((k-(n-1))/2)?")
mismatches2 = 0
for n in [5, 7, 9, 11, 13, 15]:
    ngens = n - 1
    for k in range(ngens, ngens + 16):
        w = cyclic_word(k, ngens)
        gt, _, _ = turaev_genus_of_diagram(w, n)
        predicted = (k - ngens) // 2
        if gt != predicted:
            mismatches2 += 1
            print(f"  MISMATCH n={n} k={k}: predicted {predicted}, got {gt}")
print(f"  {mismatches2} mismatches across 6 odd values of n, 16 values of k each.")

print("\n" + ("ALL CHECKS PASSED" if mismatches == 0 and mismatches2 == 0 else "SOME CHECKS FAILED"))
print("\nReminder: this verifies the CONJECTURE and its proposed mechanism computationally.")
print("It is not a substitute for the multi-lap induction that would make this a proof")
print("(see Log Entry 21's 'Honest status' paragraph).")
