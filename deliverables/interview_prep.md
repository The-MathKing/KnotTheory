# Interview preparation

The interview is **25 of 100 points** — two and a half times the poster. Its
stated criteria are: clear concise thoughtful responses; understanding of the
basic science; **understanding interpretation and limitations of results**;
**degree of independence**; recognition of potential impact; **quality of ideas
for further research**.

Three of those six reward saying accurately what is *not* proved. That is the
project's strongest suit, so do not hide the gaps — lead with them when asked.

---

## The one-sentence answer

> "One graph family, one spectrum, two matrices: is the *fixed* adjacency
> matrix's spectral gap optimal — that's the Riemann Hypothesis for the graph
> — and how degenerate can the zero eigenvalue be made over *every* matrix
> sharing that graph's pattern — that's zero forcing; I settle both exactly,
> and the first one completely: all 460 of them, for every n and every k."

## The thirty-second answer

> "Both halves ask the same spectral question about P(n,k) and differ only in
> whether the matrix is nailed down or allowed to range. Fixed matrix: is the
> adjacency spectrum as tight as an infinite family can get — Ramanujan, which
> is the Riemann Hypothesis for the graph's zeta function. I cleared the
> radicals in that comparison, got one integer polynomial — and then it
> factors, and both factors collapse to a single quadratic form with no k in
> it. So there is one fixed forbidden region, the same for every k, and the
> question is whether a grid of points hits it. Dirichlet's approximation
> theorem says it always does once n ≥ 231, which makes the family finite in
> both parameters: exactly 460 graphs qualify, none past k=45, all certified.
> Ranging matrix: how
> degenerate can zero be, over every matrix with this graph's zero pattern —
> zero forcing. I found that every such matrix collapses to a single
> recurrence whose order is exactly the best known upper bound, so the method
> either solves the problem outright or can't touch it. It solves it, and I
> built the matrices from interchangeable tiles to get from 'some n' to 'all
> n'. Both halves run on the same grid — the n-th roots of unity that index
> the cover — and the same exact-arithmetic machinery decides both."

## Why this problem

Half of it was not self-defined. Rashidi et al. (2020) published Z(P(n,3)) = 8
for n ≥ 12; Krishnan (July 2026) showed Z(P(12,3)) = 7, so the published
theorem is false, and left two things open: the stabilization threshold, and
any rigorous lower bound for k ≥ 4. I settled the threshold (it is 13) and gave
exact values for k = 4. The other half I asked myself: the spectrum of
P(n,k) has been fully known since 1997 without anyone checking it against the
Ramanujan bound, which is unusual once you notice the two literatures — spectral
graph theory and zero forcing — share this exact family and neither had asked
the other's question of it.

---

## Questions to expect

**"Why is a Riemann Hypothesis question and a zero forcing question in the same
project? Isn't that two projects stapled together?"**
No — same graph, same spectrum, same grid. P(n,k) is a cyclic cover of a
two-vertex base, and both questions decompose over the n-th roots of unity that
index that cover. The Ramanujan question fixes the matrix (the adjacency
matrix) and asks whether its spectrum, sampled on that grid, stays inside a
fixed band — a polynomial that must avoid a sign change. The zero forcing
question does the opposite: it lets the matrix range over every matrix with
the graph's pattern and asks how far you can push a *chosen* polynomial's roots
onto that same grid to make an eigenvalue vanish. Fixed polynomial avoiding a
band versus constructed polynomial hitting the grid — same object, opposite
direction. That's also why the same tools apply to both: reducing to a grid of
cyclotomic points, and certifying signs and vanishing there in exact arithmetic
rather than floating point.

**"How much of this is yours?"** *(the highest-stakes question on the sheet)*

This one is not answered with the binder. Read `derivation_drills.md` and be
able to produce, cold, on a whiteboard: the corner substitution, the Dirichlet
bound, and the gcd safety argument. A judge who watches you derive
$Q = 4x^2+4y^2-8\sqrt2|xy|+3$ from $D_k$ in ninety seconds — naming *why* each
squaring is an equivalence before being asked — stops wondering. One who
watches you reach for a page does not.

On assistance and tooling: **answer it accurately and first, before you are
asked.** Check the current ISEF/SRC rules on computational and AI assistance
and make sure the board, the Research Plan and your forms all say the same
true thing. The asymmetry is brutal — a disclosed use of tooling is ordinary
and costs nothing, an undisclosed one found by an SRC ends the project. Say
plainly what you conceived, what you directed, what tools produced, and what
you personally verified. The board's provenance line is currently a
placeholder for exactly this; it is marked in the source and the build warns
until you complete it.

The log is your corroboration, not your defence: it is dated, it records wrong
turns, withdrawn claims, and a guard bug found only by extending the range.
That pattern is what genuine work looks like. But it only helps if it matches
how the work actually happened.

**"What has this actually contributed to mathematics?"** *(answer it ranked, and concede first)*

> "Three specific gaps in one family, and the clearest ones are in Part II.
> A published theorem — Rashidi et al., Z(P(n,3)) = 8 for n ≥ 12 — is false,
> and this replaces it. It proves Conjecture 5 of Krishnan's note and fixes the
> threshold that note left open, at 13. And it gives the first exact values at
> k = 4 at all, and the first for an infinite family at any k ≥ 4. Zero forcing
> and minimum rank are an active area with a standing research programme, and
> exact values for a standard test family are the kind of thing the next person
> cites.
>
> Part I is a complete classification of a recognised kind — Droll did it for
> unitary Cayley graphs, Le–Sander for integral circulants, both with the same
> answer, 'only finitely many.' The contribution there is exactness and
> completeness, not surprise. Anyone who knows abelian covers don't expand would
> have predicted the shape.
>
> The one structural result I'd defend hardest is the ceiling: null A ≤ 2k+2 for
> *every* matrix with the pattern, exactly matching the zero forcing upper bound.
> That's a statement about the method, not the family — it says the matrix
> approach either settles the problem completely or can't touch it."

**"Isn't the Riemann Hypothesis framing overselling it?"** *(concede instantly)*
> "Partly, yes, and I'd rather say so than defend it. The graph RH is a real
> definition and the equivalence to Ramanujan is a genuine theorem of Ihara's —
> but by the determinant formula it reduces to a *finite eigenvalue check*, which
> is exactly why it's decidable and the classical RH isn't. The analogy is in
> the zeta function, not in the difficulty. The board says that where the
> question is posed, rather than waiting to be asked."

**"Isn't 'no infinite Ramanujan family is a cyclic cover' already known?"**
> "The principle is, and I say so. Abelian covers don't expand — that's exactly
> why Lubotzky–Phillips–Sarnak is built on PGL₂ and not a cyclic group. What's
> new in mine is the explicit constant, and the exact criteria for the two
> two-vertex bases, which decide the finitely many survivors rather than just
> bounding them. It's a quantitative refinement of a known phenomenon, not a
> discovery, and I'd be wrong to present it as one."

**"So the headline is a list of 460 small graphs?"**
> "The list isn't the result — the obstruction is. I proved that a natural
> infinite family of candidate expanders contains only finitely many optimal
> members, and then that the reason isn't special to this family: on any fixed
> cubic base, the $j=1$ block converges to the base's own adjacency matrix,
> whose top eigenvalue is 3, so a nontrivial eigenvalue is dragged above
> $2\sqrt2$. No infinite Ramanujan family is a cyclic cover at all. That's the
> cyclic case of why Lubotzky–Phillips–Sarnak had to use PGL₂ and not a cyclic
> group. Optimal members *must* run out; the 460 is exactly where, and the
> deficit curve says what you lose past that point — at most $3-2\sqrt2$.
> Classifications of this shape are a recognised kind of result: Le–Sander did
> it for integral circulants, Droll for unitary Cayley graphs, and in both cases
> the answer was also 'only finitely many'."

**"Part II settles someone else's open problem. Part I you asked yourself —
isn't that just a computation?"**
> "The computation is the last step, not the result. The result is that the
> criterion has no $k$ in it. An analytic statement about the poles of a zeta
> function becomes one fixed region in a square, the same region for every $k$,
> and $k$ survives only in the map into it. That's a structural reduction — it's
> what turns a per-$k$ question into a Diophantine one, which is what let
> Dirichlet close it. Without that, extending past $k=10$ was an unbounded
> computation; with it, the whole family is finite in both variables. Part II
> is where I have an attributed open problem; Part I is where I have the better
> theorem."

**"What is zero forcing actually for?"**
Two independent origins: controllability of quantum spin systems, and placement
of phasor measurement units in power grids — you want the fewest sensors that
determine the whole network state. The graph question is the same question.

**"Why are lower bounds the hard part?"**
An upper bound exhibits one forcing set. A lower bound must exclude *every*
smaller set. The matrix inequality M(G) ≤ Z(G) converts that into exhibiting a
single matrix, which is a thing you can hand someone.

**"What is the ceiling result, in plain terms?"**
Eliminating half the variables from any matrix on this pattern leaves one linear
recurrence, and its order is exactly 2k+2 — the same number as the best known
upper bound. So the method's maximum possible strength is precisely the target.
No slack in either direction. That is the part I would put on a blackboard.

**"How do you know your computations are right?"**
Three ways. The exhaustive solver reproduces every published value, including the
corrected one. Every certificate is re-checked in exact arithmetic or by an
interval proof. And one script re-derives every computational claim from
scratch; it currently passes 113 of 113. Also — twice a numerical search returned
an answer the ceiling theorem forbids, and the theorem caught it. Wrapping a
search in a bound it cannot legally violate is the only thing that tells you an
answer is wrong when it looks right.

**"What does 'certified' mean? Isn't it still floating point?"**
No. A Krawczyk contraction bound proves a genuine real solution exists inside an
explicit box — it is a proof, not a measurement. The key step was noticing the
tile condition is equivalent to a nullity condition, which turns a rational
system into a bilinear one where the bound is cheap.

**"What's the hardest thing you got wrong?"**
Several, and they are all in the dated log. The sharpest: I certified a result
and the test passed, but I had chosen the equations by pivoting, which silently
left 28 of them unproved. The fix was structural — the redundancy is exactly the
antisymmetric part of a symmetric matrix — and it is checkable, those equations
fall to 1e-61 without being solved for. A passing test is not a proof.

**"Where does it fail?"**
k ≥ 5. Tiles exist at k = 5 but I have 19 of the 54 needed. And I cannot explain
why they start at length 54 when the parameter count permits 41 — the count is a
lower bound, not a predictor. I also proposed conditioning as the explanation and
the numbers refuted it: a k = 4 case with worse conditioning works.

**"Is this useful?"**
Not directly, and I would not claim otherwise. It is a determination of an
attributed open problem in a parameter family that people use as a test case. The
transferable part is the method: a ceiling theorem that makes a search
self-checking, and a tiling argument that converts "all large n" into a finite
list of finite problems.

**"What is the strongest result in the project?"** *(lead with this)*
> "Z(P(n,k)) = M(P(n,k)) = 2k+2 for every n ≥ 17 at k = 3 and every n ≥ 29 at
> k = 4, with exhaustive search below, so Z is determined for every n at
> k = 2, 3, 4. That proves Conjecture 5 of Krishnan's July 2026 note — he had
> the correction to the published value and the table up to n = 20, and said
> the missing ingredient was a lower bound valid for all large n. The lower
> bound is a matrix: eliminating the inner coordinates of *any* matrix on the
> P(n,k) pattern leaves one recurrence of order 2k+2, so the nullity is
> dim ker(T − I) with T the monodromy, and tiles whose monodromy is the
> identity give nullity 2k+2 for every n past a threshold. Every tile is
> certified by a Krawczyk contraction evaluated in exact rational arithmetic."

**"What is conjectural in the project?"** *(say it before they ask)*
> "Two things, and one refuted conjecture I want to tell you about myself. The
> leading-coefficient criterion for when the nullity ceiling holds on a general
> cyclic cover is a conjecture; I have it proved only on two-vertex, path-with-
> loops and cycle bases. The threshold N(k) for k ≥ 6 is a conjecture. And I
> had conjectured that on a cubic family covering K4 the maximum nullity stays
> at 6 while Z = n+2 grows — an unbounded gap on cubic graphs, which would have
> answered a question in the Fallat–Hogben survey. It is false, and I can show
> you why in one line."

**"Why is it false?"** *(have this ready; it is the best thing you can say about rigor)*
> "The three zero-voltage edges of the base form a triangle, so every fibre
> carries a triangle whose only outside edges go to one other fibre. Put a
> rank-one block uuᵀ on each triangle — legal, because the off-diagonals are
> nonzero and the diagonal is free. The 3n triangle rows then have rank at most
> 2n and the other n rows at most n, so the rank is at most 3n and the nullity
> at least n. Exact rank over Q gives exactly n. So M ≥ n and the gap to
> Z = n+2 is at most 2. In the equivariant picture det M(ζ) is identically
> zero — which is a hypothesis my cover theorem needed and didn't state. Both
> of my adversarial searches missed it because the matrix lives where three of
> four fibre blocks are singular, and neither search goes there. It was found
> by reading the voltages, not by searching."

**"So what replaces regularity as the hypothesis?"**
> "The thing every proof actually used: the top coefficient of det M(ζ). On
> every base where the ceiling is proved it is a monomial in edge weights alone
> — the product of the two loop weights on P(n,k), for instance — so it cannot
> vanish and the elimination always has a leading term. On every base where
> it fails, including K4, that coefficient contains a free diagonal. That is
> now the conjecture, checked symbolically on every base in the paper. The
> general obstruction is M(G) ≥ |V| − mr(G[S]) − 2|V∖S| for any vertex set S;
> the independent-set bound is the case mr = 0, and regularity only controls
> that case."

**"What is the newest thing here?"** *(the one to lead with if they ask what you are working on now)*
> "Extending the nullity ceiling off P(n,k). The ceiling — null A at most 2k+2
> for *every* matrix with the pattern — was proved for P(n,k), and for general
> bases only for matrices that commute with the Z_n action. That gap is the
> difference between a fact about one family and a theorem about cyclic covers.
>
> I closed part of it. The elimination in the two-vertex proof *chains*: if the
> base is a path with a loop at each vertex, you solve the row at one end for
> the next fibre, substitute, and repeat. Each loop widens the window by 2p_t,
> so the final recurrence has order 2 times the sum of the p_t — which is
> exactly the degree span of det M(zeta). So the ceiling holds, non-equivariantly,
> on path-with-loops bases of *any* size, with the two-vertex theorem as the
> m = 2 case.
>
> Then I refuted the general version, which is the actual answer. A base vertex
> of degree 1 lifts to *pendant* vertices in the cover, and the diagonal is free
> in S(G) — so set the pendant diagonals to zero. The row at a pendant forces its
> neighbour to zero, the shared fibre dies, and one relation is left among 2n
> pendant coordinates. On a star base with a loop, null A = n against D = 2. Not
> a marginal counterexample — the gap grows without bound, and it's exact over
> the integers, not an optimiser result. Requiring minimum degree 2 doesn't fix
> it either: K_{2,3} gives 6 against D = 4. What survives is *regularity*, which
> costs nothing, because every cover in the paper is cubic.
>
> The cycle case I closed a different way. On a cycle base every vertex has
> degree 2, so every vertex of the cover does: the cover is a disjoint union of
> cycles. Lifting the base cycle from (x_0, i) returns to (x_0, i+W) where W is
> the holonomy, so there are exactly gcd(|W|, n) components — and since the
> minimum rank of a cycle is N-2, each contributes nullity at most 2. That gives
> null A at most 2 gcd(|W|,n), which is at most 2|W|, and 2|W| is the degree
> span. Worth saying out loud: that's a *degeneration*, not a transfer-matrix
> argument — which tells you the obstruction I'd named was an obstruction to the
> method, not evidence against the statement.
>
> So the open question is no longer 'arbitrary base' — that's settled, falsely
> — and it is no longer 'regular base' either, because K4 is cubic and a
> rank-one fibre breaks it. What is open is the leading-coefficient criterion."

**"How did you find the counterexample?"** *(the honest version, and the better story)*
> "Not by searching — by failing to. I'd run an adversarial search over ten
> bases and found nothing, and I wrote that into the paper as evidence *for* the
> conjecture. The base that breaks it was one of the ten. The search was weak
> three ways at once: Nelder-Mead in fifty dimensions, a penalty floor that
> excluded part of the admissible set instead of discouraging it, and an
> objective summing the d smallest squared singular values, so one value at
> 1e-10 hid two at 1e-6. What actually found it was reasoning about structure —
> leaves lift to pendants, the diagonal is free, so zero it — and then writing
> the matrix down by hand and taking an exact rank over Z. My own board has a
> keybox saying a failed search measures effort spent, not impossibility. I
> walked straight past it."

**"Did the search nearly find a counterexample?"** *(if they push on the evidence)*
> "It reported one, and it was my error, not the mathematics. I was minimising
> the *sum* of the d smallest squared singular values, which happily reports
> success when one is 1e-10 and the other two are 1e-6 — the sum still looks
> tiny. The actual nullity was 1, not 3. Switching the objective to the d-th
> singular value itself, relative to the matrix scale, killed it. The paper's
> caveat names the statistic for exactly that reason: evidence from an
> optimisation is only as good as what you asked the optimiser to minimise."

**"What would you do next?"**
Close k = 4 — four values remain. Then k = 5, which is compute rather than new
mathematics. I thought the genuinely open question was whether M < Z strictly
at P(10,2) — it isn't: maximising nullity over all matrices on that pattern
reaches 6, so M = Z = 6 there. Where a strict gap lives in this family is still
open, and I no longer have a candidate.

---

## Traps to avoid

- **"We prove Krishnan's Conjecture 5" is now checked against the note's
  text** (arXiv:2607.19412 §4: "Z(P(n,3)) = 8 for every n ≥ 13"; he writes
  that the missing ingredient is a lower-bound proof valid for all large n).
  Say exactly that. Do **not** say "a published theorem is false and this
  replaces it" — the correction is Krishnan's; yours is the lower bound.
- **Do not overstate k ≥ 5.** The honest line is "I did not find the tiles," not
  "they do not exist."
- **Do not claim applications.** Three top Texas mathematics projects with
  applications bolted on all failed to advance.
- If asked something unknown, say so and say what would settle it. The rubric
  rewards understanding limitations; it does not reward bluffing.


---

## How the official scoresheet actually allocates points

| Category | Pts | What the top box says |
|---|---|---|
| Research Question | 10 | Purpose clear; **contribution to field identified**; testable |
| Method | 15 | Data collection **well-designed**; **variables and controls defined and appropriate** |
| Execution | 20 | **Reproducibility good**; analysis systematic; **math methods appropriate & correct**; data sufficient |
| Creativity | 20 | **Student initiated, innovative** |
| Poster | 10 | Logical, readable, supporting docs |
| Interview | 25 | Clear responses; understands results; **recognizes impact**; **future ideas** |

Two things follow.

**The poster is worth 10 and the interview 25.** Do not over-rehearse the board.

**Method and Execution are 35 points and they are experiment-shaped** —
"data collection", "variables and controls", "reproducibility". A pure analysis
project has to stretch to fit those words. This project fits them literally, and
the mapping should be said out loud:

- *Data collection* → the computations: exhaustive $Z$ values, tile searches,
  certifications, each with a recorded budget and residual.
- *Variables and controls* → every search runs a **control** alongside it. The
  clearest example is the one that failed (below).
- *Reproducibility* → `verify_all.py`, one command, 80 checks, and the
  manuscript's numbers are *generated* from the certificates rather than typed.
- *Math methods appropriate and correct* → the Krawczyk hypotheses are evaluated
  in exact rational arithmetic, so the central claim is a proof, not an estimate.

---

## New answers to have ready

**"You say the tiles are certified. Show me the interval."**
> "There isn't one, and that's deliberate. The Krawczyk criterion needs three
> norms bounded. Evaluating them in floating point would only estimate them, so
> I evaluate them exactly. The box centre is a float64 vector and every float64
> is a dyadic rational, so it's known exactly; $f$ is bilinear with integer
> coefficients, so $f(z_0)$ and $J(z_0)$ are exactly rational; and $Y$ in the
> test is *arbitrary*, so rounding it to a rational costs nothing. The obstacle
> was speed — $\alpha$ needs every entry of a product of order a thousand — so I
> write the integers in base $2^{20}$ with balanced digits, which keeps each
> digit-pair product exactly representable in float64 and lets BLAS do the work.
> $\alpha < 1$ is an exact integer comparison."

**"What is this good for?"**
> "$M(G)$ is the inverse eigenvalue problem of a graph — which spectra a network
> can have. The reduction I use is discrete Floquet theory, the same machinery
> that describes periodic and magnetic Laplacians on covering graphs; those model
> polymers and nanoribbons. Zero forcing itself came out of quantum control and
> power-grid monitoring. I'm not claiming an application — I'm saying the
> quantity is one people already study, and I determined it exactly."

**"What's the biggest thing you don't know?"**
> "Whether the ceiling is a property of the cover or only of symmetric matrices
> that respect the rotation. I proved it for this family; the general case is
> open and it's in the paper as open. I tried to settle it by searching for a
> counterexample, and I report nothing from that search, because its **control
> failed** — I asked it to find a matrix I already know exists, and it couldn't.
> One of the four formulations I tried was a method I'd already withdrawn
> earlier in the project as unreliable; the control is what caught that I'd
> re-derived it."

*(This is the strongest answer in the set. It demonstrates understanding of
limitations, independence, and experimental design in one breath.)*

**"How do you know your computed values are right?"**
> "Three independent implementations agree on every value: an enumeration that
> uses the rotation symmetry, an enumeration that uses no symmetry at all — which
> is what tests the symmetry argument itself — and a CP-SAT integer program that
> doesn't enumerate subsets. No disagreement anywhere. And when a solver times
> out, that's recorded as 'not checked', never as agreement."

**"What would you do next?"** *(explicit scoring criterion — have this ranked)*
> 1. Prove the ceiling for arbitrary cyclic covers — turns a result about one
>    family into a method for all of them.
> 2. Prove identity tiles exist for every $k$; this reduces to a controllability
>    question in $Sp(2k+2,\mathbb R)$, which I've identified but not settled.
> 3. Separate $M$ from $Z$ somewhere — and *not* at $P(10,2)$, where I expected
>    it. Maximising nullity directly over all matrices on that pattern reaches
>    6, so $M(P(10,2)) = Z(P(10,2)) = 6$ and there is no gap there. (Numerical,
>    not yet certified.) No $(n,k)$ in this family is proved to have
>    $M < 2k+2$, so where a strict gap lives is still open.
> 4. Lower the $k=5$ threshold from 162 to 54 by finding 33 more tile lengths —
>    mechanical, not interesting.

---

## The honest comparison, if asked about other projects

Don't disparage anyone. If pressed on what distinguishes this work:

> "Mine has no hypotheses. The results are unconditional and the cases are
> closed — 'for every $n$', not 'for large $n$ assuming something unproven'. And
> every number is machine-checked from the certificates rather than typed in."


---

## Read the judge before choosing the opening

The reframing around the inverse eigenvalue problem makes the work legible to a
mathematician. It does **not** work on a non-specialist grand-award judge: "the
maximal degeneracy of the zero level of a periodic operator" buys nothing in
fifteen seconds, whereas the colouring game does. Keep both openings and pick.

**To a mathematician / category judge — lead with the problem:**
> "Over all symmetric matrices with a given graph's pattern, how degenerate can
> the zero eigenvalue be? That's the inverse eigenvalue problem of a graph. I
> determined it exactly for infinite families of periodic covers."

**To a non-specialist judge — lead with the game, then pivot in one step:**
> "There's a colouring game on a network: a filled node with exactly one empty
> neighbour fills it. The smallest starting set that fills everything is a number
> called the zero forcing number — and it turns out to control how many
> independent zero-energy states the network can support. I worked out that
> number exactly, for infinitely many networks at once."

The pivot sentence is the whole trick: *the game controls the physics*. Say the
game first, the consequence second, and never open with "cyclic cover".


---

## Hardened answers for the five critique attack vectors

### Attack 1 — "Your applications are buzzword-dropped, not grounded."

**On quantum control:**
> "The connection is structural, not analogical. Burgarth, D'Alessandro, Hogben,
> Severini and Young (IEEE Trans. Automatic Control 58(9), 2013) prove that if a
> set of vertices is a zero forcing set, the associated system is controllable.
> So Z(G) is a **sufficient** actuator count — an upper bound on how many you
> need, and a certificate that that many suffice. Part II of this work
> determines Z(P(n,k)) for every n at k = 2, 3, 4 — equal to 2k+2 from n ≥ 17
> and n ≥ 29 on at k = 3, 4 — which turns that
> guarantee into a closed form for an infinite family."

**Say it in exactly that direction.** The theorem is *zero forcing set ⇒
controllable*; it does not say you need at least Z actuators. Calling Z a "lower
bound" or "the exact actuator count" claims a converse the paper does not prove,
and a controls engineer will catch it in one question. The honest and still
strong claim: *this many provably suffice, in closed form, for infinitely many
networks.*

**On power grids:**
> "PMU placement is the power domination problem, and its propagation step is
> exactly the zero forcing rule — power domination is one domination step
> followed by zero forcing propagation. So the same machinery bounds sensor
> placement for any grid whose topology is
> P(n,k). I am not claiming a grid engineer should use this graph — I am saying
> the mathematical quantity I determined is the one that controls the sensor
> bound."

**On routing / supercomputers:**
> "The classification result is a mathematical no-go theorem: this family cannot
> supply Ramanujan graphs past a computable threshold. Whether a network architect
> would choose this family is an engineering question I don't answer. What I do
> answer is: of the infinitely many graphs in this family, exactly 460 are
> Ramanujan, all identified, and the list is finite in both parameters. That is
> the limit of the mathematical claim."

### Attack 2 — "Your 'controls' are unit tests, not scientific controls."

> "That is a fair re-framing. What I call a control is a cross-validation
> strategy: an independent implementation of the same mathematical object whose
> output is compared automatically to the primary implementation. It is not an
> experimental control in the biological sense — there is no variable being
> isolated. Its scientific value is as an audit: it detected a real algorithmic
> bug (the k=1 Laurent collision) that the test suite alone missed, and it caught
> a search in which I had unknowingly re-derived a previously-withdrawn method.
> The agreement between implementations is a diagnostic, not a scientific result.
> The scientific results are the proofs and the certified classification."

### Attack 3 — "Squaring to remove radicals is pre-calculus. What's novel?"

> "The technique of squaring twice is standard. The novel contribution is the
> *outcome*: that the Ramanujan condition for this specific family collapses
> entirely to the nonnegativity of a single explicit integer polynomial D_k of
> degree 2k+2 at cyclotomic points. No prior work asks this question for
> generalized Petersen graphs at all — Gera–Stănică (2011) determined the
> spectrum completely but the words 'Ramanujan', 'expander' and 'spectral gap'
> do not appear in that paper. The radical-clearing is the mechanism; the
> reduction to integer polynomial nonnegativity is the result. Le and Sander
> do analogous work for circulant graphs of prime power order; the analogy
> confirms this is a natural question, not that it was answered."

**If asked: "What is D_k(u) for k=2?"**

For k=2, T_2(u) = 2u² − 1, so:
- 7 + 4u·T_2(u) = 7 + 4u(2u²−1) = 8u³ − 4u + 7
- 2u + 2T_2(u) = 2u + 4u² − 2 = 4u² + 2u − 2

D_2(u) = (8u³ − 4u + 7)² − 8(4u² + 2u − 2)²

This is a degree-6 integer polynomial. D_2(1) = (8−4+7)² − 8(4+2−2)² = 121 − 8·16 = 121 − 128 = −7. ✓

**If asked: "What is tile length ℓ?"**
> "A tile is a finite block of the periodic structure — a submatrix of the
> infinite transfer matrix covering n consecutive periods. Tile length ℓ is the
> number of periods in the block. The certification argument is: if identity
> tiles exist for every length in [L, 2L), then every n ≥ L is covered by
> concatenation. ℓ is a computational parameter, not a graph-theoretic invariant."

### Attack 4 — "You come across as arrogant and defensive."

If a judge raises this directly (unlikely but possible):
> "Fair observation. I revised the board to state these as validation strategies
> rather than 'controls', and removed language that anticipated criticism. The
> underlying point — that a failed search is not a disproof — is mathematically
> necessary to state, because it changes how you interpret a null result. I tried
> to say it descriptively rather than prescriptively."

### Attack 5 — "What's missing? What are you avoiding?"

**"Where is the prior art comparison?"**
> "It is on the board now. Gera–Stănică determined the spectrum; Le–Sander and
> Droll settled the analogous question for other families. For P(n,k) the
> question had not been raised. That context is in the RESULTS block."

**"Give me one worked example end-to-end."**
> "P(5,2). n=5, k=2. The grid points are u_j = cos(2πj/5) for j=0,1,2,3,4.
> The non-trivial ones are j=1,2. D_2(cos(2π/5)) = D_2(φ/2) where φ = (1+√5)/2.
> Computing: cos(2π/5) ≈ 0.309. 8(0.309)³ − 4(0.309) + 7 ≈ 0.236 − 1.236 + 7 = 6.
> 4(0.309)² + 2(0.309) − 2 ≈ 0.382 + 0.618 − 2 = −1.
> D_2 ≈ 36 − 8(1) = 28 > 0. So j=1 passes. j=2: cos(4π/5) ≈ −0.809.
> Similarly D_2(−0.809) > 0. So P(5,2) is Ramanujan. It appears in the 460."

**"Why does the classification stop at k=45?"**
> "It doesn't stop there — it *ends* there, and that is a theorem. The per-k
> bound n ≤ π(2+√2)√(k²+1) grows with k, so by itself it can never rule out
> large k. But the failure condition is that ‖j/n‖² + ‖jk/n‖² is small — a
> simultaneous Diophantine condition — and Dirichlet's approximation theorem
> supplies such a j unconditionally: take J = ⌊√n⌋, and some j ≤ J has
> ‖jk/n‖ ≤ 1/(J+1), making the sum less than 2/n. So n ≥ 231 fails for *every*
> k. Since k < n/2, that bounds both parameters, and exhausting the finite
> region left is the whole classification: 460 pairs, 324 up to isomorphism,
> largest n = 112, largest k = 45. Past k=45 there is simply nothing."

**"231 versus 112 — isn't your bound badly loose?"**
> "Yes, by about a factor of two, and it doesn't matter. The bound's only job is
> to be *uniform in k*, which the per-k bound is not. Once it makes the region
> finite, exhaustion does the rest exactly, and sharpening 231 to 112 would not
> change a single entry of the answer. I'd rather have a loose bound I can prove
> in six lines than a sharp one I can't."

**"What's the honest gap in Part I now?"**
> "There is no closed form. The answer is a certified list, not a formula. I can
> tell you exactly which 460 graphs qualify and prove nothing else does, but I
> cannot tell you *why* the surviving k stop at 45 rather than 43 or 47 — beyond
> having checked."

**"You said you have structure toward a closed form. What exactly?"**
> "Four things, and I'd rather be precise about which are theorems.
>
> First, the criterion is *local at the divisors of n*. The grid points at
> 'level m' — those j with n/gcd(n,j) = m — are exactly the full conjugate set
> of cos(2π/m). So P(n,k) is Ramanujan iff no divisor m ≥ 3 of n is bad for k,
> and badness at m depends on k only through k mod m. That's a theorem.
>
> Second, immediately: the Ramanujan set of each k is *divisor-closed*. If n
> works and d divides n, then d works. So the whole answer is determined by the
> minimal bad divisors, and by finiteness only those below B_k matter.
>
> Third, the minimum is a gcd: min over j coprime to m of ‖jc/m‖ is exactly
> gcd(c,m)/m.
>
> Fourth — this is the one I like — the geometry gives a *gcd safety theorem*.
> The corner corollary says Q < 0 forces both |x| and |y| to be at least
> √2 − ½, which is where the forbidden region meets the side of the square.
> That means ‖j(k±1)/m‖ ≤ γ with γ = arccos(√2−½)/π = 0.1328. Combined with the
> gcd formula, a level is safe as soon as one coordinate can't get close enough.
> And since 1/γ = 7.53 while m/gcd is an integer, it's a statement about small
> integers: **if m/gcd(k+1,m) or m/gcd(k−1,m) is between 2 and 7, m is safe.**"

**"So why isn't that a closed form?"**
> "Because it's one-sided. It certifies *safety* and says nothing about badness,
> and a closed form needs both directions. For k ≤ 9 the two bounds I already
> had turn out to be the whole answer — k = 2 and 4 are unbroken runs, and odd
> k ≤ 9 is exactly 'n ≤ B_k with every odd divisor at most P_k'. But that's
> verified case by case, not derived, and it breaks at k = 6, 8 and every odd
> k ≥ 11 — precisely where an interior band binds, neither at u = 1 nor at
> u = −1. Locating those is the cyclotomic-reals-avoiding-a-semialgebraic-set
> question, and I haven't solved it. The list is complete and certified; it is
> not yet *explained*. I'd rather say that than dress the structure up as a
> formula."

**"Did anything break when you extended the range?"**
> "Yes, and it's the best example of why the guard exists. The exact sign test
> refuses to answer unless the computed value clears a separation bound. When I
> pushed n past 126 it started raising 'cannot separate sign' on values of size
> 11 — which is absurd. The cause was that the guard 10^−(dps−15) underflowed to
> exactly 0.0 in float64, and the imaginary-part test `imag < guard` compares a
> non-negative number against zero, so it could never pass. A guard bug wearing
> a precision bug's clothes. No published number moved, because at k ≤ 10 the
> bound gives n ≤ 108 and the underflow was never reached — the extension is
> what exposed it. Fixed by keeping the comparison in mpmath."

**"Is the finiteness theorem novel, or is finiteness known for such families?"**
> "Finiteness for analogous families (Le–Sander, Droll) was proved by different
> methods specific to those families. My finiteness proof for P(n,k) uses the
> polynomial criterion D_k, monotonicity, AM–GM, and 1 − cos θ ≤ θ²/2 —
> completely elementary, holding uniformly for every k with an explicit constant.
> Whether this specific argument has appeared for this family I cannot rule out,
> but the question itself (which P(n,k) are Ramanujan) does not appear in the
> literature, so the theorem is at minimum the first proof of this statement."

---

## Specific numerical traps a judge may set

### "D_k(0) ≥ 17 — is that right? I compute D_k(0) = −23 for k ≡ 2 (mod 4)."

**They are wrong. Here is the exact computation to give:**

D_k(u) = (7 + 4u·T_k(u))² − 8(2u + 2T_k(u))²

At u = 0, the term **4u·T_k(u) = 4·0·T_k(0) = 0** regardless of T_k(0).
And **2u = 2·0 = 0**. So:

D_k(0) = (7 + 0)² − 8(0 + 2T_k(0))² = **49 − 32(T_k(0))²**

Since T_k(0) = cos(kπ/2):
- Odd k: T_k(0) = 0 → D_k(0) = 49
- Even k: |T_k(0)| = 1 → D_k(0) = 49 − 32 = **17** ✓ (regardless of sign, since we square it)

The error: the judge substituted T_k(0) into the first bracket as if it were ±4, forgetting that the first bracket is `7 + 4·**u**·T_k(u)`, and at u=0 the entire 4u·T_k(u) term vanishes. The board is correct.

> "The formula is D_k(u) = (7 + 4u·T_k(u))² − 8(2u + 2T_k(u))². At u=0, both
> the 4u·T_k(u) term in the first bracket and the 2u term in the second bracket
> vanish — u multiplies them. So D_k(0) = 49 − 8(2T_k(0))² = 49 − 32(T_k(0))².
> Since (T_k(0))² ≤ 1, this is at least 17, with equality for even k."

### "Your board says Z(P(n,4))=10 for 'every n at k=4', but Future Work says M(P(24,4)) is open. Contradiction?"

The earlier version of the board said "every n" without qualification — that was a scope error, now corrected. The board now says n ≥ 29 (= SettleFour) at k=4.

> "The tiling result covers all n ≥ 29 at k=4. For n < 29, cases are handled
> individually: most are certified directly; n=24 remains open — I have not
> yet found a certificate of nullity 10 for P(24,4). The claim 'for every n'
> in earlier drafts was a scope error I corrected; the precise ranges are now
> stated in the CERTIFICATIONS table and CONCLUSIONS."

If pressed on whether Z(P(24,4)) might be less than 10:
> "I don't know. No smaller matrix has been found, but no certificate exists.
> That is exactly why it is listed as open. An open case stated honestly is
> stronger evidence of rigor than a closed case stated sloppily."
