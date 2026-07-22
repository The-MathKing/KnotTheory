# 01 — Prerequisites: numbers, arithmetic, polynomials

Everything here is high-school level or just past it. Nothing later in the
folder needs more background than this file provides.

## 1. Sets, sums, products

A **set** is an unordered collection with no repeats: {1, 2, 4, 7, 8}. The
symbol ∈ means "is an element of". |S| is the number of elements.

Σ means "add up" and Π means "multiply together". So Σ(i=1 to 3) i = 1+2+3 = 6
and Π(i=1 to 3) i = 6 as well, coincidentally.

**Z_n** (written "Z mod n") means the set {0, 1, 2, ..., n−1} with arithmetic
that wraps around: in Z_12, 11 + 3 = 2, because 14 wraps past 12. This is
clock arithmetic. It appears constantly, because the graphs in this project
have vertices indexed by Z_n arranged in a circle.

## 2. Divisibility, gcd, and the clock fact

"d divides n", written d | n, means n is a whole multiple of d.

**gcd(a, b)** is the greatest common divisor: the largest number dividing both.
gcd(12, 8) = 4, gcd(9, 5) = 1. When gcd(a,b) = 1 we say a and b are **coprime**.

**lcm(a, b)** is the least common multiple. lcm(4, 30) = 60.

### The single most useful fact in this project

Stand on an n-hour clock and repeatedly jump forward k hours. How many
distinct loops do you trace before returning to where you started, and how many
hours do you visit?

You visit exactly n/gcd(n,k) hours before returning, and if you then start
again from an unvisited hour, you trace another loop. In total you get exactly
**gcd(n,k) separate loops, each of length n/gcd(n,k)**.

Example: n = 12, k = 4. gcd = 4. Starting at 0: 0 → 4 → 8 → 0. That is a loop
of length 3 = 12/4. There are 4 such loops: {0,4,8}, {1,5,9}, {2,6,10},
{3,7,11}.

Example: n = 12, k = 5. gcd = 1. Starting at 0: 0,5,10,3,8,1,6,11,4,9,2,7,0 —
a single loop through all 12.

This one fact explains the entire inner structure of the graphs in file 03.

## 3. Complex numbers and roots of unity

A **complex number** is a + bi where i² = −1. You can add and multiply them
like ordinary algebra, replacing i² by −1 whenever it appears.

**Euler's formula**: e^(iθ) = cos θ + i sin θ. So e^(iθ) is the point on the
unit circle at angle θ.

An **n-th root of unity** is a complex number z with z^n = 1. There are exactly
n of them:

    z_m = e^(2πi m / n),   m = 0, 1, ..., n−1,

evenly spaced around the unit circle. z_0 = 1 always.

A root of unity is **primitive** of order d if z^d = 1 but no smaller positive
power gives 1. The primitive d-th roots of unity are e^(2πi j/d) with
gcd(j, d) = 1; there are φ(d) of them, where φ is Euler's totient function
(the count of integers in 1..d coprime to d). φ(1)=1, φ(2)=1, φ(3)=2, φ(4)=2,
φ(5)=4, φ(6)=2, φ(12)=4, φ(24)=8, φ(30)=8.

### The quantity that runs through everything

If z = e^(iθ) then

    z + 1/z = z + z̄ = 2cos θ,

a **real** number between −2 and 2. Setting θ = 2πm/n gives

    s_m = 2cos(2πm/n).

These n numbers are the "grid" Γ_n. Two facts about them, both used constantly:

- s_m = s_(n−m). So m and n−m give the same grid value. Each interior value
  (strictly between −2 and 2) is hit by exactly two indices m; the values ±2
  are hit by only one each (m = 0 gives +2; if n is even, m = n/2 gives −2).
- As n grows the grid becomes dense in the interval [−2, 2].

## 4. Polynomials

A polynomial is a₀ + a₁s + a₂s² + ... + a_D s^D. Its **degree** is D (the
highest power with a nonzero coefficient). It is **monic** if a_D = 1.

**Roots.** r is a root if F(r) = 0. A degree-D polynomial has exactly D complex
roots counted with multiplicity, and factors as
F(s) = a_D (s − r₁)(s − r₂)...(s − r_D).

**Squarefree** means no repeated roots — all D roots are distinct.

**Symmetric functions.** If you expand (s − r₁)(s − r₂)(s − r₃), the
coefficients are built from the roots:

    s³ − (r₁+r₂+r₃)s² + (r₁r₂ + r₁r₃ + r₂r₃)s − r₁r₂r₃.

So specifying the roots specifies the coefficients, and vice versa. This is why
"choose the roots" and "choose the coefficients" are interchangeable moves.

**Rational coefficients matter.** If a polynomial has rational (or integer)
coefficients, its roots are constrained in a strong way — they come in
"conjugate families". That is the subject of file 10, and it is the mechanism
behind the main result.

## 5. Recurrences

A **linear recurrence** expresses one term of a sequence from earlier ones:

    x_(i+1) = c₁ x_i + c₂ x_(i−1) + ... + c_p x_(i−p+1).

This has **order p**: you need p consecutive starting values to determine the
whole sequence, and the set of all solutions forms a p-dimensional space.

The order is the single most important number about a recurrence, and the main
theorem of this project is a statement that a certain recurrence has order
exactly 2k+2.

## 6. What to take away

- Clock arithmetic and gcd give the loop structure of the graphs.
- 2cos(2πm/n) is the recurring quantity; it lives on a grid Γ_n in [−2, 2].
- A polynomial is equivalently its coefficients or its roots.
- Rational coefficients force structure on the roots.
- A recurrence of order p has a p-dimensional solution space.
