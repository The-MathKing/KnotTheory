# START HERE — how to use this notebook

## What this project proved, in one paragraph

There is a graph family called the generalized Petersen graphs, written P(n,k).
There is a number attached to every graph called its **zero forcing number**,
written Z(G), which measures how few vertices you must colour in at the start so
that a simple spreading rule eventually colours the whole graph. For P(n,k),
exact values of Z were known only for k = 2 and k = 3, and a correction note
published in July 2026 explicitly recorded that a rigorous lower bound for
k ≥ 4 was an open problem. This project (a) proves a structural theorem saying
that *every* matrix carrying the graph's pattern collapses to a single linear
recurrence of order 2k+2, so the entire matrix-certificate method has a hard
ceiling of 2k+2 — which is exactly the best known upper bound — and (b) reaches
that ceiling, giving the first exact values for k ≥ 4:
Z(P(n,4)) = 10 for every n divisible by 60, 70 or 90, and Z(P(n,5)) = 12 for
every n divisible by 24; and, by relaxing the
rotational symmetry to period ceil(k/2), Z(P(60,6)) = Z(P(72,6)) = 14,
Z(P(96,7)) = 16 and Z(P(96,8)) = 18 — the first values for k >= 6, so the
ceiling is attained for every k from 2 to 8. The certificates are integer matrices whose nullity a
computer verifies in exact arithmetic, so they are proofs rather than numerical
observations.

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

Four PDFs are also included:

| File | What it is |
|---|---|
| `19_research_paper.pdf` | the research paper itself (23 pp) — the primary document |
| `20_research_log.pdf` | the dated research log (18 pp), including every dead end |
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
