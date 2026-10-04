# Proposal for independent review: cut the AI-originated results from what we present

**To:** a reviewing agent with no prior context on this project.
**From:** the agent that produced the provenance analysis this rests on. I have a
stake in this conclusion. Re-derive rather than accept — §8 says how.
**Decision owner:** Aryan (high-school student, the researcher).
**What I want:** disagreement where I am wrong, not confirmation.

---

## 1. The ask, up front

I am proposing that roughly a third of the project's numbered results be
**removed from everything presented at the science fair** — poster, abstract,
paper, presentation, interview — and that the paper shrink from ~63 pages to
~9.

Nothing is deleted from the repository. The record stays. This is about what is
*presented and claimed*, not what exists.

I want you to tell me whether this is right, over-cautious, or under-cautious.

---

## 2. Context you need

A student has a mathematics research project for the 2027 science-fair cycle
(regional Feb, state Apr, ISEF May). Two parts:

- **Part II** — zero forcing number and maximum nullity of generalized Petersen
  graphs P(n,k). Headline: Z(P(n,k)) determined for *every* n when k = 2, 3, 4,
  which includes a proof of Conjecture 5 of a July 2026 arXiv note
  (arXiv:2607.19412).
- **Part I** — which P(n,k) satisfy the Riemann Hypothesis for their Ihara zeta
  function (equivalently, which are Ramanujan). A finiteness theorem for every
  k, a parity law, and an exact classification: 247 graphs for k ≤ 10.

I independently verified the central claims of both parts by writing my own
solvers from scratch: the k=4 zero-forcing table at n = 9..17, the k=5 threshold
of 162 via a numerical-semigroup computation, and all twenty of the per-k
Ramanujan counts and maxima summing to 247. **The mathematics is correct.** This
proposal is not about correctness.

Between 29 September and 3 October, an AI agent (a prior session of mine, not
the student) contributed heavily: new theorems, most of the board text, and
nearly every file in `deliverables/`. That is documented, in the agent's own
words, in `deliverables/assistance_record.md`.

---

## 3. The evidence

### 3.1 The rule (verbatim, ISEF Companion Guide 2026–2027, Rule 8)

> Artificial Intelligence (AI) may be used as a project resource but must be
> cited and given proper acknowledgment. A student is expected to do independent
> work and all materials presented must be in the researcher's own words. A
> student may not use generative AI to write the research plan, abstract, poster
> or to create citations.

Note what this does and does not say. It **prohibits** AI-written research plan,
abstract and poster. It **permits** AI as a cited resource. Whether an
AI-*originated theorem*, re-derived and rewritten by the student, violates
"independent work" is a judgment call, not a clear prohibition. I think the
honest reading is that the rules alone do not settle this. §6 returns to it.

### 3.2 The provenance split

Determined two independent ways that agree exactly:

1. **Git boundary.** The last commit before the AI sessions is `dc2a6cf`
   (28 Sep). Labels absent there and present now were added in the window.
2. **The assistance record**, §1 (student's) and §2/§5/§9 (AI's).

For `zf_paper.tex` the git method flags 13 labels; the record names the same 13.

| | Student's | AI-originated | External |
|---|---|---|---|
| Part II | 45 (+1 where AI fixed a missing hypothesis) | 13 | — |
| Part I | 9 | 13 | 2 |
| **Total** | **54** | **26** | **2** |

Full table: `deliverables/PROVENANCE_TABLE.md`.

**Caveat:** `zf_ramanujan.tex` was untracked at `dc2a6cf`, so the git method
cannot be applied to Part I. Those rows rest on the record alone. If you think
the record is self-serving, Part I is where to press.

### 3.3 The severability finding — the load-bearing claim

**Severability holds in Part II, with one exception in Part I.** I claimed it
held everywhere; I checked mechanically and it does not. The check:

```
for each AI-originated label L, find every \ref{L} and ask whether the
referencing result is student-originated.
```

**Part II: clean.** Every reference to an AI label occurs inside the AI cluster
itself (the cover-ceiling and gap-family sections). No student result cites one.

**Part I: one exception.** `thm:ramclass` — the student's 247-graph
classification — now closes with: *"That no k beyond the table admits any n at
all is Theorem `thm:absolute`, and the total is Theorem `thm:allk`."* Both are
AI-originated. The table caption cites `thm:absolute` too.

This is a **widening**, not a dependency. The student's own claim — the
classification for k ≤ 10, 247 graphs, every n below B_k decided in exact
arithmetic, with B_k from the student's `thm:finite` — stands alone. The AI
results extend it to all k.

**Consequence for the proposal:** the cut is not purely subtractive at this one
theorem. `thm:ramclass` must be **restated** — reverted to its 28 Sep form,
scoped to k ≤ 10 — not merely have its neighbours deleted. Everywhere else,
deletion suffices.

Headlines that survive the cut unchanged: the monodromy ceiling, the complete
determination at k = 2, 3, 4, the proof of Conjecture 5, the uniform finiteness
bound, the parity law, the corner theorem.

Second coupling: `thm:cover` is the student's but AI supplied its missing
hypothesis (det M(ζ) ≢ 0), without which it is false. One line, defensible.

**I got this wrong on the first pass and found it only by testing my own claim.
Assume there are more. Please check Part I especially**, where the git boundary
is unavailable.

### 3.4 What the AI column contains

Thirteen results in each part, including: ceilings on path and cycle bases, a
refutation of an arbitrary-base ceiling, an independent-set obstruction, an
absolute finiteness bound (n ≥ 231 fails for every k), a complete classification
across all k (460 pairs, 324 isomorphism classes, nothing past k = 45), a closed
form for k ≤ 9, and a classification of rational-symbol certificates.

Some of this is good mathematics. The absolute finiteness theorem and the
all-k classification are genuinely stronger statements than anything in the
student's Part I.

### 3.5 Two external facts

- **Priority.** A pull request (`the-omega-institute/trureturing` #10129, merged
  26 Sep 2026) states `def claim : Prop := ∀ n, 13 ≤ n → zeroForcingNumber
  (gp n 3) = 8` — exactly Conjecture 5 — and proves it in ~13,000 lines of Lean
  with no `sorry` and no axioms. I could not build it. It was merged 103 minutes
  after opening with zero review comments. The student's own git history
  predates it by 23 days but is private and nothing is posted.
- **Comparables.** Every top-three ISEF 2026 Mathematics award had an arXiv
  preprint before the fair, and two of three had a named university mentor or
  co-author. The first-place paper is **nine pages**. This project has nothing
  posted, no expert reader, and a 63-page document with a status-of-claims
  section.

---

## 4. The proposal

1. **Post the k=3 note to arXiv this week**, rewritten in the student's words.
   Establishes a public date against #10129. Everything else can wait.
2. **Cut the 26 AI-originated results** from the presented paper, poster,
   abstract and presentation. Keep them in the repository, disclosed.
3. **Rewrite poster, abstract and research plan** from a mathematics-only
   skeleton — statements, numbers, structure, no sentences — so the student
   writes from their own results rather than editing AI prose.
4. **Shrink to ~9 pages**, matching the shape that wins this category.
5. **Email one expert** with those nine pages.

Exception to (2): any AI result the student re-derives independently, writes in
their own words, and can prove at a whiteboard under questioning may stay. The
test is the whiteboard, not the intention.

---

## 5. The case for it

- **Low benefit.** No headline depends on the AI column (§3.3). Cutting costs no
  claim the project leads with.
- **Real risk.** The ISEF rubric scores "degree of independence" explicitly
  under the 25-point interview. A judge who asks "walk me through this proof"
  about a result the student did not derive is the single worst moment available,
  and it is avoidable for free.
- **Evidence of unreliability in that layer specifically.** The project's
  strongest-sounding claim from this window — a "cubic gap family" conjecture —
  was **refuted on 1 October**. It was AI-produced. The student caught it and
  recorded it correctly, which is to their credit, but it is one data point about
  the base rate of that column.
- **Volume is working against the project.** The comparables say nine pages and
  one expert reader. The project has 63 pages and none. Subtraction moves toward
  the target shape; the AI column moves away from it.
- **Interview time is the binding constraint**, not page count. Every minute
  spent defending a borrowed theorem is a minute not spent on the monodromy
  ceiling, which is the best thing in the project and entirely the student's.

---

## 6. The strongest case against it — steelmanned

I want you to take these seriously; I am not sure I have weighted them right.

1. **The rules may not require this.** Rule 8 permits AI as a cited resource. If
   the student re-derives a theorem and writes it in their own words, the words
   are theirs and the use is disclosed. On that reading, the correct action is
   *rigorous disclosure plus genuine mastery*, not removal — and removal
   destroys real mathematical content for no rule-based reason. **This is the
   argument I find hardest to answer.**
2. **The AI results include the project's most general statements.** Absolute
   finiteness for every k, and a classification across all k, are stronger than
   what remains. Cutting them makes the presented project narrower and arguably
   less impressive.
3. **"Cut it" may be unenforceably vague at the boundary.** Much of the write-up
   of *student-originated* results is AI-drafted prose. If the standard is
   "nothing AI touched," almost nothing survives, which is absurd. So the line
   has to be drawn at authorship of mathematics, not contact — and that line is
   fuzzier than my table makes it look.
4. **The refutation is an asset, not a liability.** A withdrawn conjecture with a
   one-line reason is strong evidence of "understanding limitations," which the
   rubric rewards. Cutting it removes the project's best honesty exhibit. (I have
   conceded this point once already and I think it is correct.)
5. **Sunk value and morale.** Telling a student to discard a third of a project
   weeks before a deadline has costs that do not show up in a rubric.

---

## 7. Where I am most likely wrong

- I am the agent that produced both the assistance record and the provenance
  table. A tidy "two-thirds is yours, and it's exactly the good two-thirds"
  conclusion is suspiciously flattering to the analysis that produced it.
- Part I's provenance rests on the record alone (§3.2 caveat), and the record was
  written by the same author whose contributions it describes.
- I have not built the Lean PR. If it does not compile, the priority argument
  weakens considerably and the urgency in (1) is overstated.
- I may be over-indexing on one year of comparables (ISEF 2026). Nine pages and
  an arXiv preprint may be correlation, not cause.
- I have never seen this student present. "Can defend it at a whiteboard" is the
  pivotal test in my proposal and I have no evidence about where that line falls
  for them.

---

## 8. How to check me independently

```bash
cd /Volumes/2TB/scifair

# The provenance boundary — does the git method reproduce the record's 13?
git show dc2a6cf:manuscript/zf_paper.tex > /tmp/old.tex
grep -oE '\\label\{(thm|lem|prop|cor|conj|obs|rem):[^}]+\}' /tmp/old.tex | sort -u > /tmp/a
grep -oE '\\label\{(thm|lem|prop|cor|conj|obs|rem):[^}]+\}' manuscript/zf_paper.tex | sort -u > /tmp/b
comm -13 /tmp/a /tmp/b          # labels added in the AI window

# The severability claim — do any student results cite AI ones?
# Part II should come back clean; Part I has one known exception (thm:ramclass).
grep -n 'ref{thm:absolute}\|ref{thm:allk}' manuscript/zf_ramanujan.tex
grep -n 'ref{thm:cexcover}\|ref{prop:lowrank}\|ref{thm:redpath}' manuscript/zf_paper.tex

# The mathematics is correct and independently reproducible:
python3 verification/verify_all.py     # ~146 checks, several minutes
```

Primary sources: `deliverables/assistance_record.md`,
`deliverables/PROVENANCE_TABLE.md`, `deliverables/HANDOFF.md`,
`deliverables/isef_ai_rules_2026-2027_VERBATIM.txt`.

---

## 9. What I want from you

1. **Is §3.3 (severability) complete?** I asserted it held everywhere, tested it,
   and found one exception in Part I. That is one error I caught in my own
   load-bearing claim within an hour of making it. Find the ones I did not.
2. **Is §6.1 right — is disclosure sufficient, making removal unnecessary?** This
   is the crux. I lean toward cutting on risk/benefit grounds rather than rules
   grounds, but I am not confident.
3. **Is the priority urgency justified** given that #10129 is unreviewed, merged
   in 103 minutes, and unbuilt by me?
4. **Is "nine pages" right, or am I overfitting to one year of winners?**
5. **What am I not seeing?** I have been embedded in this for a week and I
   produced the artifacts I am now assessing.

Disagree in writing. The student will read both.
