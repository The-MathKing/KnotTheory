"""
Log Entries 9 and 14 of manuscript/log.tex both found, empirically, that

    g_T(K) <= braid_index(K) - 1

holds with ZERO violations across the 2,953 KnotInfo knots (c <= 12) that
have both invariants tabulated. Before reporting this as a candidate
theorem, the literature was checked (see Log Entry 17). This script does
not compute Turaev genus itself (that requires a full Kauffman state-sum
over a diagram, which is out of scope here); instead it reproduces the
arithmetic that turns a cited, published closed-form result into an
explicit refutation, and cross-checks the formula's small cases against
our own KnotInfo data (which IS something this script can verify).

Citation: K. Jin, A. M. Lowrance, E. Polston, Y. Zheng, "On the Turaev
Genus of Torus Knots" (arXiv:1703.02506), Theorem/citation to Abe-Kishimoto
(2010) and Lowrance (2011):

    g_T(T_{3, 3n+i}) = n    for every n >= 0 and i in {0, 1, 2}.

Run: python verification/refute_turaev_braid_bound.py
"""
import os
from math import gcd

import pandas as pd


def crossing_number_torus(p, q):
    """Classical crossing number of T(p,q), p,q coprime: min(p(q-1), q(p-1))."""
    return min(p * (q - 1), q * (p - 1))


def braid_index_torus(p, q):
    """Classical fact (Schubert): braid index of T(p,q), p<q coprime, is p."""
    p, q = sorted((p, q))
    return p


def turaev_genus_T3q(n, i):
    """Abe-Kishimoto (2010) / Lowrance (2011), as cited in Jin-Lowrance-Polston-Zheng."""
    return n


print("STEP 1 -- cross-check the cited formula against our own KnotInfo data")
csv_path = "data/processed/knotinfo_invariants.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path, low_memory=False)
    # 8_19 = T(3,4) (n=1, i=1); 10_124 = T(3,5) (n=1, i=2)
    checks = [("8_19", 1, 1), ("10_124", 1, 2)]
    for name, n, i in checks:
        row = df[df["name"] == name]
        tabulated_gt = int(row["turaev_genus"].values[0])
        tabulated_braid = int(row["braid_index"].values[0])
        predicted_gt = turaev_genus_T3q(n, i)
        ok = tabulated_gt == predicted_gt
        print(f"  {name} = T(3,{3*n+i}): tabulated g_T={tabulated_gt}, "
              f"formula predicts g_T={predicted_gt}, braid index={tabulated_braid} "
              f"({'OK' if ok else 'MISMATCH'})")
        assert ok, f"cited formula disagrees with KnotInfo on {name}"
else:
    print("  (KnotInfo CSV not found -- skipping the cross-check step)")

print("\nSTEP 2 -- where does g_T(T_3,q) <= braid_index - 1 = 2 first fail?")
print(f"  {'n':>3}{'i':>3}{'q':>5}{'coprime':>9}{'crossings':>11}{'g_T':>6}{'braid_idx-1':>13}{'violates?':>11}")
first_violation = None
for n in range(0, 5):
    for i in (1, 2):  # i=0 gives q=3n, never coprime to 3 for n>=1
        q = 3 * n + i
        if q <= 3 or gcd(3, q) != 1:
            continue
        c = crossing_number_torus(3, q)
        b = braid_index_torus(3, q)
        gt = turaev_genus_T3q(n, i)
        violates = gt > b - 1
        if violates and first_violation is None:
            first_violation = (n, i, q, c, b, gt)
        print(f"  {n:>3}{i:>3}{q:>5}{'yes':>9}{c:>11}{gt:>6}{b-1:>13}{'YES' if violates else 'no':>11}")

assert first_violation is not None, "expected a violation by n=4 but found none"
n, i, q, c, b, gt = first_violation
print(f"\nFirst violation: T(3,{q}) (n={n}), {c} crossings, braid index {b}, g_T={gt}.")
print(f"g_T={gt} > braid_index-1={b-1}, so 'g_T(K) <= braid_index(K) - 1' is FALSE in general.")
print(f"KnotInfo tabulates knots only up to 12 crossings; T(3,{q}) has {c} crossings, which")
print("is why the empirical sweep in Log Entries 9 and 14 never encountered a violation.")
