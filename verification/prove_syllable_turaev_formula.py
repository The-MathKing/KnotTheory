"""
THEOREM (syllable formula for 3-strand positive braid diagrams).

Let w be a positive braid word on 3 strands, written as k >= 1 maximal
syllables (blocks of a repeated generator; since there are only 2
generators on 3 strands, consecutive syllables necessarily alternate
between sigma_1 and sigma_2). Let e = length(w) be the total crossing
number. Let D be the standard closed-braid diagram of w. Then

    s_B(D) = (e - k) + (2 if k is odd else 1)                        (*)

and therefore (since s_A(D) = 3 always, for any positive braid word),

    g_T(D) = (e + 2 - s_A(D) - s_B(D)) / 2 = floor(k/2) - 1          (**)

for k >= 2 (k = 1 is a degenerate case: the diagram is disconnected, since
an entire strand is never crossed, and the Turaev-genus formula requires a
connected diagram).

Note this is a statement about the Turaev genus of ONE SPECIFIC diagram
(an upper bound on the true, diagram-minimized g_T of the underlying knot),
not a new claim about the knot invariant itself -- see Log Entry 17 for why
that distinction matters.

PROOF.

Lemma 1 (syllable reduction). Applying a syllable of m >= 1 repeated
crossings at the same position pair (i, i+1) is equivalent, for circle
counting purposes, to applying that generator ONCE, plus (m-1) permanently
isolated circles.

Proof of Lemma 1. Let X, Y be the frontier values at positions i, i+1
immediately before the syllable starts. The first crossing performs
union(X, Y) -- a genuine, meaningful merge -- then creates a fresh node
Z_1 and sets frontier[i] = frontier[i+1] = Z_1. Every subsequent crossing
in the same syllable (2nd, 3rd, ..., m-th) reads frontier[i] = frontier
[i+1] = Z_{j} (the previous crossing's fresh node, since nothing else can
have touched positions i, i+1 in between -- they are the same generator),
performs union(Z_j, Z_j) (a no-op on an already-fresh, never-yet-unioned
singleton node), and creates a new fresh Z_{j+1}. Each Z_1, ..., Z_{m-1}
is therefore permanently isolated: created fresh, immediately superseded
in the frontier array by the next crossing in the same syllable, and never
referenced by any union() call again (union() only ever reads the CURRENT
frontier array). Each contributes exactly one circle to the final count.
Only Z_m survives as the syllable's output to the rest of the word, with
X and Y already merged -- identical to what a single application of the
generator would have produced.                                          QED

Applying Lemma 1 to every syllable of w: the k syllables contribute
sum(m_i - 1) = e - k permanently isolated circles, and the REST of the
computation is identical to applying the k-syllable PURE ALTERNATION word
of length k (one crossing per syllable). This proves the additive term in
(*) and reduces the problem to the base case e = k.

Lemma 2 (base case, pure alternation). For the pure-alternation word of
length k >= 1 (crossings alternate sigma_1, sigma_2, sigma_1, ... starting
with sigma_1), before the final braid closure there are ALWAYS exactly 3
distinct components among all nodes created, consisting of:
  (A) {TOP_0, TOP_1}: sealed together at step 1, and never touched again
      by any later union (positions (0,1) are vacated of TOP_0, TOP_1
      immediately after step 1 and never point back to them).
  (B) a "chain" component containing TOP_2 that absorbs, at every step
      j >= 2, the fresh node created at step j-1 (this is because
      generators sigma_1 = cap(0,1) and sigma_2 = cap(1,2) share strand
      position 1 as a common "hinge": a syllable's fresh node is written
      to BOTH of its two positions, so even though only one of those two
      positions is touched by the very next crossing, that crossing reads
      the SAME shared node via the hinge and pulls it into the chain).
  (C) the single most-recently-created fresh node, not yet absorbed.

Proof by induction on k. Base k=1: step 1 performs union(TOP_0, TOP_1) --
component A -- and creates fresh Z_1 at positions (0,1); TOP_2 is
untouched. So the 3 components are A = {TOP_0,TOP_1}, B = {TOP_2}, C =
{Z_1}, matching the claim. Inductive step: assume the claim holds after
k-1 steps, so components are A (fixed, as above), B (containing TOP_2 and
Z_1, ..., Z_{k-2}), C = {Z_{k-1}}. Step k touches positions determined by
parity; by the hinge argument, one of the two positions it touches carries
the node Z_{k-1} forward (component C) and the other carries the node
Z_{k-2} (already in component B, since it was absorbed at step k-1).
union(Z_{k-1}, Z_{k-2}) therefore merges C into B, and a new fresh Z_k is
created as the new component C. Components A, B, C retain the stated
structure with k in place of k-1.                                       QED

Given Lemma 2, the braid closure applies union(frontier[j], TOP_j) for
j = 0, 1, 2. Case k odd (last step was sigma_1, touching positions (0,1)):
frontier = [C, C, B] (frontier[2] was last set at step k-1, an even/sigma_2
step, and by the hinge mechanism was absorbed into B at step k). Closure:
union(C, TOP_0 in A) is a real merge (A, C join); union(C in A+C, TOP_1 in
A) is a no-op (already the same component); union(B, TOP_2 in B) is a
no-op (B already contains TOP_2). Final count: 2 components ({A,C}, {B}).
Case k even: frontier = [B, C, C] (frontier[0] absorbed into B via the
symmetric hinge argument). Closure: union(B, TOP_0 in A) is a real merge
(A, B join); union(C, TOP_1 in A+B) is a real merge (all three join);
union(C in A+B+C, TOP_2 in A+B+C) is a no-op. Final count: 1 component.
This proves Lemma 2, and hence (*) and (**).                            QED

This script verifies (*) computationally: brute force across many (e, k)
pairs and many random syllable-length distributions per pair (the reduction
lemma predicts the distribution never matters), plus the base case alone
across k = 1..40.

Run: python verification/prove_syllable_turaev_formula.py
"""
import sys
import os
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from math_engine.turaev_diagram import turaev_genus_of_diagram, s_B


def word_from_syllables(syllables):
    word, gen = [], 1
    for length in syllables:
        word += [gen] * length
        gen = 2 if gen == 1 else 1
    return word


def predicted_sB(e, k):
    return (e - k) + (2 if k % 2 == 1 else 1)


def predicted_gT(k):
    return k // 2 - 1


print("STEP 1 -- base case (pure alternation), k = 1..40")
mismatches = 0
for k in range(1, 41):
    w = word_from_syllables([1] * k)
    sb = s_B(w, 3)
    predicted = 2 if k % 2 == 1 else 1
    if sb != predicted:
        mismatches += 1
        print(f"  MISMATCH k={k}: predicted s_B={predicted}, got {sb}")
print(f"  {41-1} values of k tested, {mismatches} mismatches.")

print("\nSTEP 2 -- reduction lemma: s_B depends only on (e,k), not on distribution")
random.seed(0)
tested = distribution_mismatches = formula_mismatches = 0
for e, k in [(15, 5), (20, 5), (20, 8), (24, 6), (18, 9), (30, 10), (30, 11), (40, 13)]:
    if k > e:
        continue
    seen = set()
    for _ in range(20):
        cuts = sorted(random.sample(range(1, e), k - 1))
        parts = [cuts[0]] + [cuts[i] - cuts[i - 1] for i in range(1, k - 1)] + [e - cuts[-1]]
        w = word_from_syllables(parts)
        sb = s_B(w, 3)
        seen.add(sb)
        tested += 1
    if len(seen) != 1:
        distribution_mismatches += 1
        print(f"  DISTRIBUTION VARIES for e={e},k={k}: got {seen}")
    elif seen != {predicted_sB(e, k)}:
        formula_mismatches += 1
        print(f"  FORMULA MISMATCH for e={e},k={k}: predicted {predicted_sB(e,k)}, got {seen}")
print(f"  {tested} random (e,k,distribution) triples tested, "
      f"{distribution_mismatches} where distribution mattered (should be 0), "
      f"{formula_mismatches} where the formula was wrong (should be 0).")

print("\nSTEP 3 -- full formula g_T(D) = floor(k/2) - 1, k = 2..30, e = k..k+20")
mism = tot = 0
for k in range(2, 31):
    for e in range(k, k + 21, 3):
        parts = [1] * (k - 1) + [e - (k - 1)]  # one long syllable absorbs the extra length
        w = word_from_syllables(parts)
        gt, sa, sb = turaev_genus_of_diagram(w, 3)
        tot += 1
        if gt != predicted_gT(k):
            mism += 1
            print(f"  MISMATCH e={e} k={k}: predicted g_T={predicted_gT(k)}, got {gt}")
print(f"  {tot} (e,k) pairs tested, {mism} mismatches.")

print("\n" + ("ALL CHECKS PASSED" if mismatches == 0 and distribution_mismatches == 0
              and formula_mismatches == 0 and mism == 0 else "SOME CHECKS FAILED"))
