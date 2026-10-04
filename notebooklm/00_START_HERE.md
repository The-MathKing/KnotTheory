# START HERE — how to use this notebook

## What this project proved, in one paragraph

Every finite graph carries an **Ihara zeta function**, with an Euler product, a
functional equation, and a prime number theorem counting closed paths. So every
graph has a **Riemann Hypothesis** — and unlike the classical one, it is
decidable: by the Ihara determinant formula a cubic graph satisfies it exactly
when it is **Ramanujan**, every eigenvalue of modulus other than 3 having
modulus at most 2√2. Part I of this project asks which generalized Petersen
graphs P(n,k) satisfy it, a question whose ingredients have been on the shelf
since the spectrum of P(n,k) was determined in 2011 but which appears never to
have been put. Substituting the threshold into the characteristic polynomial and
squaring twice — each squaring an equivalence, since both sides are provably
positive — clears both radicals and leaves the nonnegativity of one integer
polynomial D_k of degree 2k+2 on the grid cos(2πj/n). Three exact evaluations
then settle the structure: D_k(1) = −7 forbids a band where the grid
accumulates, so **only finitely many n qualify for each k**, with an explicit
certified bound; and D_k(−1) is −7 for odd k but +9 for even k, while an even n
lands exactly on an exempt trivial eigenvalue, giving a **parity law** in which
bipartiteness helps. Then two further steps close it completely: D_k factors over Q(√2) and both
factors collapse to one quadratic form **Q = 4x²+4y²−8√2|xy|+3 ≥ 0 that does not
mention k**, so the forbidden set is one fixed region (four corner pieces, 0.43%
of the square) for every k; and since failure is a *simultaneous Diophantine*
condition, Dirichlet's approximation theorem forces it for every k once n ≥ 231.
The family is therefore finite in **both** variables, and exhausting what
remains gives the classification outright: exactly **460** pairs (n,k), **324**
graphs up to isomorphism, from 13,110 cases in exact arithmetic — largest
n = 112, and nothing at all past k = 45.

Part II uses the same cyclic-cover decomposition on a different question: over
**every** matrix carrying the graph's pattern, how degenerate can the zero
eigenvalue be? Eliminating the inner coordinates collapses any such matrix to a
single linear recurrence of order 2k+2, so the whole matrix-certificate method
has a hard ceiling of 2k+2 — which is exactly the best known upper bound on the
zero forcing number Z. Reaching that ceiling with tiles determines
Z(P(n,k)) = M(P(n,k)) for **every** n at k = 2, 3, 4, proving Conjecture 5 of a
July 2026 correction note and fixing at 13 the threshold it leaves open. (Note
on priority: exact values for k ≥ 4 were **not** previously unknown — Rashidi et
al. give Z(P(2k+1,k)) = 6 for k ≥ 5. What is new is the first n at which the
bound 2k+2 is *attained*, and the first results holding for infinitely many n.)

## What is in this folder

Read in order. Each file assumes only the ones before it.

| File | What it covers | Depends on |
|---|---|---|
| `01_prerequisites.md` | numbers, modular arithmetic, complex numbers, polynomials | nothing |
| `02_linear_algebra.md` | rank, nullity, eigenvalues, symmetric matrices, Schur complements | 01 |
| `03_graph_theory.md` | graphs, cubic graphs, P(n,k), I(n,j,k), DP(n,k), gcd structure | 01 |
| `04_zero_forcing.md` | the colour change rule, closure, Z(G), forts | 03 |
| `05_minimum_rank_and_M_le_Z.md` | S(G), maximum nullity, and the inequality M ≤ Z | 02, 04 |
| `06_rotation_bootstrap.md` | how the upper bounds are proved | 04 |
| `07_circulants_and_fourier.md` | circulant matrices and why symmetry block-diagonalises them | 02 |
| `08_chebyshev_and_the_symbol.md` | the polynomials L_k and the three-parameter symbol | 07 |
| `09_transfer_matrices_and_monodromy.md` | the reduction theorem and the ceiling | 02, 05 |
| `10_cyclotomic_and_galois.md` | minimal polynomials of 2cos(2π/d) and Galois orbits | 01, 08 |
| `11_main_results.md` | every theorem, with proofs, in dependency order | 05–10 |
| `12_computational_methods.md` | the engines, exact arithmetic, verification protocol | 11 |
| `13_what_failed_and_why.md` | dead ends, refuted conjectures, self-corrections | 11 |
| `14_worked_examples.md` | P(24,5) and P(60,4) fully by hand | 08, 10 |
| `15_glossary_and_notation.md` | every symbol and term | — |
| `16_open_questions.md` | what is genuinely still open, and why | 11 |
| `17_anticipated_questions.md` | hard questions a judge or referee would ask, with answers | 11 |
| `18_isef_context.md` | competition landscape and requirements | — |
| `23_antipodal_obstruction.md` | exactly when a certificate exists; the signed adjacency matrix; $k=3,7$ | 08, 10, 11 |
| `24_general_n.md` | escaping the congruence classes; certified primes; all $n\ge22$ for $k=3$ | 09, 23 |
| `25_riemann_hypothesis.md` | **Part I**: Ihara zeta, the RH for graphs, the criterion, finiteness, the parity law, the classification | 03, 07, 08, 10 |

Four PDFs are also included:

| File | What it is |
|---|---|
| `19_research_paper.pdf` | the research paper itself (31 pp) — the primary document |
| `20_research_log.pdf` | the dated research log (21 pp), including every dead end |
| `21_foundations_guide.pdf` | a foundations guide (14 pp) built from high-school level |
| `22_abandoned_investigation.pdf` | the log of an abandoned target (4 pp); read it for how a project gets killed |

The markdown files are self-contained — you can learn the whole thing from them
alone. The PDFs are the primary documents those files describe, and are worth
uploading so NotebookLM can quote them directly.

## How to drive NotebookLM with this

Good prompts, roughly in order of increasing difficulty:

- "Explain the colour change rule as if I have never seen a graph before, then
  give me three examples worked step by step."
- "Why is M(G) ≤ Z(G) true? Walk through the proof line by line and tell me
  exactly where each hypothesis is used."
- "I do not understand why t = L_k(s) exactly. Derive it."
- "Explain why the symbol polynomial has only three free parameters even though
  it has degree k+1. What goes wrong if I try to prescribe four roots?"
- "What is a monodromy, concretely, for someone who knows matrices but not
  differential equations?"
- "Why does a rational symbol polynomial force its remaining roots onto the
  grid? Explain the Galois argument without assuming Galois theory."
- "Quiz me on the difference between Z(G), M(G), and M_cs(G)."
- "What is the weakest step in the main argument, and what would break it?"
- "Give me the P(24,5) certificate and check it with me by hand."

## The one honest caveat

The main results settle k = 4 and k = 5 only for n in specific congruence
classes; the k >= 6 values are numerically certified rather than verified in
exact arithmetic, a genuinely weaker standard; and every result is at specific
n rather than all n. Anyone
who tells you the problem is solved has misread it. `16_open_questions.md` is precise about what remains.
