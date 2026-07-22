# 07 — Circulant matrices and Fourier block-diagonalisation

Why symmetry shatters a big matrix into tiny ones.

## 1. The shift matrix

Let P be the n×n **cyclic shift**: P sends basis vector e_i to e_(i+1), indices
mod n. Then P^n = I, and P⁻¹ = P^T is the backward shift.

A **circulant** matrix is any polynomial in P:

    C = c_0 I + c_1 P + c_2 P² + ... + c_(n−1) P^(n−1).

Equivalently, every row is the previous row shifted right by one. Circulants are
exactly the matrices that **commute with P** — i.e. that are invariant under the
rotation.

## 2. The eigenvectors are roots of unity

Let ω = e^(2πi/n) and fix m. Consider the vector

    f_m = (1, ω^m, ω^(2m), ..., ω^((n−1)m)).

Then P f_m = ω^(−m) f_m (or ω^m depending on your shift convention) — f_m is an
eigenvector of P. So **every circulant has the same eigenvectors**, and they do
not depend on the entries at all. A circulant C has eigenvalue

    Σ_j c_j ω^(jm)

on f_m. Diagonalising one matrix diagonalises all of them simultaneously.

This is the discrete Fourier transform, and it is the reason symmetry is so
powerful: it replaces one n×n problem by n independent 1×1 problems.

## 3. The symmetric combination that keeps things real

The specific circulants in this project are of the form

    a I + b (P + P⁻¹).

Its eigenvalue on f_m is

    a + b(ω^m + ω^(−m)) = a + b · 2cos(2πm/n) = a + b s_m,

using ω^m + ω^(−m) = 2cos(2πm/n) from file 01. So the whole matrix is
controlled by the grid value s_m ∈ Γ_n. Similarly

    d I + e (P^k + P^(−k))

has eigenvalue d + e · 2cos(2πkm/n) = d + e t_m, where t_m = 2cos(2πkm/n).

Note carefully: **s_m and t_m are not independent**. Both come from the same
angle θ = 2πm/n; s is 2cos θ and t is 2cos kθ. File 08 turns that dependence
into an exact polynomial relation, and that relation is the key to everything.

## 4. Block-diagonalising the graph matrix

Take a matrix A ∈ S(P(n,k)) that is invariant under the rotation ρ. Then all
the outer edge weights are equal (call it b), all spokes equal (c), all inner
edge weights equal (e), and the two diagonals are constant (a on outer, d on
inner). In block form, with outer vertices first,

    A = [ U   C ]        U = a I + b(P + P⁻¹)
        [ C   V ]        V = d I + e(P^k + P^(−k))
                          C = c I

Applying the Fourier basis to both blocks at once splits A into **n independent
2×2 blocks**, one for each m:

    M_m = [ a + b s_m     c      ]
          [    c       d + e t_m ]

and therefore

    nullity(A) = Σ over m of nullity(M_m).

Each M_m is a 2×2 real symmetric matrix with **nonzero off-diagonal entry c**.
A 2×2 symmetric matrix with a nonzero off-diagonal entry cannot be the zero
matrix, so if it is singular its rank is exactly 1 and its nullity is exactly 1.
Hence

    nullity(A) = #{ m ∈ Z_n : det M_m = 0 },

and

    det M_m = (a + b s_m)(d + e t_m) − c².

**A whole 2n × 2n nullity problem has become: count how many m make one scalar
expression vanish.** That is the payoff of symmetry.

## 5. The doubling, and the two exceptions

Since s_m = s_(n−m) and t_m = t_(n−m), the blocks at m and n−m are identical.
So each grid value s strictly between −2 and 2 that makes the determinant
vanish contributes **2** to the nullity. The values s = +2 (from m = 0) and
s = −2 (from m = n/2, when n is even) are fixed by m ↦ n−m and contribute only
**1** each.

Consequence worth remembering: **even nullities come from interior grid values,
odd nullities require using an endpoint ±2.**

## 6. Breaking the symmetry: period d

You do not have to be fully rotation-invariant. If the weights are periodic
with period d (where d divides n), the matrix commutes with ρ^d rather than ρ,
and Fourier analysis over Z_(n/d) splits it into n/d blocks of size 2d instead
of n blocks of size 2. You get more free parameters (5d − 1 independent ratios
instead of 3) at the cost of larger blocks.

This is the natural knob to turn when the fully symmetric construction runs out
of parameters, and file 16 explains why it is the right next step.

## 7. What to take away

- All circulants share the Fourier eigenvectors; symmetry diagonalises
  everything at once.
- A rotation-invariant A on P(n,k) splits into n blocks of size 2.
- nullity(A) = #{m : (a + b s_m)(d + e t_m) = c²}.
- Interior grid values count twice, the endpoints ±2 count once.
- s_m and t_m come from the same angle and are therefore linked — see file 08.
