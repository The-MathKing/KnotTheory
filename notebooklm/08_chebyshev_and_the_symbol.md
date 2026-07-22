# 08 — The polynomials L_k, and the three-parameter symbol

File 07 ended with: nullity(A) = #{m : (a + b s_m)(d + e t_m) = c²}, where
s_m = 2cos(2πm/n) and t_m = 2cos(2πkm/n). This file eliminates t in favour of s
and extracts the object that controls everything.

## 1. The polynomials L_k

Define L_k by the property

    L_k( z + 1/z ) = z^k + 1/z^k.

Concretely, with s = z + 1/z:

- L_0 = 2
- L_1 = s
- L_2 = s² − 2         (because (z+1/z)² = z² + 2 + 1/z²)
- L_3 = s³ − 3s
- L_4 = s⁴ − 4s² + 2
- L_5 = s⁵ − 5s³ + 5s
- and generally the three-term recursion **L_k = s · L_(k−1) − L_(k−2)**.

Each L_k is a **monic polynomial of degree k with integer coefficients**. (They
are the Lucas/Dickson polynomials, and are a rescaling of the Chebyshev
polynomials of the first kind: L_k(s) = 2 T_k(s/2).)

### Why this is exactly what we need

Put z = e^(iθ). Then z + 1/z = 2cos θ and z^k + 1/z^k = 2cos kθ. So

    **2cos(kθ) = L_k( 2cos θ )   exactly.**

Setting θ = 2πm/n gives **t_m = L_k(s_m)**, with no approximation. The two grid
quantities are not independent at all: t is a fixed polynomial function of s.

## 2. The symbol

Substitute t = L_k(s) into the singularity condition. Scale so that b = 1 (we
may, since the whole matrix can be scaled), and divide through by e (nonzero):

    (a + s)(d + e L_k(s)) − c² = 0
    ⟺  e·s·L_k(s) + a·e·L_k(s) + d·s + (ad − c²) = 0
    ⟺  (s + a) L_k(s) + α s + β = 0,

where

    α = d / e,      β = (a d − c²) / e.

Define the **symbol**

    F(s) = (s + a) L_k(s) + α s + β.

Then:

> **nullity(A) = #{ m ∈ Z_n : F(s_m) = 0 }.**

F is **monic of degree k+1**, since L_k is monic of degree k.

## 3. The crucial counting fact

F has degree k+1, so it has k+1 coefficients to play with — but it carries only
**three free parameters** (a, α, β), no matter how large k is. Equivalently:

    F(s) − s·L_k(s)  must lie in the span of  { L_k(s), s, 1 },

which is k+1 − 3 = **k − 2 linear conditions** on the coefficients of F.

So as k grows, the family of achievable symbols becomes a smaller and smaller
slice of the space of monic degree-(k+1) polynomials. That tightening is the
central obstruction of the whole project, and file 16 explains the fix.

## 4. Prescribing roots: the condition is linear

Suppose we want F(r) = 0 for a chosen grid value r. Expand:

    (r + a) L_k(r) + α r + β = 0
    ⟺ **a · L_k(r) + α · r + β = − r · L_k(r).**

This is **linear in (a, α, β)**. So three distinct prescribed roots give three
linear equations in three unknowns, which generically determine (a, α, β)
uniquely, and a fourth root cannot be imposed.

## 5. The mistake this project made, and the correction

From "three roots can be prescribed and no more", it is tempting to conclude
"so the nullity is at most 6" (three interior roots, each counting twice). The
project asserted exactly that, and it is **wrong**.

The premise is right; the inference is not. Prescribing three roots
**determines the other k − 2 roots as well** — they are whatever they are. And
those remaining roots may land on the grid Γ_n all by themselves.

They do exactly when arithmetic puts them there. That is file 10.

Concretely: for k = 5 the symbol s·L_5(s) − 1 has degree 6 and *all six* of its
roots lie in Γ_24. You do not choose six roots; you choose a polynomial whose
roots are forced to be grid values.

## 6. Recovering the matrix from the symbol

Given a target symbol F, read off its parameters and rebuild A:

1. Compute G = F − s·L_k(s).
2. Let a be the coefficient of s^k in G.
3. Check that G − a·L_k has degree ≤ 1 (this is the membership test). Write
   G − a L_k = α s + β.
4. Set e = 1, d = α, and **c² = a α − β**.
5. The certificate is

       A = [ a I + P + P⁻¹        c I          ]
           [    c I          α I + P^k + P^(−k) ]

6. **Admissibility:** the matrix is real with the correct pattern only if
   **c² > 0**. If c² ≤ 0 the construction fails — the spoke weight would be
   imaginary or zero, and A would not lie in S(P(n,k)). This is a genuine
   constraint, rejected many times in the searches.

## 7. Two worked symbols

**k = 2.** Here degree k+1 = 3 and the family has 3 parameters, so *every*
monic cubic is reachable. Choose any three grid values as roots, solve the
linear system, check c² > 0. This gives Z(P(n,2)) = 6 for essentially all n,
recovering and extending the published result.

**k = 5.** Take a = 0, α = 0, so F(s) = s·L_5(s) + β; take β = −1:

    F(s) = s(s⁵ − 5s³ + 5s) − 1 = s⁶ − 5s⁴ + 5s² − 1.

Its roots are ±1, ±2cos(π/12), ±2cos(5π/12) — all six lie in Γ_24. And
c² = aα − β = 0·0 − (−1) = 1 > 0, with a = d = 0 and c = 1, so the certificate
is the **plain adjacency matrix**. Nullity 12 = 2k+2.

## 8. What to take away

- L_k is monic of degree k with L_k(2cos θ) = 2cos kθ **exactly**.
- The symbol F(s) = (s + a)L_k(s) + αs + β controls the nullity completely.
- F is monic of degree k+1 but has only three free parameters, for every k —
  that is k−2 linear conditions, tightening as k grows.
- The root condition is linear, so three roots may be prescribed and no more.
- But the remaining k−2 roots can land on the grid by themselves, and the
  "cap of 6" inference from this was the project's own error.
- c² = aα − β must be strictly positive or the certificate is not real.
