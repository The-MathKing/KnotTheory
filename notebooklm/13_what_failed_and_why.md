# 13 — Dead ends, refuted conjectures, and self-corrections

This file exists because the failures are more instructive than the successes,
and because a research log that only records wins is not a research log. Every
item here actually happened, in order.

## 1. Three combinatorial lower-bound routes, all dead

Fort duality (file 04) says Z is a minimum hitting set over forts. Three
standard consequences follow — and all three fail on P(n,k), all degrading as k
grows:

- **Disjoint fort packing.** t pairwise disjoint forts give Z ≥ t. But forts
  here have 7–13 vertices in a graph of only 2n ≤ 56 vertices, and a greedy
  search found at most **two** disjoint forts in every case tested. The
  certificate cannot exist at those sizes — this is a structural impossibility,
  not a search failure.
- **The fort LP.** Computing the exact LP value by cutting planes gives
  LP/Z ≈ 0.43–0.50 — for example LP = 3.00 against Z = 7 for P(12,3), and
  LP = 3.21 against Z = 10 for P(18,4). The integrality gap is about 2 and
  widens with k.
- **Hoffman-type spectral bound.** Yields 1.2–2.9 against true Z of 6–12.

**What was learned.** All three failures are of one kind: asking a
combinatorial relaxation to certify a quantity it cannot see. The fix was not
to work harder inside the category but to **change the category of argument**,
to matrices. That instinct — when three attempts fail the same way, the category
is wrong — is the single most transferable lesson of the project.

Side benefit: the factor-2 LP gap also *explains* why fort-based exact solvers
converge slowly on this family. Branch and bound must close a factor-2 gap by
branching.

## 2. Conjecture refuted: the single threshold n_0(k) = 5k − 2

The data for k = 3, 4, 5 showed the bound 2k+2 first attained at n = 13, 18, 23
— exactly 5k − 2. The conjecture was that this is a **stabilization threshold**:
beyond it, Z(P(n,k)) = 2k+2 for all n.

It made a falsifiable prediction: n = 28 should be the first n with
Z(P(n,6)) = 14. That prediction was **recorded before the computation finished**
and was **borne out** after a 14.2-hour run.

Then Z(P(29,6)) = 12. Since 29 > 28, the value is *lost again*, so 28 is not a
stabilization point and the single-threshold form is false.

**The explanation.** Sort the k = 6 data by d = gcd(n,6):

| d | n | Z(P(n,6)) |
|---|---|---|
| 1 | 13, 17, 19, 23, 25, 29 | 6, 8, 8, 10, 10, 12 |
| 2 | 14, 16, 20, 22, 26, 28 | 8, 9, 10, 12, 12, 14 |
| 3 | 15, 21, 27 | 9, 12, 13 |
| 6 | 18, 24 | 9, 12 |

Each gcd class climbs on its **own** schedule. The class d = 2 reaches 14 at
n = 28 while the coprime class has only reached 12 by n = 29. At k = 4 and
k = 5 all classes had converged inside the computed range, which is why a
single threshold appeared to fit. The thresholds 10, 13, 18, 23 should be read
as "the point at which the slowest class happened to arrive", not as a formula.

**Lesson.** The sequences are non-monotone, so a run of equal values proves
nothing. Five consecutive equal values occurred at k = 5 (Z = 10 for
17 ≤ n ≤ 21) before the sequence moved to 11 and then 12.

## 3. Conjecture refuted: Z ≤ 2(gcd(n,j) + gcd(n,k))

Among 20 computed I-graphs with both gcds > 1, every one satisfied
Z ≤ 2(d_1 + d_2), with equality in four cases. Tempting.

But it is false in general: take j = 1 so d_1 = 1, and n coprime to k so
d_2 = 1; then the bound reads Z ≤ 4, while Z(P(n,k)) = 2k+2 grows without
bound. Z(P(11,3)) = 7 > 4 and Z(P(17,4)) = 9 > 4 both refute it.

**The failure mode.** The conjecture was generalised from 20 graphs *all
selected for* gcd > 1, and the excluded boundary case was never tested — even
though the refuting data was **already in the validation table**. The
observation survives only as a statement restricted to d_1, d_2 > 1.

## 4. Overstating a theorem's reach

The I-graph theorem Z(I(n,j,k)) ≤ 2(j+k) was initially presented as broadly
new. It is not: when gcd(n,j) = 1, multiplying indices by j⁻¹ mod n gives
I(n,j,k) ≅ P(n, j⁻¹k), so those graphs are generalized Petersen graphs and the
existing corollary already applied. The new content is confined to gcd(n,j) > 1.

Compounding it, the theorem was then called "mostly slack" on the basis of
sharpness measurements taken **outside its own hypothesis** n ≥ 2(j+k)+1. Both
errors are now stated explicitly in the paper.

## 5. The period-two detour — built to escape a cap that did not exist

Believing that period-one certificates were capped at 6, considerable machinery
was built to break past it: period-two equivariance, ten parameters, 4×4
Hermitian blocks, a determinant identity
det M = (a_0v_0 − c_0²)(a_1v_1 − c_1²) − |β|²v_0v_1, a reduction to
(x + μ)N(w) = L(w), and a search over a one-parameter pencil after discovering
that fitting five points always forced c² ≤ 0.

It worked, in the sense that it produced nullity 8 for P(n,4) and 10 for
P(24,6). Then the "cap of 6" turned out to be false (file 08 §5), period-one
certificates were found reaching 10 and 12, and **the entire period-two
apparatus became unnecessary**. Its results are superseded.

**Lesson.** The claim that justified months of machinery was never tested. When
the exhaustive check was finally written — expecting confirmation — it printed
12 immediately.

## 6. The numerical traps

Covered in detail in file 12. Briefly: a vanishing edge weight (3×10⁻⁴ against
scale 4.5) manufacturing a fake nullity 7 for P(14,2); a dense-grid tolerance
manufacturing nullity 7 for k = 2; a scaling failure manufacturing nullity 48
at (48,7). All three caught by a bound that must hold.

## 7. The monotonicity failure, and a conclusion drawn too early

A search over the combinatorially symmetric class returned a *smaller* maximum
nullity on P(12,2) than the symmetric search did. Since S(G) is contained in
that class, this is impossible — the search was faulty, not the mathematics.

The uncomfortable part: a conclusion had already been drawn from those numbers
— that even 8n parameters cannot reach 2k+2 at k = 3 — before the guardrail
caught the fault. That conclusion may well be true, but the evidence for it was
worthless, and it had already been written down.

## 8. Five consecutive misses in target selection

Before the zero forcing work, four candidate results in low-dimensional
topology were each found to be already known. A fifth came afterwards, and it
was the worst.

**The octal game 0.45.** Selected as a target on the belief that its
conjectured period-20 nim-sequence was unproved. Considerable correct work
followed: an independently written Sprague–Grundy engine validated eight ways
(reproducing Guy's 1949 Kayles result exactly, and four of Flammenkamp's
published period pairs), a genuine structural finding (the sequence is confined
to {1,2,4,7,8} beyond n = 198), and a bespoke proof with one honestly flagged
gap.

Then the audit. Flammenkamp's database has two tables. The one consulted gives
sequences and periods. The one **not** consulted is headed *Nontrivial
Octal-Games with known Structure* and ends in a `solved` column. Its row for
`.45` reads `… 11 200 8 37 1 0.4 **1956**`. The game was settled by Guy and
Smith in the paper that introduced the notation.

Worse: four statistics had been pulled from that **same row** as engine
validation (rare = 11, miss = 67, last+t = 200, maxG = 8, all reproduced to the
digit) without parsing the column that made the project pointless. And
independently, the Guy–Smith shift argument closes the game in half a page,
needing the sequence checked only to n = 2p + 2ℓ + t = 1038.

**The distinction that matters.** Misses 1–4 came from inferring openness from
*absence of evidence* — nobody had written the result down where I looked. Miss
5 came from reading a primary source that **stated the answer explicitly**, in a
column I did not parse. Volume of verification did not help; every computational
claim was correct, and two of them agreed with the database to the digit.

**Rule adopted.** Before committing effort, every column of every table in the
primary source that names the target must be identified by name, including
columns not being used. A source consulted for one field has not been read. If a
table has a `solved` column, read it first.

## 9. What survived from the failures

- The Sprague–Grundy engine, validated eight ways.
- A clean re-derivation of the Guy–Smith periodicity theorem.
- The instinct to change argument category after repeated same-shaped failures,
  which is what produced the matrix method.
- A working discipline: falsifiable predictions recorded in advance; searches
  wrapped in bounds they cannot violate; claims labelled proved / computed /
  open; and errors left in the log rather than edited out.
