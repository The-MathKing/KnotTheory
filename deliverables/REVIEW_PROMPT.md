# Review prompt

Paste the block below into a fresh Claude session with this repository attached
or accessible. It is written to get an adversarial check rather than a
confirmation.

---

You are reviewing a high-school mathematics research project for correctness and
for competition readiness. The repository is at `/Volumes/2TB/scifair`. Be
adversarial. I want defects found, not encouragement. If something is right, say
so briefly and move on; spend your effort where the risk is.

**Do not take any claim in the repository at face value, including claims in the
research log about what was verified.** Where you can check something yourself,
check it. Where you cannot, say explicitly that you could not.

## What the project claims

Zero forcing number `Z(G)` and maximum nullity `M(G)` of generalized Petersen
graphs `P(n,k)`. Main claims, in the author's own labelling:

- `Z(P(n,2))` and `Z(P(n,3))` are determined for **every** admissible n.
- `Z(P(n,3)) = 8` for every n >= 13, and 13 is optimal.
- `Z(P(n,4)) = M(P(n,4)) = 10` for every n >= 29, and `Z(P(n,4))` determined for every n.
- A "ceiling theorem": for any matrix on the pattern of `P(n,k)`, the nullity is
  at most `2k+2`, with equality iff a monodromy `T = I`.
- A "tiling theorem": identity tiles of every length in `[L,2L)` give
  `Z(P(n,k)) = 2k+2` for every n >= L.
- 56 tiles certified by a Krawczyk contraction evaluated in exact rational arithmetic.

## Tasks

**1. Verify the mathematics independently.**
Read `manuscript/zf_paper.tex`. For each numbered theorem, decide whether the
proof actually establishes the statement. Pay particular attention to:
- hypotheses that are stated but not used, or used but not stated;
- the reduction theorem's hypothesis `n >= 2k+3` — confirm it is necessary and
  that nothing downstream silently assumes the weaker `2k < n`;
- the tiling theorem's docking argument, which claims each tile's transfer
  product depends only on that tile's interior. Verify the index range.
- the claim that the square subsystem chosen for certification is *equivalent*
  to `A K = 0` rather than a maximal-rank selection of it.

**2. Re-run the computations.**
`verification/verify_all.py` claims 77 checks, all passing. Run it. Then write
your **own** independent zero-forcing solver from scratch and check at least
these against it: `Z(P(12,3))`, `Z(P(13,3))`, `Z(P(10,3))`, `Z(P(8,2))`,
`Z(P(10,2))`, `Z(P(19,4))`. Report any disagreement immediately.

**3. Audit the certification.**
The Krawczyk argument is the load-bearing rigor claim. Read
`verification/krawczyk.py` and `verification/certify_tiles.py`. Decide whether a
passing test really proves a true real solution exists. Check the Lipschitz
bound `L_LIP = 12` — is it actually an upper bound, or asserted?

**4. Find internal inconsistencies.**
The paper is long and was edited many times. Grep for numbers that appear in
more than one place and disagree: tile counts, threshold values `L(k)`, the set
of n claimed, certification counts. Check the Status section against every
theorem it references. This has been a recurring failure mode.

**5. Check novelty.**
Search the literature for: zero forcing on generalized Petersen graphs; maximum
nullity via transfer matrices or monodromy; tiling or block constructions for
matrices on circulant-like graphs; interval certification of nullity. **The
author has not verified that the tiling/monodromy method is novel.** Report what
you find, including if it has been done before.

**6. Check attribution.**
The project claims a 2020 paper's theorem is false and that a July 2026 arXiv
note (2607.19412) corrects it and leaves open the stabilization threshold. Verify
the note exists, says that, and that the project's characterisation of what it
leaves open is accurate. The project deliberately does **not** claim to prove a
conjecture stated in that note, because the author did not read it; if the note
does state such a conjecture, say so.

**7. Judge overstatement.**
Read `manuscript/zf_log.tex`. The author repeatedly reports negative results and
later finds the limitation was in the computational budget rather than the
mathematics. Check whether any *current* claim in the paper is stated more
strongly than the evidence supports, particularly anything about `k >= 5` or
about what "cannot" be done.

**8. Assess competition readiness.**
Against the ISEF 100-point rubric (Research Question 10, Design and Methodology
15, Execution 20, Creativity 20, Presentation: poster 10 + interview 25), score
it and justify each number. Identify the single highest-leverage fix.

## Output

For each defect: file, location, what is wrong, how serious, and the fix. Rank by
severity. Separate "this is wrong" from "this is unclear" from "this is a
presentation problem". End with the three things most worth doing next, and say
plainly if you think any headline claim does not hold.
