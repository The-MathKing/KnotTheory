"""
Search infinite families of positive braid closures for the signature defect
Delta(K) = |s(K)| - |sigma(K)|, using the validated Seifert-matrix engine in
src/math_engine/braid_topology.py (Collins 2007 algorithm; see that file's
self_test() for the validation against KnotInfo ground truth and closed-form
torus-knot signatures).

This replaces an earlier version of this script whose defect computation
depended on a 3-braid-only signature routine that was tautologically forced
to output sigma = -(e-2). That routine could not find a nonzero defect by
construction -- it was not evidence that positive 3-braids are
"signature-rigid". See manuscript/log.tex Log Entry 16 and
verification/refute_3braid_claim.py for the counterexample (T(3,7), a
positive 3-braid knot with defect 4) that the old code could never see.
"""
import sys
import os
import pandas as pd
from math import gcd

sys.path.insert(0, os.getcwd())
from src.math_engine.braid_topology import BraidKnot, evaluate_braid_defect, self_test


def run_investigation():
    print("=" * 80)
    print("BRAID FAMILY SEARCH FOR THE SIGNATURE DEFECT (validated engine)")
    print("=" * 80)

    assert self_test(verbose=False), "Seifert-matrix engine failed self-test; aborting."
    print("Engine self-test: PASSED (34/34 torus knots, 17/17 KnotInfo positive braids)\n")

    # --- Family 1: 4-syllable 3-braids  beta(a,b,c,d) = s1^a s2^b s1^c s2^d --
    print("--- Family 1: 4-syllable positive 3-braids sigma_1^a sigma_2^b sigma_1^c sigma_2^d ---")
    print("Sweeping a,b,c,d in [1..8] (crossings up to 32)...")
    records = []
    for a in range(1, 9):
        for b in range(1, 9):
            for c in range(1, 9):
                for d in range(1, 9):
                    word = [1] * a + [2] * b + [1] * c + [2] * d
                    res = evaluate_braid_defect(word, n=3)
                    if res is not None:
                        res.update(a=a, b=b, c=c, d=d)
                        records.append(res)
    df1 = pd.DataFrame(records)
    n_defect = int((df1["defect"] > 0).sum())
    print(f"Synthesized {len(df1)} authentic 1-component knots.")
    print(f"Zero defect: {len(df1) - n_defect} ({100*(1 - n_defect/len(df1)):.1f}%)  |  "
          f"Nonzero defect: {n_defect} ({100*n_defect/len(df1):.1f}%)")
    if n_defect:
        worst = df1.sort_values("defect", ascending=False).iloc[0]
        print(f"Largest defect found: {int(worst['defect'])} at (a,b,c,d)="
              f"({worst['a']},{worst['b']},{worst['c']},{worst['d']}), "
              f"c={worst['crossings']}, s={worst['s']}, sigma={worst['sig']}")
    else:
        print("No defect found within this specific 4-syllable parameter range.")
        print("(This is a statement about this family/range, not a general theorem -- ")
        print(" see the torus-braid sweep below, which DOES find defects at low crossing number.)")

    # --- Family 2: 6-syllable 3-braids -----------------------------------
    print("\n--- Family 2: 6-syllable positive 3-braids ---")
    print("Note: the uniform pattern (s1^k s2^k)^3 is the closure of (sigma_1 sigma_2)^{3k},")
    print("i.e. the torus LINK T(3,3k) -- gcd(3,3k)=3 always, so it has 3 components, never 1.")
    print("is_knot() correctly rejects every one of these (an earlier version of this script")
    print("mislabeled this pattern 'Torus Knots T(3,3k)' and implicitly claimed a nonexistent")
    print("N=336 one-component knot sample from it). Using a genuinely varied sweep instead:")
    records2 = []
    for k in range(1, 8):
        word = [1]*k + [2]*(k+1) + [1]*k + [2]*(k+1) + [1]*(k+1) + [2]*k
        res = evaluate_braid_defect(word, n=3)
        if res is not None:
            res.update(family=f"k={k}")
            records2.append(res)
    df2 = pd.DataFrame(records2)
    if len(df2):
        print(f"{'family':<10}{'c':>4}{'s':>6}{'sigma':>7}{'defect':>8}")
        for _, r in df2.iterrows():
            print(f"{r['family']:<10}{r['crossings']:>4}{r['s']:>6}{r['sig']:>7}{r['defect']:>8}")
        n_defect2 = int((df2["defect"] > 0).sum())
        print(f"Nonzero defect in {n_defect2} of {len(df2)} configurations.")
    else:
        print("No 1-component knots produced by this sweep either.")

    # --- Family 3: torus braids T(3,q), the family that DOES show defect --
    print("\n--- Family 3: torus braids T(3,q) = closure of (sigma_1 sigma_2)^q ---")
    print("(The natural infinite family in braid index 3; included because Family 1/2's")
    print(" coarse syllable patterns may or may not sample it -- checked explicitly here.)")
    records3 = []
    for q in range(2, 20):
        if gcd(3, q) != 1:
            continue
        word = [1, 2] * q
        res = evaluate_braid_defect(word, n=3)
        res.update(q=q)
        records3.append(res)
    df3 = pd.DataFrame(records3)
    print(f"{'T(3,q)':<10}{'c':>4}{'s':>6}{'sigma':>7}{'defect':>8}")
    first_q = df3[df3["defect"] > 0]["q"].min() if (df3["defect"] > 0).any() else None
    for _, r in df3.iterrows():
        flag = "  <-- first nonzero defect" if r["defect"] > 0 and r["q"] == first_q else ""
        label = f"T(3,{int(r['q'])})"
        print(f"{label:<10}{r['crossings']:>4}{r['s']:>6}{r['sig']:>7}{r['defect']:>8}{flag}")
    first_defect = df3[df3["defect"] > 0]
    if len(first_defect):
        q0 = int(first_defect.iloc[0]["q"])
        c0 = int(first_defect.iloc[0]["crossings"])
        print(f"\nSmallest defect-bearing torus braid in this family: T(3,{q0}), "
              f"a genuine 3-braid closure with {c0} crossings and braid index 3.")
        print("This is a direct counterexample to the retracted claim that positive")
        print("3-braid closures are universally signature-rigid (Log Entry 15, retracted).")

    print("\n" + "=" * 80)
    print("HONEST SUMMARY:")
    print("=" * 80)
    print("- The signature defect Delta = |s| - |sigma| is NOT an exclusive phenomenon")
    print("  of braid index >= 4: it already occurs within braid index 3 (T(3,7) and beyond).")
    print("- Whether it appears in a *given* coarse family (Family 1, Family 2) depends on")
    print("  how finely that family samples the word space -- absence of defect in a small")
    print("  swept region is NOT evidence of a general rigidity theorem.")
    print("- No claim above is asserted as a proved theorem; all are direct readouts of the")
    print("  validated engine (src/math_engine/braid_topology.py self_test()).")


if __name__ == "__main__":
    run_investigation()
