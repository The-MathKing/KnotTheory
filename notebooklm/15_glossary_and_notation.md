# 15 — Glossary and notation

## Symbols

| Symbol | Meaning |
|---|---|
| G | a graph; V vertices, E edges |
| N[u] | closed neighbourhood of u: u together with its neighbours |
| P(n,k) | generalized Petersen graph: outer cycle u_i—u_(i+1), inner edges v_i—v_(i+k), spokes u_i—v_i; 2n vertices, cubic |
| I(n,j,k) | I-graph: outer edges skip j, inner edges skip k; P(n,k) = I(n,1,k) |
| DP(n,k) | double generalized Petersen graph; 4n vertices |
| ρ | the rotation automorphism, i ↦ i+1 |
| cl(S) | closure of S under the colour change rule |
| Z(G) | zero forcing number: size of the smallest zero forcing set |
| S(G) | real **symmetric** matrices with G's off-diagonal pattern, free diagonal |
| M(G) | maximum nullity over S(G) |
| M_cs(G) | maximum nullity over combinatorially symmetric matrices (not necessarily symmetric) |
| mr(G) | minimum rank, equal to (number of vertices) − M(G) |
| P | the n×n cyclic shift matrix |
| ω | e^(2πi/n), a primitive n-th root of unity |
| s_m | 2cos(2πm/n) — the outer Fourier quantity |
| t_m | 2cos(2πkm/n) — the inner Fourier quantity |
| Γ_n | the grid {2cos(2πm/n) : m ∈ Z_n} ⊂ [−2, 2] |
| L_k | monic integer polynomial of degree k with L_k(z + 1/z) = z^k + z^(−k) |
| F(s) | the symbol, (s + a)L_k(s) + αs + β; monic of degree k+1 |
| a, d | diagonal entries (outer, inner) |
| b, c, e | edge weights (outer, spoke, inner) |
| α, β | d/e and (ad − c²)/e |
| φ(d) | Euler totient: count of 1..d coprime to d |
| Φ_d | d-th cyclotomic polynomial: minimal polynomial of a primitive d-th root of unity |
| Ψ_d | minimal polynomial of 2cos(2π/d); degree φ(d)/2 for d ≥ 3; Ψ_1 = s−2, Ψ_2 = s+2 |
| T | the monodromy matrix of the reduced recurrence, in GL(2k+2, R) |
| Q(ζ_n) | the cyclotomic number field, used for exact verification |

## Terms

**Colour change rule.** If a black vertex has *exactly one* white neighbour,
that neighbour becomes black.

**Zero forcing set.** A starting set whose closure is everything.

**Fort.** A nonempty set F such that every vertex outside F has 0 or ≥2
neighbours in F. S is zero forcing iff it meets every fort.

**Nullity.** dim ker A — the number of independent directions crushed to zero;
equivalently the geometric multiplicity of the eigenvalue 0.

**Carries the pattern of G / combinatorially symmetric.** A_(u,v) ≠ 0 exactly
when uv ∈ E, for u ≠ v; diagonal free. "Combinatorially symmetric" allows
A_(u,v) ≠ A_(v,u); symmetric does not.

**Certificate.** An explicit matrix with the graph's pattern and a known
nullity, proving a lower bound on Z by M ≤ Z.

**Circulant.** A matrix that is a polynomial in the shift P; equivalently one
that commutes with the rotation.

**Symbol.** The degree-(k+1) polynomial F(s) whose roots on Γ_n count the
nullity of a rotation-invariant certificate.

**Monodromy.** The matrix describing what one full trip around the cycle does
to the state vector of a recurrence. Kernel vectors correspond to its fixed
vectors.

**Admissible / realisable.** A candidate symbol whose recovered parameters give
a genuine real matrix with the right pattern — in practice, c² > 0.

**Galois conjugates.** The other roots of the minimal polynomial of an
algebraic number. A rational polynomial having one root of a family has them
all.

**Squarefree.** No repeated roots.

**Period-d construction.** Weights repeating with period d rather than being
constant; commutes with ρ^d, splits into n/d blocks of size 2d, and carries
5d − 1 free ratios instead of 3.

## Numbers worth memorising

| Quantity | Value |
|---|---|
| Upper bound for P(n,k) | 2k+2 |
| Order of the reduced recurrence | 2k+2 (the same number — not a coincidence) |
| Free parameters in the period-1 symbol | 3, for every k |
| Membership conditions on the symbol | k − 2 linear conditions |
| Free ratios in a period-d symbol | 5d − 1 |
| Z(P(n,2)) | 6 for n ≥ 10 (published 2020) |
| Z(P(n,3)) | 8 for n ≥ 13 (the 2020 claim for n ≥ 12 is false) |
| Z(P(12,3)) | 7 — the counterexample that forced the 2026 correction |
| Z(P(n,4)) | 10 whenever n is divisible by 60, 70 or 90 — **new** |
| Z(P(n,5)) | 12 whenever n is divisible by 24 — **new** |
| Z(P(29,6)) | 12, refuting our own single-threshold conjecture |
