> **STALE — superseded 2026-09-27.** This document was written before the
> general-$n$ results and is wrong in three load-bearing ways. (1) It states
> that $k=3,6,7,8,9$ "cannot attain $2k+2$, and that is a theorem about
> rational symbols": false. That enumeration imposed $c^2>0$ (a *symmetric*
> certificate) where $c^2\neq0$ suffices; six symbols survive at $k=3$ and one
> at $k=7$. (2) It says a period-$d$ symbol carries $5d-1$ free ratios; the
> count is $2d+1$. (3) Its central recommendation, "General $n$, not more
> special $n$", has been executed: $Z(P(n,k))$ is now determined for all large
> $n$ at $k=2,3,4$ with no congruence conditions, so the stated gap against the
> 2026 first-place project is closed for those $k$. Its "second-award shaped"
> verdict predates the project's strongest results. Read `zf_paper.tex`
> Status section for the current position.

# Scoping the ISEF Mathematics category, and what the project must produce

Two things are assembled here. **Part 1** is the actual ISEF 2026 Mathematics
field — every published abstract, every award — pulled from the Society for
Science abstract database and cross-checked against the official full-awards
release. **Part 2** is the concrete list of what has to exist, and by when, to
get from a Dallas regional entry to the ISEF floor.

Raw data: `data/isef2026_mathematics.json` (39 records with abstracts),
`data/isef2026_mathematics_table.txt` (readable listing).

---

## Part 1 — The ISEF 2026 Mathematics field

### 1.1 How the category is actually scored

ISEF 2026 was held in Phoenix. Mathematics project numbers run to at least
MATH041, and 39 finalists consented to publish an abstract. Ten Grand Awards
were given:

| Tier | Amount | Count |
|---|---|---|
| First | $6,000 | 1 |
| Second | $2,400 | 2 |
| Third | $1,200 | 3 |
| Fourth | $600 | 4 |

So roughly **one project in four takes a Grand Award**, and a *single* project
takes first. On top of that, the American Mathematical Society gives its own
first award ($2,000), one-year memberships to seven projects, and honorable
mentions to five — which is why 28 of the 39 published projects list *some*
award. Do not read that 72% figure as an easy field: special-society awards are
broad, Grand Awards are not.

The category winner also took the **Regeneron Young Scientist Award of
$75,000**, one of the two top prizes of the entire fair. In 2026 a mathematics
project was among the very top of ISEF overall.

### 1.2 The ten Grand Award winners

**First — $6,000, plus the $75,000 Young Scientist Award**
*Solvability of Meromorphic Equations in Elementary Functions* — Nikola
Veselinov, Sofia High School of Mathematics, Bulgaria.
A general theorem: if `f'` has infinitely many roots `x_i` and `{f(x_i)}` is
infinite, then `f(x)=a` is unsolvable in elementary functions. It generalises a
chain of published results (Kanel-Belov–Malistov–Zaytsev; Zelenko) and the
proof combines Wielandt's theorem on primitive infinite permutation groups with
an iterative decomposition of the monodromy group via one-dimensional
topological Galois theory.

**Second — $2,400 each**
- *Universal Matrices for Counting Fibo-Multinomial and C-Multinomial
  Coefficients With a Cryptographic Application* — Arav Chand, NY. A
  universality theorem: one family of matrices governs prime divisibility for
  binomial, C-nomial, multinomial and C-multinomial coefficients at once,
  independent of the sequence `C`. Drops complexity from `O(n³ log n)` to
  `O(log n)`, then builds a CSPRNG that passes all NIST tests over 500M bits.
- *Detecting Causality in (2+1)-Dimensional Globally Hyperbolic Spacetimes
  Using Conjugation Quandles Over Dihedral Groups* — Zining Fan, PA. Proves the
  `D₅` conjugation quandle separates Allen–Swenberg sky links that the
  Alexander–Conway polynomial cannot, then extends to the full infinite family
  via Smith normal form and a closed-form homomorphism count.

**Third — $1,200 each**
- *Complexity Functions Are All You Need* — Liqian Ying, Singapore. Introduces
  "Formation Complexity Functions," a five-parameter framework unifying integer
  complexity, resistor networks and combinatorial number games; proves
  logarithmic upper bounds for a generalised "24 game."
- *Early Warning for Critical Transitions in Epidemics* — Maya Rangarajan, NY.
  Dynamical systems plus a deep classifier trained on 100,000 simulated
  outbreaks; validated on 5,274 real outbreaks.
- *The Repelling Propellers Problem* — Riya Mehrotra, CA. An open problem posed
  by James Propp. **Uses complex-number and cyclotomic techniques to get a
  closed form in terms of the gcd**, classifies configurations, proves a
  conjecture two independent ways.

**Fourth — $600 each**
- *Projective Generalization of Foci and Isogonal Cubics Loci of Complete
  Quadrilaterals* — Pin-Chun Lu, Chinese Taipei (projective geometry).
- *The Split Elevation Theorem and the H Tower for Virtual Knots* — Ha/Jang/Ha,
  South Korea (a theorem generating stronger invariants from any flat virtual
  knot invariant, plus an infinite hierarchy).
- *Energy-Stable Numerical Method for Blood Flow in 3D Brain Aneurysms* — Helen
  Zhu, NJ (finite elements, provable discrete energy law).
- *Persistent Homology to Quantify Gerrymandering* — Ananya Shah, NY (applied
  topology).

### 1.3 What the pattern actually says

**Pure mathematics owns the top.** Seven of ten Grand Awards are pure; and
*all three of the top award slots* — the First and both Seconds — are pure
theorem-proving work. The applied/ML-flavoured projects (epidemics, aneurysm
flow, gerrymandering) cluster at Third and Fourth. This directly contradicts
the instinct that an ML-heavy applied project photographs better to judges.

**The winning shape is: a named open question, a general theorem, real
machinery.** Veselinov did not solve a toy case — he stated a hypothesis and a
conclusion that subsume several published theorems, and he used named heavy
tools (topological Galois theory, Wielandt). Chand proved a *universality*
statement. These read like short research papers, not like projects.

**An application is a bonus, not the result.** Chand's crypto PRNG with NIST
validation sits on top of a theorem; it is not the theorem. Chand placed
second; the purely theoretical project placed first.

**Attacking a specifically-attributed open problem is common at the top.**
Mehrotra's problem is Propp's. Fan's is Allen–Swenberg's. Veselinov generalises
a named chain. None of them invented a vague question.

### 1.4 Where this project sits

Calibrating honestly against the ladder above:

- The project attacks a **specifically attributed open problem** — Krishnan's
  July 2026 correction note explicitly records a rigorous lower bound for
  `k ≥ 4` as open. That matches the top-tier pattern.
- It produces a **structural theorem** (every matrix with the graph's pattern
  reduces to a nine-term recurrence of order `2k+2`; nullity = `dim ker(T−I)`;
  the method's ceiling equals the upper bound), and then **first exact values**
  `Z(P(n,4))=10` and `Z(P(n,5))=12` on infinite families.
- The mechanism is **cyclotomic/Galois** — the same family of tools as the
  third-place Propellers project, deployed on a harder target.
- Certificates are **integer matrices verified by exact rational arithmetic**,
  which is a stronger reproducibility story than most of the field offers.

That is second-award shaped today, and plausibly first-award shaped if the
remaining gap closes. **The honest gap against Veselinov:** his theorem is a
clean general statement with no residue conditions. Ours resolves `k=4,5` only
for `n` in specific congruence classes, and `k ≥ 6` is untouched. A general-`n`
construction, or a proof that the arithmetic obstruction is real, is what would
move this from "first exact values on families" to "the problem is settled."

---

## Part 2 — What has to exist, and by when

### 2.1 The path and the dates

| Stage | When | Where | Who advances |
|---|---|---|---|
| DRSEF registration | on or about **10 Feb 2027** | STEM Wizard | — |
| **DRSEF** | **20 Feb 2027** | Fair Park, Dallas | two separate outcomes, below |
| Texas State (TXSEF) | 2–3 Apr 2027 | — | **top 2 in the category** |
| **ISEF 2027** | **8–14 May 2027** | Los Angeles | **7 top Grand Award winners, across all categories** |

**There are two different doors out of DRSEF.**

1. *Top 2 in the Mathematics category* → Texas State (TXSEF).
2. *One of the **7 top Grand Award winners** of the whole fair* → ISEF directly.

Last year's ISEF entrant from DRSEF came through door 2.

**Neither door avoids a cross-category judgment — door 1 only defers it.**
An earlier version of this document treated door 1 as the "category-level"
route, as though winning Mathematics were sufficient. It is not. Only about
**10 projects advance from TXSEF to ISEF**, and ISEF has 22 categories, so most
categories send nobody. A selection that small cannot be category-internal; it
is necessarily comparative across fields. So door 1 is not one gate but two:
a category gate at DRSEF, then a harder cross-category gate at state level
against the strongest projects in Texas.

Practical consequence: **designing for a non-specialist panel is an
unconditional constraint, not a contingency for one route.** It applies from
the first board.

### Hard evidence: the Texas state Mathematics winners did not advance

The top three Mathematics projects at the Texas state fair this year:

1. *Dynamic Mathematical PDE Modeling of TANGO2 Progression and Episode
   Prediction*
2. *Irreducible Polynomials over Finite Fields as Cryptographic Frameworks for
   Cybersecurity*
3. *Mathematical analysis of a new real-domain Collatz map preserving parity
   dynamics with applications to momentum-based optimization*

**None of them made ISEF.** Winning the Mathematics category at state was not
sufficient; the ~10 state slots went to other categories.

This is the single most useful calibration point available, and it sharpens the
ISEF-level analysis rather than contradicting it. Two patterns in those three
titles:

**Every one has an application bolted on.** "Episode Prediction." "for
Cybersecurity." "with applications to momentum-based optimization." The
instinct is that an application makes a math project legible to a general
panel. The evidence says the opposite, and the mechanism is not subtle: *a
mathematics project that presents itself as applied gets judged as an applied
project, against specialists in that application.* A PDE model of disease
progression is compared by a cross-category panel against actual biomedical
research and found thin — not because the mathematics is bad, but because it
has volunteered for the wrong comparison. Contrast ISEF 2026, where the
Mathematics winner was maximally pure (topological Galois theory, unsolvability
in elementary functions) and took the $75,000 Young Scientist Award in exactly
the cross-category judgment these three lost.

**One invented its own object.** "A *new* real-domain Collatz map." Defining
your own object and then analysing it is a structurally weaker claim than
answering a question somebody else posed and failed to answer, because nobody
outside the project can tell whether the question was hard. Every ISEF 2026
Grand Award winner in Mathematics attacked an attributed problem: Propp's,
Allen–Swenberg's, or a named published chain.

### Consequences for this project

- **Do not add an application.** The zero forcing number has real, citable
  origins — controllability of quantum spin networks, sensor placement in power
  grids — and those belong in one sentence of motivation. They must not become
  the claim. The claim is the theorem.
- **Lead with the attribution.** A published 2020 theorem about this family is
  *false*; a 2026 correction note records the corrected question as open for
  k >= 4; this work answers it. That provenance is what a non-specialist can
  verify without understanding any mathematics, and it is exactly what the
  three state winners lacked.
- **Lead with checkability.** "The proof is a matrix of whole numbers and a
  computer can verify it in exact arithmetic" is a claim of a kind that
  survives a panel with no mathematicians on it. It is also true, for k = 4
  and k = 5.
- **The bar is high and should be stated plainly.** Beating the three projects
  above is necessary and not sufficient. The target is top ~10 in the state
  across all categories, or top 7 at DRSEF across all categories.

### This does not mean diluting the mathematics

The strongest available evidence points the other way. At ISEF 2026 the
Mathematics first-place project — Veselinov's *Solvability of Meromorphic
Equations in Elementary Functions*, about as purely theoretical as the category
gets — also took the **Regeneron Young Scientist Award of $75,000**, one of the
two top prizes of the entire fair, which is decided by exactly the kind of
cross-category panel in question. Maximally pure mathematics won the
cross-category judgment outright.

What the press release did with it is the instructive part. The theorem became:
"a new theorem describing the conditions under which certain equations cannot
be solved using basic math functions." The technical content is untouched; only
the *question* is restated in words anyone can hold.

### Why this project is unusually well-placed for that panel

Most pure mathematics is hard to open to a non-specialist because the question
itself is technical. Here it is not:

- **The rule is elementary.** Colour some dots; if a coloured dot has exactly
  one uncoloured neighbour, that neighbour gets coloured; how few do you need
  to start? That is a puzzle anyone can play in twenty seconds with a diagram.
  The difficulty is entirely in the *answer*, not the *question* — which is the
  best possible position to be in with a general panel.
- **There is a narrative with stakes.** A 2020 published theorem about this
  number was *wrong*; a 2026 counterexample exposed it; the corrected note said
  the general case was open; this work answers it for two new cases. Judges
  understand "the published proof was false" without any mathematics.
- **The proof is a physical object.** The certificate is a matrix of whole
  numbers, and its correctness is checkable in exact integer arithmetic — no
  rounding, no floating point. That is tangible in a way most theory is not,
  and it speaks to rigour in a language non-mathematicians respect.
- **The applications are real and citable**, not retrofitted: controllability
  of quantum spin networks, and sensor placement in power grids.

### The actual weak point

Not the beginning and not the end — the **middle**. The distance from "colour
dots" to "cyclotomic polynomials and Galois orbits" is long, and a judge who
asks how one leads to the other needs a single sentence, not a lecture. The
honest bridge is the classical inequality M ≤ Z:

> Counting colourings directly is hard, but there is a theorem that converts it
> into a question about matrices — and matrices I can compute with. It works
> because a solution to the matrix equation that vanishes on a starting set is
> forced to vanish everywhere, propagating by *exactly* the colouring rule.

That sentence is the load-bearing one for a general audience, and it should be
rehearsed until it is automatic.

### A second reason to want a general-n theorem

The congruence conditions are a communication liability as well as a
mathematical one. "I settled it when n is divisible by 60, 70 or 90" invites
"why 60?", and the honest answer is technical (it is the lcm of the cyclotomic
orders). "I settled it for all large n" needs no caveat at all. The same gap
that weakens the result mathematically also weakens it rhetorically, which
raises the value of Priority 2 in Part 3 for an independent reason.

Eligibility: grades 9–12, TEA Region 10 (Collin, Dallas, Ellis, Fannin,
Grayson, Hunt, Kaufman, Rockwall counties).

### 2.2 Forms — for a pure math project

A mathematics project with no human participants, no vertebrate animals, no
hazardous biological agents and no hazardous chemicals needs:

| Form | What | When |
|---|---|---|
| **Form 1** | Checklist for Adult Sponsor / safety assessment | **before** research |
| **Form 1A** | Student Checklist + **Research Plan** | **before** research |
| **Form 1B** | Approval Form | **before** research |
| **Form 2A** | Student Support Disclosure | **before** research |
| **Form 3** | Risk Assessment | **before** research |
| **Abstract** | max 250 words, one page | **after** research |
| Form 7 | Continuation / Research Progression — **only if** this continues prior-year work | after |

Not needed: Forms 4, 5A/5B, 6A/6B (human participants, animals, biological
agents, tissue). Form 2B (Qualified Scientist) and 2C (Regulated Research
Institution) are only needed if a mentor or institutional lab is involved.

**The timing rule bites.** Forms 1, 1A, 1B, 2A and 3 are supposed to be signed
*before* research begins. Work here started around September 2026, so these
need to be dated and signed now rather than reconstructed in February.

### 2.3 The research window

> "Students will be judged only on laboratory experiment/data collection
> performed over 12 continuous months beginning no earlier than January 2026
> and ending May 2027."

Everything in this project falls inside that window. If any of it is presented
as continuing earlier work, Form 7 is required and the board and abstract must
show **the current year's work only**, with prior material clearly labelled.

### 2.4 The deliverables

| Item | Status | Notes |
|---|---|---|
| **Abstract** | **Required** | Max 250 words, one page, written after the research; must describe the *student's* work, not a mentor's. |
| **Display board** | **Required** | Max **30 in deep × 48 in wide × 108 in high** floor-to-top. The current poster is 48 × 48 in, which is exactly at the width limit — print at ~46 in to leave margin. |
| **Research paper** | *Not required, strongly recommended* | ISEF says recommended for judging; affiliated fairs may require it. `manuscript/zf_paper.tex` (11 pp) already serves. |
| **Project data book / log** | *Not required, strongly recommended* | `manuscript/zf_log.tex` (9 pp, dated entries) is unusually strong here — it records dead ends, refuted conjectures and self-corrections. |
| **Quad chart / visual abstract** | **Verify** | The ISEF "Rules for All Projects" page does **not** mention a quad chart. Secondary sources say it is required, and last year's DRSEF entrant submitted a visual abstract. Treat as required and confirm with DRSEF. |
| **Finalist Questionnaire** | Required at ISEF | Where the paperwork is submitted for SRC review. |

### 2.5 What is already in hand

- `manuscript/zf_paper.tex` — 11 pp research paper.
- `manuscript/zf_log.tex` — 9 pp dated research log.
- `manuscript/zf_guide.tex` — 14 pp foundations guide (not an ISEF deliverable,
  but it is what makes the project defensible under questioning).
- `manuscript/zf_poster.tex` — 48 × 48 in board poster, rebuilt.
- `verification/` — every claim reproducible; certificates verified in exact
  arithmetic.

### 2.6 What is missing

1. The **250-word abstract** — not yet written.
2. The **visual abstract / quad chart** in Q1–Q4 form.
3. **Forms 1, 1A, 1B, 2A, 3** signed and dated, plus a written Research Plan.
4. A **plain-language one-liner** for non-specialist Grand Prize judges.
5. Confirmation of the quad chart requirement and any DRSEF-specific paper
   requirement via STEM Wizard.

---

### Sources

- Society for Science abstract database — `abstracts.societyforscience.org`
- Society for Science, *Full Awards: 76th Regeneron ISEF* press release
- Society for Science, ISEF International Rules: Rules for All Projects;
  Display & Safety Rules; Forms
- Beal Bank Dallas Regional Science and Engineering Fair — students page


---

## Part 3 — Rescope, after seeing the field

Nothing about the *subject* needs to change. The field data says pure
mathematics owns the top of the Mathematics category, and this is a pure
mathematics project attacking an attributed open problem with cyclotomic and
Galois machinery. That is the winning shape already. No pivot.

What does change is **which open end to push on**, and the reason is a result
proved after the field analysis (Proposition, `zf_paper.tex`):

> For each `k`, the search over **rational** period-1 symbols is a *finite,
> complete* enumeration — `deg Ψ_d ≤ k+1` forces `φ(d) ≤ 2k+2`, so only
> finitely many `d` qualify. Carrying it out: `k = 2, 4, 5` attain `2k+2`;
> `k = 3, 6, 7, 8, 9` **cannot**, and that is a theorem about rational symbols,
> not a statement about how far the search went.

So the previously-stated plan — "search further for more cyclotomic families" —
is now known to be a dead end. It is finished, and it found everything there is.

**Revised priorities, in order.**

1. **Period-`d` symbols.** At `k = 7`, 378 of 385 rational candidates fail
   because `F` is not in the three-parameter family, and only 7 fail
   realisability. The binding constraint is `k−2` linear conditions imposed on
   a 3-dimensional family, and it tightens as `k` grows. A period-`d` symbol
   carries `5d−1` free ratios, so `d ≥ (k+2)/5` restores the count. This is the
   one change that addresses the actual obstruction rather than working around
   it. Highest value.

2. **General `n`, not more special `n`.** The gap between this project and the
   first-place shape is that Veselinov's theorem is a clean general statement
   while ours holds on congruence classes. One construction valid for all
   sufficiently large `n` is worth more than ten more residue classes. Note the
   ceiling theorem means such a construction would *settle the problem
   outright*, since the method's ceiling equals the upper bound.

3. **Irrational period-1 symbols for `k ≥ 6`.** Cheaper than (1), and the
   triple scan already showed irrational symbols beat rational ones at `k = 3`.
   Worth a bounded run before committing to (1).

4. **Deprioritised:** more exhaustive `Z` values by brute force; the
   `DP(n,k)` family; any attempt to add an "application." The field data says
   applications are a bonus that sits *on top of* a theorem, and chasing one
   would cost theorem time.

**What would actually move the tier.** Second-award shape is already in hand.
First-award shape needs one of: a general-`n` construction (settles the problem
for that `k`), a proof that the arithmetic obstruction is genuine (turns a
computational gap into a theorem), or period-`d` certificates reaching `2k+2`
for `k ≥ 6` (shows the method scales). Any one of the three is a clean,
statable general theorem rather than a table of values.
