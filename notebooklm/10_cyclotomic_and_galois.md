# 10 — Cyclotomic polynomials, Galois orbits, and the mechanism

This file explains the idea that makes the main result work: **a polynomial
with rational coefficients cannot have "only some" of a conjugate family as
roots.** Get one, get them all — for free.

## 1. Algebraic numbers and minimal polynomials

A real or complex number r is **algebraic** if it is a root of some nonzero
polynomial with rational coefficients. Among all such polynomials there is a
unique monic one of smallest degree: the **minimal polynomial** of r, written
min_r. Two standard facts:

- min_r is **irreducible** over Q (it does not factor into smaller rational
  polynomials).
- If **any** rational polynomial F has r as a root, then min_r **divides** F.

The second fact is the whole engine. It means you cannot include r as a root of
a rational polynomial without also including *every* root of min_r. Those other
roots are the **Galois conjugates** of r.

Example: √2 has minimal polynomial s² − 2, whose roots are √2 and −√2. Any
rational polynomial with √2 as a root automatically has −√2 as a root too. You
cannot have one without the other.

## 2. Cyclotomic polynomials

The **d-th cyclotomic polynomial** Φ_d is the minimal polynomial of a primitive
d-th root of unity. Its roots are exactly the φ(d) primitive d-th roots of
unity, and it has integer coefficients. Examples:

    Φ_1 = x − 1,  Φ_2 = x + 1,  Φ_3 = x² + x + 1,  Φ_4 = x² + 1,
    Φ_5 = x⁴ + x³ + x² + x + 1,  Φ_6 = x² − x + 1.

## 3. The real subfield: minimal polynomials of 2cos(2π/d)

Our grid values are real: s = 2cos(2π m/n) = ζ + ζ⁻¹ for ζ a root of unity. So
we want the minimal polynomial of 2cos(2π/d). Call it **Ψ_d**.

Since ζ and ζ⁻¹ both map to the same s, passing from ζ to ζ + ζ⁻¹ halves the
degree:

    **deg Ψ_d = φ(d)/2**   for d ≥ 3,

and by convention Ψ_1 = s − 2 (root s = 2) and Ψ_2 = s + 2 (root s = −2), each
of degree 1.

The roots of Ψ_d are exactly the **primitive** values 2cos(2πj/d) with
gcd(j,d) = 1.

A concrete way to compute it: Φ_d is palindromic of degree φ(d) = 2g, so
Φ_d(x)/x^g can be written in terms of x^j + x^(−j) = L_j(s), giving Ψ_d
directly. Some values:

    Ψ_3 = s + 1              (root −1)
    Ψ_4 = s                  (root 0)
    Ψ_5 = s² + s − 1
    Ψ_6 = s − 1              (root 1)
    Ψ_10 = s² − s − 1        (roots the golden ratio and its conjugate)
    Ψ_14 = s³ − s² − 2s + 1
    Ψ_18 = s³ − 3s − 1
    Ψ_24 = s⁴ − 4s² + 1
    Ψ_30 = s⁴ + s³ − 4s² − 4s + 1

## 4. The mechanism, stated plainly

**Every root of Ψ_d lies in Γ_n as soon as d divides n.**

Why: the roots of Ψ_d are 2cos(2πj/d) with gcd(j,d) = 1. If d | n, write
n = d·q; then 2cos(2πj/d) = 2cos(2π(jq)/n), which is the grid value at index
m = jq. So it is in Γ_n.

Now combine with §1. Suppose the symbol F has **rational coefficients** and one
of its roots happens to be a grid value of "type d". Then Ψ_d divides F, so
**all** φ(d)/2 roots of Ψ_d are roots of F — and all of them are grid values
too. You paid for one root and received an entire orbit.

That is how a polynomial with only three free parameters can have all k+1 of
its roots on the grid: you do not place them one at a time.

## 5. The construction

> **Theorem (cyclotomic certificates).** Choose a set D of distinct positive
> integers with Σ (d ∈ D) deg Ψ_d = k + 1, and set F = Π (d ∈ D) Ψ_d.
> Write G = F − s·L_k, let a be the coefficient of s^k in G, and suppose
> G − a·L_k has degree ≤ 1, say = α s + β. Put e = 1, d = α, c² = aα − β, and
> suppose c² > 0. Then for every n divisible by lcm(D) with 2k < n, the matrix
>
>     A = [ a I + P + P⁻¹        c I          ]
>         [    c I          α I + P^k + P^(−k) ]
>
> lies in S(P(n,k)) and has nullity
> 2·Σ(d ∈ D, d ≥ 3) deg Ψ_d + #{d ∈ D : d ≤ 2}. If every d ≥ 3 this is exactly
> **2k+2**, and therefore **Z(P(n,k)) = M(P(n,k)) = 2k+2**.

**Proof.** By construction F = (s + a)L_k + αs + β as an identity in Z[s], so F
is the symbol of A (file 08). c² > 0 makes c real and nonzero, so A really lies
in S(P(n,k)). Every d ∈ D divides n, so all k+1 roots of F lie in Γ_n; they are
distinct because the Ψ_d are distinct irreducible polynomials. Counting
multiplicities as in file 07 (interior roots twice, endpoints once) gives the
nullity. Combine with M ≤ Z and the bootstrap bound Z ≤ 2k+2. ∎

Note the three conditions doing the work: **degree matches k+1**, **membership
in the three-parameter family** (that is k−2 integer linear conditions), and
**c² > 0**.

## 6. The results it produces

All of these certificates have a, α, c ∈ Z, so each is an **integer matrix**
and its nullity is confirmed by exact rational Gaussian elimination.

| k | D | lcm | F | a | d | c² | nullity |
|---|---|---|---|---|---|---|---|
| 2 | {3,10} | 30 | s·L_2 − 1 | 0 | 0 | 1 | 6 = 2k+2 |
| 2 | {14} | 14 | Ψ_14 | −1 | 0 | 1 | 6 = 2k+2 |
| 3 | {1,4,5} | 20 | Ψ_1Ψ_4Ψ_5 | −1 | −1 | 1 | 7 |
| 4 | {4,30} | 60 | Ψ_4Ψ_30 | 1 | −1 | 1 | 10 = 2k+2 |
| 4 | {5,14} | 70 | Ψ_5Ψ_14 | 0 | 1 | 1 | 10 = 2k+2 |
| 4 | {5,18} | 90 | Ψ_5Ψ_18 | 1 | 0 | 1 | 10 = 2k+2 |
| 5 | {3,6,24} | 24 | s·L_5 − 1 | 0 | 0 | 1 | 12 = 2k+2 |

So **Z(P(n,4)) = 10 for every n divisible by 60, 70 or 90**, and
**Z(P(n,5)) = 12 for every n divisible by 24**. These are the first exact
values of Z(P(n,k)) for k ≥ 4.

## 7. The adjacency-matrix special case

For k = 2 and k = 5 the parameters are a = d = 0 and c = 1 — that is, **the
certificate is the plain adjacency matrix** of P(n,k). The symbol is
s·L_k(s) − 1, and the factorisations are

    s L_2 − 1 = (s + 1)(s² − s − 1) = Ψ_3 Ψ_10
    s L_5 − 1 = (s − 1)(s + 1)(s⁴ − 4s² + 1) = Ψ_6 Ψ_3 Ψ_24

Since det M_m = s_m t_m − 1, the statement is equivalently

    nullity( Adj P(n,k) ) = #{ m : 2cos(2π(k+1)m/n) + 2cos(2π(k−1)m/n) = 1 },

a **rational linear relation among cosines of rational angles** — the subject of
the Conway–Jones theorem. Which k admit solutions at all is therefore a
question of that type; in the computed range k ≤ 10 only k = 2, 5, 8 do.

It is worth sitting with the fact that the simplest matrix in the entire class
was sufficient, after a great deal of effort on elaborate ones.

## 8. Rational is sufficient, not necessary

F only needs **real** coefficients and roots in Γ_n; it does not need to be
rational. Irrational symbols exist and are sometimes better. For k = 3 **no**
rational symbol attains 8, but irrational ones do, at n = 40, 60, 80, 120 —
for instance a = −√2, d = 0, c² = 1 at n = 40, and c² = 1/φ (φ the golden
ratio) at n = 60.

Those certificates are verified exactly by working in the number field Q(ζ_n):
represent 2cos(2πm/n) as x^m + x^(n−m) modulo Φ_n(x), so the membership
identity, the reality of a, α, β, c², and c² ≠ 0 are all decided by exact
integer arithmetic rather than floating point.

## 9. The search over rational symbols is complete

This is worth stating carefully because it is a theorem, not a search limit.

Attaining 2k+2 forces F to be squarefree with all k+1 roots interior and on the
grid. If F is rational it is a product of distinct Ψ_d with Σ deg Ψ_d = k+1.
Then **every** factor satisfies deg Ψ_d ≤ k+1, i.e. φ(d) ≤ 2k+2 — and since
φ(d) → ∞, only finitely many d qualify and they can all be listed. So for each
k the enumeration is finite and complete. Carrying it out:

| k | 2k+2 | candidates | admissible | verdict |
|---|---|---|---|---|
| 2 | 6 | 17 | 5 | attained |
| 3 | 8 | 35 | 0 | impossible for rational symbols |
| 4 | 10 | 67 | 3 | attained |
| 5 | 12 | 127 | 1 | attained |
| 6 | 14 | 225 | 0 | impossible for rational symbols |
| 7 | 16 | 385 | 0 | impossible for rational symbols |
| 8 | 18 | 651 | 0 | impossible for rational symbols |
| 9 | 20 | 1065 | 0 | impossible for rational symbols |

**How the failures split matters.** At k = 7, 378 of the 385 candidates fail
because F is **not in the three-parameter family**, and only 7 fail because
c² ≤ 0. So the binding constraint is the k−2 linear membership conditions
imposed on a 3-dimensional family, and it tightens as k grows. That diagnosis
points directly at the fix: enlarge the family by using period-d symbols, which
carry 5d − 1 free ratios instead of 3 (file 16).

## 10. What to take away

- A rational polynomial that has one root of a conjugate family has them all.
- Ψ_d = minimal polynomial of 2cos(2π/d), degree φ(d)/2; its roots are grid
  values whenever d | n.
- Build F as a product of distinct Ψ_d with total degree k+1, check membership
  and c² > 0 — then the nullity is 2k+2 for every n divisible by lcm(D).
- For k = 2 and k = 5 the certificate is literally the adjacency matrix.
- The rational search is finite and complete; k = 3, 6, 7, 8, 9 are impossible
  over the rationals, and the failure is a shortage of *parameters*, not of
  realisability.
