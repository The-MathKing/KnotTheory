# 11 — Every result, in dependency order

A single reference list of what is proved, what it rests on, and what it does
not say. Proofs are in files 05, 06, 09, 10; this file is the map.

## A. Foundational (not original to this project)

**A1. M(G) ≤ Z(G).** For any graph, the maximum nullity over matrices carrying
its pattern is at most the zero forcing number. Proof in file 05. Extends
verbatim to combinatorially symmetric (non-symmetric) matrices, giving
M(G) ≤ M_cs(G) ≤ Z(G).

**A2. Fort duality.** S is zero forcing iff it meets every fort. File 04.

**A3. Known values.** Z(P(n,2)) = 6 for n ≥ 10 (2020). Z(P(n,3)) = 8 for
n ≥ 13 (2026 correction note; the 2020 claim for n ≥ 12 is false, since
Z(P(12,3)) = 7). The same note records a rigorous lower bound for k ≥ 4 as
**open** — this is the target.

## B. Upper bounds by the rotation bootstrap

**B1. Bootstrap Lemma.** If ρ is an automorphism of a finite graph and
ρ(S) ⊆ cl(S), then cl(S) is ρ-invariant. File 06.

**B2. Closing Lemma.** In a cubic graph split as O ⊔ I with one spoke per
vertex, O ⊆ cl(S) implies cl(S) = V. File 06.

**B3. I-graph bound.** Z(I(n,j,k)) ≤ 2(j+k) for n ≥ 2(j+k)+1.
*Scope:* genuinely new only when gcd(n,j) > 1, since otherwise
I(n,j,k) ≅ P(n, j⁻¹k).

**B4. Corollary.** **Z(P(n,k)) ≤ 2k+2** for n ≥ 2k+3, witnessed by the 2k+2
consecutive outer vertices u_0, ..., u_(2k+1).

**B5. DP bound.** Z(DP(n,k)) ≤ 4k+4 for n ≥ 2k+3. No zero forcing results for
this family existed previously. Sharp at k = 1 and k = 2.

## C. The structural theorem (the core contribution)

**C1. Reduction Theorem.** For 2k < n and **any** matrix A whose off-diagonal
support is exactly E(P(n,k)) — symmetric or not — eliminating the inner
coordinates yields one scalar linear recurrence supported on nine indices, of
order exactly 2k+2, and

    nullity(A) = dim ker(T − I) ≤ 2k+2,

where T is the monodromy, with equality **iff T = I**. File 09.

**C2. Determinant formula.** det T = (Π b')(Π e') / ((Π b)(Π e)), equal to 1
whenever A is symmetric.

**C3. Ceiling Corollary.** M(P(n,k)) ≤ M_cs(P(n,k)) ≤ 2k+2. The inequality is
not new (it follows from A1 and B4), but the **identification is exact**: the
order of the recurrence equals the size of the bootstrap's forcing set, so the
ceiling of the matrix-certificate method coincides with the upper bound it is
trying to match. Either the method settles Z completely, or nothing does.

**C4. Product form.** For symmetric A, nullity(A) = dim ker(SU − I), the
multiplicity of eigenvalue 1 in a product of two symmetric cycle matrices.

*Verification:* 189 random matrices over 63 pairs (n,k) for C1; 60 more over 30
pairs, in both matrix classes, for C2, C4 and the forcing-set statement.

## D. The symbol, and the correction

**D1. Symbol Proposition.** For rotation-invariant A,
nullity(A) = #{m : F(s_m) = 0} where **F(s) = (s + a)L_k(s) + αs + β**, monic
of degree k+1 with exactly **three** free parameters, for every k. Interior
roots count twice, endpoints ±2 count once. Admissible iff c² = aα − β > 0.
File 08.

**D2. Correction to an earlier claim of ours.** The project previously asserted
that this construction "never exceeds 6 for every k ≥ 2". The premise (only
three roots can be prescribed) is correct; the inference is not, because
prescribing three roots determines the remaining k−2, which can land on the
grid by themselves. Period-one certificates in fact reach 2k+2 for k = 2, 3, 4,
5. The elaborate period-two machinery built to escape the nonexistent cap was
unnecessary, and the values it gave (8 for P(n,4), 10 for P(24,6)) are
superseded.

## E. The main results

**E1. Cyclotomic Certificates.** Let D be a set of distinct integers with
Σ deg Ψ_d = k+1 and F = Π Ψ_d. If F lies in the three-parameter family and
c² > 0, then for every n divisible by lcm(D) with 2k < n the resulting matrix
lies in S(P(n,k)) with nullity 2k+2 (when all d ≥ 3), so

    **Z(P(n,k)) = M(P(n,k)) = 2k+2.**

File 10.

**E2. The exact values.**

| statement | for | how certified |
|---|---|---|
| **Z(P(n,4)) = M(P(n,4)) = 10** | every n divisible by 60, 70 or 90 | integer matrix, exact rational rank |
| **Z(P(n,5)) = M(P(n,5)) = 12** | every n divisible by 24 | integer matrix (the adjacency matrix), exact rational rank |
| Z(P(n,3)) = 8 | n = 40, 60, 80, 120 | irrational certificate, verified in Q(ζ_n) |
| Z(P(n,2)) = 6 | 9 ≤ n ≤ 130, n ≠ 10 | verified in Q(ζ_n) |

The k = 4 and k = 5 lines are **the first exact values of Z(P(n,k)) for k ≥ 4**,
the range the 2026 note records as open. The k = 3 line is a *matrix* proof of
values obtained combinatorially elsewhere.

**E3. The adjacency-matrix corollary.**

    nullity( Adj P(n,k) ) = #{m ∈ Z_n : 2cos(2π(k+1)m/n) + 2cos(2π(k−1)m/n) = 1},

a rational linear relation among cosines of rational angles (Conway–Jones type).
For k = 5 the count is 12 = 2k+2 whenever 24 | n.

**E4. Completeness of the rational search.** For each k the enumeration of
rational symbols attaining 2k+2 is **finite and complete**, because
deg Ψ_d ≤ k+1 forces φ(d) ≤ 2k+2. Result: attained for k = 2, 4, 5; impossible
for k = 3, 6, 7, 8, 9. At k = 7, 378 of 385 candidates fail *membership in the
three-parameter family* and only 7 fail realisability — so the binding
constraint is a shortage of parameters, and it tightens with k.

## E5. Period-d certificates, and the first k = 6 values

**E5a. The rank law (observation, not a theorem).** For a period-`d` matrix
(weights repeating with period `d | n`), write `G` for the degree-`(k+1)`
symbol obtained from `det M_ℓ`. The map (weights) → (monic coefficients of `G`)
has

    rank = min(2d + 1, k + 1)

in every case computed, for `3 ≤ k ≤ 13` and `1 ≤ d ≤ 7`. At `d = 1` this
returns 3, exactly the three free parameters of the period-1 symbol — a check
that was not built in.

Most of the `5d` weights are **gauge**: conjugating by a positive diagonal
matrix preserves both the pattern and the nullity, so counting weights counts
nothing. The consequence is that every symbol becomes locally reachable
precisely when

    2d + 1 ≥ k + 1     ⟺     d ≥ ⌈k/2⌉,

**not** `d ≥ (k+2)/5` as a naive weight count suggests. (An earlier version of
this project asserted the naive count; it is corrected.) The underlying
assumption — that `det M(ζ)` really is a degree-`(k+1)` polynomial in
`σ = ζ + 1/ζ` — was checked separately by fitting to degree `k+4` and confirming
the surplus coefficients vanish to ~10⁻¹⁵.

**E5b. Prescribing the symbol.** For `d ≥ ⌈k/2⌉` the map is a submersion, so
instead of searching for a certificate one can prescribe one: choose `k+1`
interior values of `Γ_m` (`m = n/d`), form the monic `G*` with those roots, and
solve `G(w) = G*`. That is `k+1` equations in `5d` unknowns with full-rank
Jacobian, so the solution set is a manifold of dimension `5d − (k+1)`.

Two independent conditions must hold: `m ≥ 2k+4`, so `Γ_m` contains `k+1`
distinct *interior* values at all; and `d ≥ ⌈k/2⌉`, so the symbol is reachable.
For `k=6` these force `d ≥ 3` and `n ≥ 48`.

**E5c. The degeneracy.** Solving without further constraint reliably returns a
point where one spoke weight has collapsed to zero. That is a genuine solution
— with a spoke gone the matrix block-diagonalises and `G` factors as
`det(U_ℓ)·det(V_ℓ)` — but the matrix carries the pattern of a *different graph*
and certifies nothing. At those points the Jacobian rank drops from 7 to 6:
they are **singular points**, which is why random restarts return to them.
Neither a realisability barrier nor continuation escapes (continuation loses
the symbol at the first step, `τ = 0.02`).

What escapes is slack in the choice of roots. `Γ_16` (n=48) has exactly 7
interior values for the 7 needed — one root set, no freedom; `Γ_18` (n=54) has
8, and all 8 sets degenerate. `Γ_20` and `Γ_24` (n=60, 72) have 9 and 11,
giving 36 and 330 root sets — and there realisable points exist.

**E5d. Theorem.**

    Z(P(60,6)) = Z(P(72,6)) = 14      (period 3)
    Z(P(96,7))              = 16      (period 4)
    Z(P(96,8))              = 18      (period 4)

The first exact values for `k ≥ 6`. In every case the period used is the one
the rank law prescribes, `d = ⌈k/2⌉` — and the law *predicted* this before the
runs: `d=3` carried `k=6` and failed for `k=7,8`, where `d=4` succeeded. A law
measured on one set of cases going on to predict which experiments would work
is the main reason to believe it rather than merely report it.

A sweep over `n` for `k=6` finds certificates at `n = 60, 72, 84`, the last two
on the first or second root set tried — so this is not two lucky values of `n`.
Once the counting conditions hold with a little slack, certificates appear
readily. Verified on the **full 2n × 2n matrix**,
independently of the Fourier blocks used to find them: for `n=60` with roots at
`ℓ ∈ {2,3,4,5,6,8,9}`, fourteen eigenvalues below `4×10⁻¹⁵` and the fifteenth
at `5.1×10⁻²` — thirteen orders of separation — with every vertex carrying
exactly three off-diagonal nonzeros and the smallest required entry at 0.188 of
the matrix scale. Several further root sets at each `n` give independent
certificates, so this is a region, not an isolated point.

**Status caveat.** Unlike the `k=4,5` certificates, which are integer matrices
checked by exact rational elimination, these come from a Newton solve and their
weights are algebraic numbers of no recognised form. They are **numerically
certified, not yet verified in exact arithmetic**, and should not be described
at the same standard. The route I expected to close that gap — choosing the root set as a union of
full Galois orbits, making `G*` rational — is **closed**: all eight
Galois-closed sets at `n=72` hit the symbol to `10⁻¹⁵` with nullity 14, and all
eight collapse a weight, whether or not `σ=0` is among the roots. Rationality
and realisability are in tension here, and the reason is not understood. The
remaining route is interval Newton, which the ceiling theorem makes tractable:
certifying the *equation* `G(w) = G*` exactly gives the nullity as a discrete
consequence (`k+1` grid roots ⟹ `2k+2` singular blocks ⟹ nullity ≥ `2k+2`,
with the ceiling forcing equality).

## F. Negative results (why other routes fail)

**F1.** Disjoint fort packing: at most two disjoint forts exist in any case
tested; the certificate cannot exist at those sizes.

**F2.** The fort LP: integrality gap ≈ 2 (LP = 3.21 against Z = 10 for
P(18,4)), widening with k. This also explains why fort-based exact solvers
converge slowly on this family.

**F3.** Hoffman-type spectral bound: gives 1.2–2.9 against true Z of 6–12.

All three are insufficient **in principle**, not merely in practice.

## G. Refuted conjectures (ours)

**G1.** "n_0(k) = 5k − 2 is a single stabilization threshold." Fits k = 3, 4, 5
and correctly predicted that n = 28 would be the first n with Z(P(n,6)) = 14 —
a prediction recorded before the 14.2-hour computation finished, and borne out.
But **Z(P(29,6)) = 12**, and 29 > 28, so 28 is not a stabilization point and the
single-threshold form is false. The explanation is gcd(n,k): each gcd class
climbs on its own schedule.

**G2.** "Z ≤ 2(gcd(n,j) + gcd(n,k))." Refuted by Z(P(11,3)) = 7 > 4, using data
already in the validation table. The conjecture had been generalised from 20
graphs all selected for gcd > 1, without testing the excluded boundary.

**G3.** "Period-one certificates never exceed 6." See D2.

## H. What is NOT claimed

- Not claimed: Z(P(n,k)) = 2k+2 for all large n. Only for the stated residue
  classes.
- Not claimed: anything for k ≥ 7.
- Not claimed at the exact-arithmetic standard: the k = 6 values (see E5d).
- Not claimed: that M(P(n,k)) < 2k+2 for the remaining n. Extensive search
  plateaus well above machine precision, but no proof exists and no single
  (n,k) is proved to have M < 2k+2.
- Not claimed: that the period-one construction is the best possible. Higher
  period is unexplored.


## Realisability, exactly (newest results)

Full treatment in `23_antipodal_obstruction.md`. In brief:

0. **The theorem.** $c^2 = 0 \iff F = (s+a)(L_k(s)+t)$. One line. Everything
   else is a corollary. Over $\mathbb{Q}$, Niven's theorem forces
   $a,t \in \{0,\pm1,\pm2\}$: at most 25 degenerate symbols per $k$.
0b. **Only $c^2=0$ is fatal**, since $c^2$ is the *product* of the two spoke
   weights. Requiring $c^2>0$ (symmetric) where $c^2\neq0$ suffices had made
   $k=3$ and $k=7$ look impossible. They are not.
0c. **$Z(P(n,3)) = 8$ for $10 \mid n$ and $Z(P(n,7)) = 16$ for $120 \mid n$**,
   by the adjacency matrix with one spoke set negated. Its nullity is classified
   by $Q_k(z) = z^{2k+2}+z^{2k}+z^{k+1}+z^2+1$, which splits into cyclotomics
   only for $k=2,3,7$ in $2\le k\le 60$. The unsigned $P_k$ splits only at
   $k=2,5$, so the two signs cover $k\in\{2,3,5,7\}$.
0d. **$k=6,8,9,10$ are impossible over $\mathbb{Q}$ in both classes**, and now
   for an identified reason rather than an empty search.
1. **Closed form at $k=2$.** $c^2 = -(s_1+s_2)(s_1+s_3)(s_2+s_3)$, so the
   construction fails exactly when two prescribed roots are antipodal.
2. **Parity theorem, all even $k$.** Since $L_k(-s) = (-1)^k L_k(s)$, an
   antipodal pair of roots forces $c^2 = 0$ identically for every even $k$.
   For odd $k$, $c^2 = L_k(y)(y^2-a^2)/y$ and there is no obstruction.
3. **$k=2$ settled completely.** $Z(P(n,2)) = M(P(n,2)) = 6$ for all
   $n \ge 9$ with $n \ne 10$, by an explicit certificate at the three most
   negative grid values. Plus $Z = M_{cs} = 6$ for $7 \mid n$ by an integer
   non-symmetric certificate. The exceptions: $Z(P(5,2))=5$, $Z(P(6,2))=4$,
   $Z(P(8,2))=5$, $Z(P(10,2))=6$.
4. **The non-symmetric class is necessary at $n=7$** — the only case in the
   project where it is.
5. **Corollary for even $k$:** the cyclotomic factor set may not contain both
   $d$ and $2d$ for odd $d$, nor any $d$ with $4 \mid d$ and
   $\varphi(d) \ge 4$. This accounts for every rejection in the $k=2$
   exhaustive enumeration.
