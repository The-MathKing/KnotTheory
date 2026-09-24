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
