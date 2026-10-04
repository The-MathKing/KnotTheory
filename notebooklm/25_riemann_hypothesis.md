# 25 — The Riemann Hypothesis for graphs, and the classification

Depends on: 03 (graphs, P(n,k)), 07 (circulants and Fourier), 08 (Chebyshev),
10 (cyclotomic and Galois). Nothing in this file needs zero forcing.

---

## 1. Why a graph has a Riemann Hypothesis at all

Attached to a finite connected graph X is its **Ihara zeta function**

    ζ_X(u) = ∏_[C] ( 1 − u^ℓ(C) )^(−1)

the product taken over equivalence classes of primitive, backtrackless,
tailless closed paths, with ℓ(C) the length. Read the analogy directly:

| Riemann ζ(s) | Ihara ζ_X(u) |
|---|---|
| product over primes p | product over primitive closed geodesics |
| meromorphic continuation | ζ_X(u)^(−1) is a polynomial, so ζ_X is rational |
| functional equation | yes, for regular graphs |
| prime number theorem | yes — counts closed geodesics by length |
| Riemann Hypothesis | poles of ζ_X(q^(−s)) on Re s = 1/2 |

For a (q+1)-regular graph the substitution u = q^(−s) makes the last row
meaningful, and one can ask the Riemann Hypothesis for the graph.

## 2. Why it is decidable — the key theorem

This is the pivot of the whole project.

> **Theorem (Ihara determinant formula; Terras, *Zeta Functions and Chaos*,
> Exercise 9).** A connected (q+1)-regular graph X satisfies the Riemann
> Hypothesis **if and only if** X is **Ramanujan**: every eigenvalue λ of the
> adjacency matrix with |λ| ≠ q+1 satisfies |λ| ≤ 2√q.

An analytic statement about poles becomes a finite statement about a 2n × 2n
matrix. Note carefully what is excluded: **only** the eigenvalues of modulus
exactly q+1. In a connected (q+1)-regular graph, +（q+1) has multiplicity 1
always, and −(q+1) occurs (with multiplicity 1) exactly when the graph is
bipartite. Those are the *trivial* eigenvalues.

The term "Ramanujan graph" is due to Lubotzky, Phillips and Sarnak. The bound
2√q is not arbitrary: it is the spectral radius of the adjacency operator on the
infinite (q+1)-regular tree, that is, the smallest second eigenvalue any
infinite family of (q+1)-regular graphs can have. So Ramanujan graphs are the
**optimal expanders**, which is why they matter for communication networks,
error-correcting codes and derandomization.

Our graphs are cubic: q + 1 = 3, q = 2, threshold **2√2 = 2.8284271247…**

## 3. The question

> For which n and k does P(n,k) satisfy the Riemann Hypothesis?

Three things to know about the status of this question:

- The **spectrum of P(n,k) has been completely known since 2011** (Gera and
  Stănică, *The spectrum of generalized Petersen graphs*).
- That paper contains **no occurrence** of the words *Ramanujan*, *expander* or
  *spectral gap*.
- The same classification **has** been carried out for other families — Droll
  for unitary Cayley graphs, Le and Sander for integral circulant graphs of
  prime power order — and in each case only finitely many members qualify.

So it is a question of a recognised kind, the ingredients were on the shelf, and
it was not put.

## 4. Step one: the spectrum is a symbol on a grid

This is exactly the decomposition of file 07, applied to P(n,k).

P(n,k) carries the rotation ρ : i ↦ i+1, so its adjacency matrix lies in the
commutant of a ℤ_n action and decomposes over the characters χ_j(a) = ζ_n^(ja)
into 2 × 2 blocks:

    M_j = [ α_j  1 ]      α_j = 2cos(2πj/n)
          [ 1  β_j ]      β_j = 2cos(2πjk/n) = 2 T_k(α_j/2)

with T_k the Chebyshev polynomial of the first kind (file 08). This is
Theorem 2.4 of Gera–Stănică.

**Two things worth saying out loud.** First, on the zeta side this decomposition
*is* the factorization of ζ_{P(n,k)} into **Artin–Ihara L-functions** over the
characters of ℤ_n — the same statement, read on the other side. Second, the
spectrum is therefore *one fixed curve, sampled at n points*, and the grid
{2πj/n} **refines** as n grows. That single fact will bound n.

## 5. Step two: clearing both radicals

The eigenvalues of M_j are ( A ± √((α−β)² + 4) ) / 2 with A = α+β, and they are
to be compared against 2√2. Two nested irrationalities, and the comparison is
decided at a band edge — precisely where floating point stops meaning anything.

Both radicals can be removed, and this is the technical heart.

M_j has characteristic polynomial λ² − Aλ + (P − 1), where P = αβ. Substituting
λ = 2√2 gives 8 − 2√2·A + P − 1 = 0, so:

- **upper** constraint λ₊ ≤ 2√2  ⟺  2√2·A − P ≤ 7
- **lower** constraint λ₋ ≥ −2√2 ⟺ −2√2·A − P ≤ 7

Together: **2√2·|A| ≤ 7 + P**.

Now square. The step is legitimate — an *equivalence*, not merely an
implication — because both sides are positive:

- |α|, |β| ≤ 2, so |A| ≤ 4 < 4√2. (Licenses the first squaring.)
- |P| = |αβ| ≤ 4, so 7 + P ≥ 3 > 0. (Licenses the second.)

**Always check this.** Squaring an inequality is only an equivalence when both
sides are known nonnegative; otherwise it is a one-way implication and the
argument silently breaks. Here it is checked, so nothing is lost.

Squaring gives 8A² ≤ (7+P)². Substituting α = 2u, β = 2T_k(u) with u = cos t:

> **Criterion.** With
>
>     D_k(u) = ( 7 + 4u·T_k(u) )² − 8( 2u + 2T_k(u) )²   ∈ ℤ[u],
>
> of degree **2k+2** and leading coefficient 4^(k+1), both eigenvalues of M_j
> lie in [−2√2, 2√2] **if and only if** D_k(u_j) ≥ 0, where u_j = cos(2πj/n).

> **Corollary.** P(n,k) satisfies the Riemann Hypothesis if and only if
> D_k(cos(2πj/n)) ≥ 0 for every j in {1, …, n−1}, **except** j = n/2 when n is
> even and k is odd.
>
> (Those two excluded indices, j = 0 and j = n/2, carry the trivial eigenvalues
> +3 and −3. Their *other* eigenvalues are 1 and −1, both well inside the
> bound, so skipping the index entirely is safe.)

An analytic statement about the poles of a zeta function has become the
nonnegativity of **one integer polynomial** at n−1 cyclotomic points.

## 6. Step three: three exact values decide the structure

Everything else follows from evaluating D_k at three points.

|  | value | why |
|---|---|---|
| D_k(1) | **−7** | T_k(1) = 1, so 11² − 8·4² = 121 − 128 |
| D_k(0) | 49 or 17 | T_k(0) ∈ {0, ±1}, so 49 − 32·T_k(0)² |
| D_k(−1) | **−7** (k odd), **+9** (k even) | T_k(−1) = (−1)^k |

### Finiteness

D_k(1) = −7 < 0, so there is a forbidden band just below u = 1 — and u = 1
corresponds to t = 0, which is exactly where the grid accumulates as n grows.
The grid's smallest nonzero angle is 2π/n.

> **Theorem (finiteness, for EVERY k).** If P(n,k) satisfies the Riemann
> Hypothesis then
>
>     n ≤ π(2 + √2)·√(k²+1).
>
> *Proof.* Put a = 1−cos t, b = 1−cos kt, s = a+b, and τ = (√2−1)² = 3−2√2. On
> s < τ we have a, b < 1, so cos t, cos kt > 0 and
> G = 4√2(x+y) − 4xy = (8√2−4) − (4√2−4)s − 4ab. By AM-GM, 4ab ≤ s², so G > 7
> follows from s² + (4√2−4)s < 8√2−11 — and the left side, increasing in s,
> equals the right side **exactly** at s = τ. Finally 1 − cos θ ≤ θ²/2 gives
> s ≤ (1+k²)t²/2, so every t < √(2τ)/√(k²+1) = (2−√2)/√(k²+1) is forbidden.
> The grid's smallest nonzero angle is 2π/n. ∎
>
> **Theorem (finiteness, sharper, one k at a time).** Let u_k be the largest
> root of D_k in (−1,1). Then n ≤ B_k := 2π / arccos(u_k).

(The root exists because D_k(0) ≥ 17 > 0 and D_k(1) = −7 < 0.) The bound is
**sharp at k = 2, 3, 4** — there the largest Ramanujan n equals ⌊B_k⌋ exactly.

### The parity law

D_k(−1) is −7 for odd k, so for odd k there is a *second* band, at u = −1, that
is at t = π. For even k, D_k(−1) = +9 > 0 and there is no such band.

Now the key observation: **the grid {2πj/n} contains t = π exactly when n is
even** (at j = n/2). And when n is even and k is odd, P(n,k) is bipartite, so
the sample there is the trivial eigenvalue −3 — which is *exempt*. When n is
odd the grid straddles π, landing at distance π/n, inside the band.

> **Theorem (parity law).** For k odd and n odd, if P(n,k) satisfies the
> Riemann Hypothesis then n ≤ ½·π(2+√2)·√(k²+1), and more sharply
> n ≤ π / arccos(−v_k) with v_k the smallest root of D_k in (−1,1). No such
> restriction applies to even n, nor to even k.
>
> The first form is **exactly half** the uniform bound, and for a good reason:
> setting t = π − φ with k odd gives cos t = −cos φ and cos kt = −cos kφ, so
> the expression for G is *identical* with a′ = 1−cos φ, b′ = 1−cos kφ. The only
> change is that for odd n the grid's nearest point to π is at φ = π/n rather
> than 2π/n.

Sharp at k = 1, 5, 7, 9. The slogan: **being bipartite helps.** Bipartiteness
exempts the eigenvalue −3, and for odd k that exemption is worth a factor of
two in n. This is why the tail of the classification is even for odd k.

## 7. Step four: certifying the finite remainder exactly

A finite computation is not yet a proof. At a band edge the decision compares
algebraic numbers, and that is the one place float64 fails silently.

Write c_m = 2cos(2πjm/n). Using 4cos a cos b = 2cos(a+b) + 2cos(a−b):

    A = c_1 + c_k          P = c_{k+1} + c_{k−1}

so A, P and hence D are values at z = ζ_n^j of **Laurent polynomials with
integer coefficients**. Since ζ_n^j is a primitive m-th root of unity for
m = n/gcd(n,j), each value is an algebraic integer of ℤ[ζ_m].

- **Reduce modulo Φ_m.** The value becomes an exact integer coordinate vector.
  It is the zero vector **if and only if** the value is exactly zero. So the
  band-edge cases are decided by pure integer arithmetic, no estimate anywhere.
- **Guard the sign.** For a nonzero value, the product of its conjugates is a
  nonzero rational integer, so |D| ≥ 1 / 249^(deg−1) (using |D| ≤ 249 on the
  conjugate set). Evaluate at a precision set from that separation bound and
  **refuse** to report a sign unless the computed value clears the guard.
  A wrong sign is then excluded, not merely improbable.

## 8. The result

> **Theorem (absolute finiteness).** If n ≥ 231 then P(n,k) fails the Riemann
> Hypothesis for **every** k. Since 1 ≤ k < n/2, the family is finite in both
> variables.
>
> **Theorem (complete classification).** For every n and every k the question is
> decided: exactly **460** pairs (n,k) satisfy the Riemann Hypothesis — **324**
> graphs up to isomorphism — from **13,110** cases decided in exact arithmetic.
> The largest is n = 112; no P(n,k) with k > 45 qualifies at all.

The table below lists k ≤ 10; the full table runs to k = 45 and is generated
into `manuscript/ram_table.tex`.

| k | B_k | count | the n for which P(n,k) satisfies the RH |
|---|---|---|---|
| 1 | 15 | 9 | 3–8, 10, 12, 14 |
| 2 | 23 | 19 | 5–23 |
| 3 | 32 | 18 | 7–16, 18, 20, 22, 24, 26, 28, 30, 32 |
| 4 | 42 | 34 | 9–42 |
| 5 | 51 | 28 | 11–26, then even to 50 |
| 6 | 61 | 20 | 13–16, 18, 20–23, 25, 27–28, 30, 32, 35, 37, 39, 42, 44, 49 |
| 7 | 71 | 39 | 15–36, then even to 70 |
| 8 | 81 | 16 | 17, 19–22, 24, 26, 28–29, 31, 33, 35, 38, 40, 42, 49 |
| 9 | 91 | 50 | 19–46, then even to 90 |
| 10 | 101 | 14 | 21, 23, 25–26, 28, 30, 32, 34, 37, 39, 41, 43, 50, 52 |

Read the table for the structure: a solid run at small n, then (for odd k) only
even n — the parity law — then a hard stop below B_k.

**It is not monotone in k.** k = 9 reaches n = 90 while k = 8 and k = 10 stop at
49 and 52. The reason is a *third* band, interior to (0, π) rather than at an
endpoint, which appears for even k and binds well before the band at u = 1.

## 9. What is open

**Not** finiteness, and no longer the list either — both are now settled for
every n and every k. What is open is a **closed form**: the answer is a
certified list, not a formula. Nothing proves the surviving k stop at 45 rather
than near it except having checked every case, and getting a formula means
understanding the divisibility structure the grid imposes — which is exactly the
question of **which cyclotomic reals avoid a semialgebraic set**, the same
Galois-orbit territory as file 10. Also open: the exact criterion on bases of
three or more vertices (two-vertex bases are done; on any base we have
finiteness with a constant, but not a criterion).

## 10. The bug worth remembering

The exact certifier builds its Laurent polynomials from dictionaries keyed by
exponent. At k = 1 the exponents collide: k and 1 are the same key, and k−1 and
−(k−1) are both 0. A Python dict *literal* keeps only the last of each duplicate
key, so the polynomial silently lost half its terms, and the exact classifier
declared **every** P(n,1) Ramanujan — including P(9,1), whose spectrum contains
2cos(8π/9) − 1 = −2.879.

The float64 classifier, running alongside as a control with no authority,
disagreed on exactly four values and failed the run.

**The lesson is the sharp one:** the *exact* method was the wrong one, and only
the *approximate* method knew. A control is not there to be less accurate than
the thing it checks — it is there to be independent of it.
