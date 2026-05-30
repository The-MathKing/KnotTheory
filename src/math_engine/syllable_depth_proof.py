"""
Extends the braid-family defect search (investigate_braid_families.py) to
6-syllable 3-braids and to a genuine 4-strand positive-braid sweep, using the
validated Seifert-matrix engine (braid_topology.py, Collins 2007 algorithm).

This replaces an earlier version whose 4-strand section never computed a
signature at all -- it printed "s(K) = 2*g_3(K) = 2*g_4(K)" as a labelled
"Exact Rasmussen / 4-ball genus relation" theorem, but that identity is just
the Rasmussen/Kronheimer-Mrowka slice-Bennequin equality for ALL positive
braids (already used elsewhere in this codebase); no signature comparison
was made, so no defect claim was actually tested for n=4. This version
computes real 4-strand signatures and reports the real defect rate.
"""
import sys
import os
import pandas as pd

sys.path.insert(0, os.getcwd())
from src.math_engine.braid_topology import evaluate_braid_defect, self_test


def run_syllable_depth_proof():
    print("=" * 80)
    print("6-SYLLABLE 3-BRAIDS AND 4-STRAND POSITIVE BRAIDS (validated engine)")
    print("=" * 80)

    assert self_test(verbose=False), "Seifert-matrix engine failed self-test; aborting."

    print("\n--- 6-syllable positive 3-braids, a..f in [1..4]/[1..2] (c up to 36) ---")
    results = []
    for a in range(1, 5):
        for b in range(1, 5):
            for c in range(1, 5):
                for d in range(1, 5):
                    for e in range(1, 3):
                        for f in range(1, 3):
                            word = [1] * a + [2] * b + [1] * c + [2] * d + [1] * e + [2] * f
                            res = evaluate_braid_defect(word, n=3)
                            if res is not None:
                                res.update(a=a, b=b, c=c, d=d, e=e, f=f)
                                results.append(res)
    df6 = pd.DataFrame(results)
    print(f"Synthesized {len(df6)} authentic 1-component knots.")
    counts = df6["defect"].value_counts().to_dict()
    print(f"Defect value counts: {counts}")
    n_defect = int((df6["defect"] > 0).sum())
    print(f"Nonzero defect: {n_defect}/{len(df6)} ({100*n_defect/len(df6):.2f}%)")
    if n_defect:
        print("\nSample defect-bearing 6-syllable knots:")
        print(f"{'(a,b,c,d,e,f)':<22}{'c':>4}{'s':>6}{'sigma':>7}{'defect':>8}")
        for _, r in df6[df6["defect"] > 0].head(10).iterrows():
            vec = f"({r['a']},{r['b']},{r['c']},{r['d']},{r['e']},{r['f']})"
            print(f"{vec:<22}{r['crossings']:>4}{r['s']:>6}{r['sig']:>7}{r['defect']:>8}")

    print("\n--- 4-strand positive braids sigma_1^a sigma_2^b sigma_3^c sigma_1^d sigma_2^e sigma_3^f ---")
    results4 = []
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                for d in range(1, 4):
                    for e in range(1, 4):
                        for f in range(1, 4):
                            word = [1] * a + [2] * b + [3] * c + [1] * d + [2] * e + [3] * f
                            res = evaluate_braid_defect(word, n=4)
                            if res is not None:
                                results4.append(res)
    df4 = pd.DataFrame(results4)
    print(f"Synthesized {len(df4)} authentic 1-component 4-strand braid knots "
          f"(crossings up to {int(df4['crossings'].max())}).")
    n_defect4 = int((df4["defect"] > 0).sum())
    print(f"Nonzero defect: {n_defect4}/{len(df4)} ({100*n_defect4/len(df4):.2f}%)  |  "
          f"Zero defect: {len(df4)-n_defect4}/{len(df4)} ({100*(len(df4)-n_defect4)/len(df4):.2f}%)")
    if n_defect4:
        worst = df4.sort_values("defect", ascending=False).iloc[0]
        print(f"Largest defect: {int(worst['defect'])} at word={worst['word']}, "
              f"c={worst['crossings']}, s={worst['s']}, sigma={worst['sig']}")

    print("\n(Genus identity check, separate from the defect: for every positive braid,")
    print(" s(K) = 2*g_3(K) = e(beta) - n + 1 holds by construction -- this is the")
    print(" Rasmussen/Kronheimer-Mrowka slice-Bennequin equality, not a new result.)")


if __name__ == "__main__":
    run_syllable_depth_proof()
