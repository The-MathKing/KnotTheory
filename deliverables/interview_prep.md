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

> "A 2020 paper claimed a value for this graph family; a 2026 note showed the
> claim was false and left the problem open. I determined it completely — and
> two more cases besides."

## The thirty-second answer

> "Zero forcing is a colouring game on a graph, and the number of starting
> vertices you need bounds how degenerate a matrix on that graph can be. I found
> that every matrix on these graphs collapses to a single recurrence whose order
> is exactly the best known upper bound — so the matrix method either solves the
> problem outright or can't touch it. It solves it. I then built the matrices out
> of interchangeable tiles, which is what got it from 'some n' to 'all n'."

## Why this problem

Not self-defined. Rashidi et al. (2020) published Z(P(n,3)) = 8 for n ≥ 12;
Krishnan (July 2026) showed Z(P(12,3)) = 7, so the published theorem is false,
and left two things open: the stabilization threshold, and any rigorous lower
bound for k ≥ 4. I settled the threshold (it is 13) and gave exact values for
k = 4.

---

## Questions to expect

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
interval proof. And one script re-derives all 69 computational claims from
scratch; it currently passes 69 of 69. Also — twice a numerical search returned
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

**"What would you do next?"**
Close k = 4 — four values remain. Then k = 5, which is compute rather than new
mathematics. The genuinely open question is whether M < Z strictly at P(10,2);
that would be the first strict gap in this family.

---

## Traps to avoid

- **Do not say "we prove Krishnan's conjecture"** unless the note's text is
  checked. What is certain and citable: the note records the stabilization
  threshold as open, and this determines it.
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
> 3. Separate $M$ from $Z$ somewhere. I expect $M(P(10,2)) < Z(P(10,2)) = 6$ but
>    have no proof, and no $(n,k)$ is proved to have $M < 2k+2$.
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
