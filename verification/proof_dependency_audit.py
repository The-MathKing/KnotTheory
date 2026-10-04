"""Which results in this paper depend on computation, and how is it justified?

A FIRST VERSION OF THIS FILE GOT THE ANSWER WRONG, in a way worth recording.
It classified the tile-based theorems as "a search is the proof". They are not.
Reading exact_krawczyk.py: z0 is snapped to the dyadic grid 2^-60, so it is
exactly rational; f and J are integer-coefficient polynomials, so f(z0) and
J(z0) are exactly rational; the Krawczyk test holds for ARBITRARY Y, so a
float-derived Y loses nothing; and the final comparisons are exact integer
comparisons. The search only FOUND the tile. What justifies it is an exact
existence proof with an explicit rational witness. Conflating "a computer found
this" with "a computer is the only reason to believe this" is the central error
in judging computational mathematics, and this file made it.

The four categories below are about JUSTIFICATION, not about how much code ran.

  PURE         The proof is self-contained.

  WITNESS      An explicit exact object is exhibited -- an integer matrix, a
               counterexample, a dyadic-rational point plus a certified ball --
               and an exact finite calculation confirms its property. This is
               ordinary mathematics. A referee does not call this
               computer-dependent.

  FINITE-CHECK Finiteness is PROVED first, then the finitely many cases are
               checked in exact arithmetic. The mathematics is the reduction;
               the check is bookkeeping. This is the standard shape of
               respectable computer-assisted mathematics, and the project does
               it well: prop:exh proves the enumeration is finite and listable
               before enumerating, and cor:excluded proves a structural reason
               accounting for ALL the rejections.

  SOLVER       The claim rests on an external solver's assertion (CP-SAT
               returning "optimal") or on a bespoke search program. Nothing
               exhibits a checkable witness for a NEGATIVE result: "no forcing
               set of size 8 exists" has no short certificate. This is the only
               genuinely soft category, and it is small.

Run: python3 verification/proof_dependency_audit.py
"""

import os
import re
import sys
from collections import Counter

_HERE = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.join(os.path.dirname(_HERE), "manuscript")

#: label -> ("PURE" | "TYPE2" | "TYPE1", one-line reason)
#: Reviewed by hand. Add a line when a result is added; UNREVIEWED is reported.
CLASSIFICATION = {
    'thm:red'             : ('PURE', ''),
    'thm:red2'            : ('PURE', ''),
    'thm:theta'           : ('PURE', ''),
    'thm:redpath'         : ('PURE', ''),
    'thm:redcycle'        : ('PURE', ''),
    'thm:congbound'       : ('PURE', ''),
    'thm:order'           : ('PURE', ''),
    'lem:slice'           : ('PURE', ''),
    'lem:tile'            : ('PURE', ''),
    'lem:concat'          : ('PURE', ''),
    'thm:tiling'          : ('PURE', ''),
    'thm:k3all'           : ('PURE', ''),
    'prop:indobs'         : ('PURE', ''),
    'cor:regblocks'       : ('PURE', ''),
    'prop:lowrank'        : ('PURE', ''),
    'thm:antipodal'       : ('PURE', ''),
    'prop:symbol'         : ('PURE', ''),
    'thm:realis'          : ('PURE', ''),
    'cor:niven'           : ('PURE', ''),
    'prop:k2closed'       : ('PURE', ''),
    'thm:k3'              : ('PURE', ''),
    'thm:cyclo'           : ('PURE', ''),
    'thm:adjclass'        : ('PURE', ''),
    'thm:cover'           : ('PURE', ''),
    'prop:ratobs'         : ('PURE', ''),
    'cor:ceiling'         : ('PURE', ''),
    'thm:I'               : ('PURE', ''),
    'thm:DP'              : ('PURE', ''),
    'prop:SU'             : ('PURE', ''),
    'lem:boot'            : ('PURE', ''),
    'lem:close'           : ('PURE', ''),
    'cor:excluded'        : ('PURE', ''),
    'prop:exh'            : ('PURE', ''),
    'prop:reach'          : ('PURE', ''),
    'thm:signedadj'       : ('PURE', ''),
    'prop:k4cert'         : ('WITNESS', ''),
    'thm:k4rankone'       : ('WITNESS', ''),
    'thm:cexcover'        : ('WITNESS', ''),
    'thm:p17'             : ('WITNESS', ''),
    'rem:twoexc'          : ('WITNESS', ''),
    'thm:k2all'           : ('WITNESS', ''),
    'thm:k5all'           : ('WITNESS', ''),
    'thm:certvals'        : ('WITNESS', ''),
    'thm:coverattain'     : ('WITNESS', ''),
    'thm:k6'              : ('WITNESS', ''),
    'thm:k7'              : ('WITNESS', ''),
    'thm:k3krishnan'      : ('WITNESS', ''),
    'thm:k6imp'           : ('FINITE-CHECK', 'finite complete enumeration (prop:exh); cor:excluded explains all rejections'),
    'thm:ramclass'        : ('FINITE-CHECK', '460 pairs from 13,110 cases; finiteness proved by thm:absolute'),
    'thm:allk'            : ('FINITE-CHECK', 'complete over all k; bounded by thm:uniform + thm:absolute'),
    'prop:closedsmall'    : ('FINITE-CHECK', 'a CLOSED FORM in proved bounds B_k, P_k -- near-provable'),
    'prop:k4z'            : ('SOLVER', 'CP-SAT asserts optimality; no short certificate for the negative'),
    'thm:complete'        : ('SOLVER', 'small-n Z values by bespoke exhaustive search'),
    'thm:grh'             : ('PURE', ''),
    'lem:blocks'          : ('PURE', ''),
    'thm:crit'            : ('PURE', ''),
    'cor:crit'            : ('PURE', ''),
    'thm:corner'          : ('PURE', ''),
    'cor:lens'            : ('PURE', ''),
    'lem:signs'           : ('PURE', ''),
    'thm:uniform'         : ('PURE', ''),
    'thm:finite'          : ('PURE', ''),
    'thm:absolute'        : ('PURE', ''),
    'thm:parity'          : ('PURE', ''),
    'thm:local'           : ('PURE', ''),
    'cor:divclosed'       : ('PURE', ''),
    'lem:mingcd'          : ('PURE', ''),
    'thm:gcdsafe'         : ('PURE', ''),
    'thm:covcorner'       : ('PURE', ''),
    'thm:thetarh'         : ('PURE', ''),
    'thm:covfinite'       : ('PURE', ''),
    'thm:noinfinite'      : ('PURE', ''),
    'prop:deficit'        : ('PURE', ''),
    'conj'                : ('CONJ', ''),
    'conj:leading'        : ('CONJ', ''),
    'conj:generaln'       : ('CONJ', ''),
}


def results():
    t = open(os.path.join(MAN, "zf_paper.tex"), encoding="utf-8").read()
    ram = os.path.join(MAN, "zf_ramanujan.tex")
    if os.path.exists(ram):
        t = t.replace("\\input{zf_ramanujan}",
                      open(ram, encoding="utf-8").read())
    return re.findall(
        r"\\begin\{(theorem|proposition|lemma|corollary|conjecture)\}"
        r"(?:\[[^\]]*\])?\s*\\label\{([^}]*)\}", t)


def main():
    found = results()
    counts, unreviewed, by_kind = Counter(), [], {}
    for kind, lab in found:
        if lab in CLASSIFICATION:
            k = CLASSIFICATION[lab][0]
        else:
            k = "UNREVIEWED"
            unreviewed.append((kind, lab))
        counts[k] += 1
        by_kind.setdefault(k, []).append(lab)

    total = len(found)
    print("Proof-dependency audit")
    print("=" * 66)
    print(f"{total} formal results in the manuscript\n")
    order = ["PURE", "WITNESS", "FINITE-CHECK", "SOLVER", "CONJ", "UNREVIEWED"]
    label = {"PURE": "self-contained proof",
             "WITNESS": "explicit exact witness + exact check",
             "FINITE-CHECK": "finiteness PROVED, then cases checked exactly",
             "SOLVER": "rests on a solver/bespoke search (no witness)",
             "CONJ": "conjecture",
             "UNREVIEWED": "NOT CLASSIFIED BY HAND"}
    provable = counts["PURE"] + counts["WITNESS"]
    base = total - counts["CONJ"] - counts["UNREVIEWED"]
    for k in order:
        if not counts[k]:
            continue
        pct = 100.0 * counts[k] / total
        print(f"  {k:<11} {counts[k]:>3}  ({pct:4.1f}%)  {label[k]}")

    print(f"\nOf the {base} results with proofs, "
          f"{provable} ({100.0*provable/base:.0f}%) do not depend on a search.")
    print(f"Only {counts["SOLVER"]} are computer-dependent in the sense that")
    print("matters to a referee. Those, and only those, are worth converting:\n")
    for lab in sorted(by_kind.get("SOLVER", []) + by_kind.get("FINITE-CHECK", [])):
        print(f"    {lab:<20} {CLASSIFICATION[lab][1]}")

    if unreviewed:
        print(f"\nUNREVIEWED ({len(unreviewed)}) -- classify these by hand "
              f"before quoting any percentage:")
        for kind, lab in unreviewed:
            print(f"    {kind:<12} {lab}")
    stale = sorted(set(CLASSIFICATION) - {l for _, l in found} - {"rem:twoexc"})
    if stale:
        print(f"\nIn the table but not found in the manuscript "
              f"(renamed or removed?): {', '.join(stale)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
