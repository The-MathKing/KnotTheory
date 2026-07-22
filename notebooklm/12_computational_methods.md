# 12 — Computational methods and the verification protocol

Every number in this project came from code that was validated before it was
trusted. This file describes the tools and, more importantly, the discipline.

## 1. The exhaustive zero forcing solver

To get exact values of Z(P(n,k)) for small n, the solver searches all vertex
subsets. Three ideas make it fast enough:

- **Bitmask closure.** A vertex set is a 128-bit integer; the colour change rule
  becomes bit operations. Written in C with `__uint128_t`.
- **Symmetry reduction.** By the rotation, a minimum forcing set may be assumed
  to contain a fixed orbit representative — either u_0, or v_0 if the set
  contains no outer vertex. This divides the search by roughly n.
- **Threading.** pthreads over the outer loop, giving about a 14× speedup.

**Validation before use.** The solver reproduced *every* published value before
being used for anything new: the full table of Z(P(n,3)) for 7 ≤ n ≤ 20
including the corrected Z(P(12,3)) = 7 and the non-monotone values at n = 10,
11; Z(P(n,2)) = 6 for 10 ≤ n ≤ 16; and Z(P(2k+1,k)) = 6 for k = 5, 6, 7. It was
also cross-checked against an independent brute-force implementation and two
exact solver formulations (an ILP over forts and a CP-SAT model).

Cost grows brutally: the search is over C(2n−1, m−1) subsets. On this hardware
(j,k) = (2,3) takes minutes, (3,4) about ninety, (2,5) roughly a day, and (3,5)
some 10^4 years. Sharpness questions beyond small parameters are
**computationally out of reach**, not merely unfinished — a distinction worth
being precise about.

## 2. Certificate search: a two-stage design

Finding a matrix with high nullity is a continuous optimisation. The design
that worked:

**Stage 1 — cheap filter, many starts.** Minimise the sum of the squares of the
r smallest eigenvalues (or singular values, for non-symmetric A), subject to a
scale normalisation and a barrier keeping required-nonzero entries away from
zero. The gradients are analytic and cheap:

    d(λ²)/dw_j = 2λ · qᵀE_j q ,     d(σ²)/dw_j = 2σ · uᵀE_j v,

and each generator E_j has one or two nonzero entries, so every quadratic form
is O(1). One function evaluation is a single 2n × 2n eigendecomposition. That
makes hundreds of random starts affordable — necessary, because the question
being asked is whether a solution exists at all.

**Stage 2 — quadratic polish.** L-BFGS-B on the eigenvalue objective stalls
near 1e−8, because the objective is only piecewise smooth at eigenvalue
crossings. Switching to the bilinear system A(w)X = 0, XᵀX = I with an analytic
Jacobian converges to machine precision. So: filter cheaply, then polish the
best candidates.

This matters: with stage 1 alone, P(12,2) at r = 6 reports "none found" with a
best plateau of 5×10⁻⁹; after polishing, 1×10⁻¹⁶.

**Reading the plateau.** When no certificate exists, the plateau is *tight and
reproducible* across independent starts. At P(13,3) with r = 8, 200 starts
plateau around 4×10⁻³ — six orders of magnitude worse than a case that does
have a solution. That contrast is the evidence; a single failed run is not.

## 3. Exact arithmetic — three levels

Numerical nullity is not a proof. Three levels of rigour were used:

**Level 1 — integer matrices.** The cyclotomic certificates have a, α, c ∈ Z,
so A is an integer matrix. Its nullity is computed by exact Gaussian
elimination over the rationals (Python `Fraction`). No floating point anywhere.

**Level 2 — the number field Q(ζ_n).** Irrational certificates are verified by
representing 2cos(2πm/n) as x^m + x^(n−m) modulo the cyclotomic polynomial
Φ_n(x), and doing all arithmetic with rational coefficient vectors. In that
field one checks exactly: the membership identity F = (s+a)L_k + αs + β; that
a, α, β, c² are **real**, i.e. fixed by the automorphism x ↦ x^(n−1) (complex
conjugation); and that c² ≠ 0. The sign of the nonzero algebraic number c² is
then read off at high precision, which is decisive because the value is bounded
away from zero.

**Level 3 — closed-form counting.** For the adjacency-matrix family the nullity
is a count of solutions to 2cos(2π(k+1)m/n) + 2cos(2π(k−1)m/n) = 1, which can
be checked directly.

## 4. Two numerical traps, and what caught them

**Trap 1 — dense grid, loose tolerance.** Counting grid roots by |F(r)| < 10⁻⁸
reported nullity 7 for k = 2 at n = 126, 128, 130. That is impossible: the
ceiling is 2k+2 = 6. As Γ_n becomes dense, near-roots pass a fixed tolerance.

**Trap 2 — bad scaling.** A candidate at (n,k) = (48,7) had |a| enormous
against the edge weights 1. A nullity threshold relative to max|A| then
swallowed 48 eigenvalues.

**Trap 3 (earlier, same family) — a vanishing edge.** A period-two search once
reported nullity 7 for P(14,2), where Z = 6. The optimiser had driven a
required-nonzero edge weight to 3×10⁻⁴ against a matrix scale of 4.5,
numerically deleting that edge. The zero-pattern test passed, because the entry
was technically nonzero.

**All three were caught by an inequality that must hold** — Z ≥ M in the third
case, the ceiling nullity ≤ 2k+2 in the first two.

> **Working rule.** Wrap every numerical search inside a bound it cannot
> legally violate. That bound is the only thing that will tell you an answer is
> wrong when it looks right.

The fixes: test each Fourier block against **its own** scale rather than a
global one; impose a *relative* floor on required-nonzero entries; audit
certificates by block determinants (zero by construction) rather than by
thresholded eigenvalues; and certify in exact arithmetic where it matters.

## 5. A monotonicity guardrail

S(G) sits **inside** the combinatorially symmetric class. So a search over the
larger class can never legitimately return a smaller maximum than a search over
the smaller one.

That guardrail fired: an early run reported cs < sym on P(12,2), which is
impossible. The mathematics was fine; the search was weak. The fix was to seed
the larger search with the symmetric certificate (duplicating each edge weight
into its two directed entries), making the cs answer monotone by construction.

Uncomfortable detail worth keeping: a conclusion had **already been drawn** from
those numbers — that even 8n parameters could not reach 2k+2 at k = 3 — before
the check caught the fault. The conclusion may still be true, but the evidence
for it was worthless.

## 6. Reproducibility

Every claim has a script, and every script writes its output to a results file.
The key ones:

- `recurrence_order.py` — the structural theorem, checked on 249 matrices
- `cyclotomic_certificates.py` — the exact integer certificates
- `cyclotomic_exhaustive.py` — the completeness of the rational search
- `period1_optimum.py` — the exhaustive triple scan per (n,k)
- `exact_certifier.py` — verification in Q(ζ_n)
- `certified_lower_bounds.py` — the certified exact values
- `fast_nullity.py`, `monodromy_certificates.py`, `cs_certificates.py` — the
  general-weight searches
- `adjacency_nullity.py` — the closed-form count with exact rank cross-check

## 7. What to take away

- Validate an engine against every published value *before* using it.
- Two-stage optimisation: cheap many-start filter, then quadratic polish.
- A tight reproducible plateau across independent starts is evidence of
  non-existence; one failed run is not.
- Exact arithmetic (integers, or Q(ζ_n)) turns an observation into a proof.
- Wrap searches in a bound they cannot violate; it is your only alarm.
