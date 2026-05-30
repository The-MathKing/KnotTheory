"""
Log Entry 15 of manuscript/log.tex asserts:

  "positive 3-braid closures are universally signature-rigid, sigma(beta-hat) = -(e(beta)-2),
   and the signature defect in positive knots is an exclusive phenomenon of braid index >= 4."

Two problems, both demonstrated below.

(1) src/math_engine/braid_topology.py cannot possibly have tested this. Its
    goeritz_matrix_and_signature() builds a hand-written matrix whose signature is
    -(e-2) for EVERY positive 3-braid word. The "0 defects in 1,280 configurations"
    result is forced by the code, not discovered from it.

(2) The claim is false. T(3,7) is a positive 3-braid knot (14 crossings, inside the
    stated c <= 36 search range) with defect |s| - |sigma| = 4.

Run:  ./venv/bin/python verification/refute_3braid_claim.py
"""
import sys
from math import gcd
sys.path.insert(0, "src")
from math_engine.braid_topology import BraidKnot as FixedBraidKnot


class OldBuggyBraidKnot:
    """Historical reproduction of the pre-fix implementation that used to live
    at src/math_engine/braid_topology.py (BraidKnot.goeritz_matrix_and_signature).
    It has since been REPLACED in that file by a real, validated Seifert-matrix
    engine (see that file's self_test()); this class is kept here, standalone,
    only so this script can still demonstrate what was wrong with the old one."""

    def __init__(self, n, word):
        self.n = n
        self.word = list(word)

    def is_knot(self):
        perm = list(range(self.n))
        for gen in self.word:
            idx = abs(gen) - 1
            if idx < 0 or idx >= self.n - 1:
                return False
            perm[idx], perm[idx + 1] = perm[idx + 1], perm[idx]
        visited = [False] * self.n
        cycles = 0
        for i in range(self.n):
            if not visited[i]:
                cycles += 1
                cur = i
                while not visited[cur]:
                    visited[cur] = True
                    cur = perm[cur]
        return cycles == 1

    def goeritz_matrix_and_signature(self):
        # Reproduces the old file's logic exactly: for n==3, positive words,
        # it always returned -(e-2) regardless of the actual crossing pattern.
        e = len(self.word)
        if self.n == 3 and all(x in [1, 2] for x in self.word):
            return -(e - 2)
        return None


def sigma_torus(p, q):
    """Classical signature of T(p,q). Each eigenvalue of the symmetrised Seifert
    form is indexed by (i,j) and is negative iff i/p + j/q (mod 2) lies in (1/2, 3/2)."""
    return sum(-1 if 0.5 < (i/p + j/q) % 2 < 1.5 else 1
               for i in range(1, p) for j in range(1, q))

def genus_torus(p, q):
    return (p - 1) * (q - 1) // 2

print("STEP 1 -- validate the signature formula against KnotInfo ground truth")
GROUND_TRUTH = [(2,3,"3_1",-2), (2,5,"5_1",-4), (2,7,"7_1",-6), (2,9,"9_1",-8),
                (2,11,"11a_367",-10), (3,4,"8_19",-6), (3,5,"10_124",-8)]
for p, q, name, truth in GROUND_TRUTH:
    got = sigma_torus(p, q)
    assert got == truth, f"formula disagrees with KnotInfo on {name}"
    print(f"  T({p},{q}) = {name:<9} sigma = {got:<4} matches KnotInfo")

print("\nSTEP 2 -- the engine returns -(e-2) for every positive 3-braid it accepts")
import random
random.seed(0)
tested = deviating = 0
for _ in range(4000):
    e = random.randint(4, 16)
    word = [random.choice([1, 2]) for _ in range(e)]
    bk = OldBuggyBraidKnot(3, word)
    if not bk.is_knot():
        continue
    sg = bk.goeritz_matrix_and_signature()
    if sg is None:
        continue
    tested += 1
    deviating += (sg != -(e - 2))
print(f"  {tested} positive 3-braid knots tested; {deviating} gave sigma != -(e-2).")
print("  The engine's signature is a restatement of its own input length.")

print("\nSTEP 3 -- counterexamples: positive 3-braid knots T(3,q) = closure of (s1 s2)^q")
print(f"  {'knot':<9}{'c':>4}{'s = 2g':>8}{'|sigma|':>9}{'DEFECT':>8}   {'old (buggy)':>12}{'new (fixed)':>12}")
first = None
for q in range(2, 20):
    if gcd(3, q) != 1:
        continue
    e = 2 * q
    s = 2 * genus_torus(3, q)
    sg = abs(sigma_torus(3, q))
    defect = s - sg
    old_eng = OldBuggyBraidKnot(3, [1, 2] * q).goeritz_matrix_and_signature()
    new_eng = FixedBraidKnot(3, [1, 2] * q).signature()
    flag = "  <-- counterexample" if defect else ""
    if defect and first is None:
        first = (q, e, s, sg, defect)
    assert new_eng == -sg, f"fixed engine disagrees with closed form at T(3,{q}): {new_eng} vs {-sg}"
    print(f"  T(3,{q}){'':<3}{e:>4}{s:>8}{sg:>9}{defect:>8}   {old_eng:>12}{new_eng:>12}{flag}")

q, e, s, sg, d = first
print(f"\nSmallest counterexample: T(3,{q}), a positive 3-braid knot with c = {e} crossings,")
print(f"braid index 3, s = {s}, |sigma| = {sg}, defect = {d} > 0.")
print("The old engine reports sigma = -(e-2) regardless (column 'old (buggy)'), so it could")
print("never see this. The new, validated engine (column 'new (fixed)') agrees exactly with")
print("the independently-checked closed form at every q -- assertion above confirms this for")
print("all torus braids in this sweep.")
print("The defect therefore does NOT require braid index >= 4, and positive 3-braid")
print("closures are NOT signature-rigid. Log Entry 15 (original draft) was correctly retracted.")
