# 09 — Transfer matrices, monodromy, and the exact ceiling

This is the structural theorem of the project. It applies to **every** matrix
with the graph's pattern — symmetric or not, rotation-invariant or not.

## 1. Setting up the kernel equations

Let A be combinatorially symmetric for P(n,k) (file 05). Name the entries:

- b_i = A(u_i, u_(i+1)) and b'_i = A(u_(i+1), u_i)   — outer edges
- c_i = A(u_i, v_i)     and c'_i = A(v_i, u_i)       — spokes
- e_i = A(v_i, v_(i+k)) and e'_i = A(v_(i+k), v_i)   — inner edges
- a_i = A(u_i, u_i), d_i = A(v_i, v_i)               — diagonals (free)

All of b, b', c, c', e, e' are nonzero; that is what "carries the pattern"
means. Write a kernel vector as (x, y), x on the outer vertices and y on the
inner ones. Then Ax = 0 reads, row by row:

    (O_i)   b'_(i−1) x_(i−1) + a_i x_i + b_i x_(i+1) + c_i y_i = 0
    (I_i)   e'_(i−k) y_(i−k) + d_i y_i + e_i y_(i+k) + c'_i x_i = 0

for every i ∈ Z_n. Equation (O_i) is the row at outer vertex u_i; (I_i) is the
row at inner vertex v_i.

## 2. Eliminating the inner variables

Every spoke weight c_i is **nonzero**, so (O_i) solves uniquely for y_i:

    y_i = − ( b'_(i−1) x_(i−1) + a_i x_i + b_i x_(i+1) ) / c_i.

So y is completely determined by x. Substituting this into (I_i) gives a single
scalar equation in the x variables alone. Since y_j depends on x at
{j−1, j, j+1}, and (I_i) uses y at {i−k, i, i+k}, the resulting equation
involves x at

    {i−k−1, i−k, i−k+1} ∪ {i−1, i, i+1} ∪ {i+k−1, i+k, i+k+1},

which is **nine positions** (for k ≥ 3 these three triples are disjoint).

So we get, for each i, a relation

    Σ (p from −k−1 to k+1) γ_(i,p) x_(i+p) = 0,

with γ_(i,p) nonzero only at those nine positions, and with the two extreme
coefficients

    γ_(i, k+1)  = − e_i · b_(i+k) / c_(i+k)        ≠ 0
    γ_(i, −k−1) = − e'_(i−k) · b'_(i−k−1) / c_(i−k) ≠ 0.

Both are products and quotients of nonzero quantities, hence nonzero. **This is
the crucial point.**

## 3. It is a recurrence of order exactly 2k+2

Because the coefficient of x_(i+k+1) is nonzero, the relation solves for
x_(i+k+1) in terms of the previous 2k+2 values x_(i−k−1), ..., x_(i+k). Because
the coefficient of x_(i−k−1) is also nonzero, it solves backwards too.

So the relation is a **linear recurrence of order 2k+2**: specify any 2k+2
consecutive values of x and the entire bi-infinite sequence is determined. The
solution space over the integers Z is therefore exactly (2k+2)-dimensional.

### A first consequence, worth stating on its own

A nonzero solution cannot vanish on 2k+2 consecutive indices — if it did, the
recurrence would propagate zero in both directions and the solution would be
identically zero.

**And 2k+2 consecutive outer vertices is exactly the forcing set the rotation
bootstrap produces (file 06).** So this statement *is* the M ≤ Z argument of
file 05, specialised to that particular forcing set. The order of the
recurrence equals the size of that forcing set. That is not a coincidence; it
is the same fact seen twice.

## 4. Monodromy

Bundle the state:

    Z_i = ( x_(i−k−1), x_(i−k), ..., x_(i+k) )  ∈ R^(2k+2).

The recurrence gives a matrix T_i (a companion matrix) with Z_(i+1) = T_i Z_i.
Going once around the cycle defines the **monodromy**

    T = T_(n−1) · T_(n−2) · ... · T_1 · T_0   ∈ GL(2k+2, R).

A solution on Z corresponds to a kernel vector of A precisely when it is
**n-periodic**, i.e. when it is a fixed vector of T.

## 5. The theorem

> **Theorem (Reduction).** For 2k < n and any combinatorially symmetric A for
> P(n,k),
>
>     nullity(A) = dim ker(T − I)   ≤ 2k + 2,
>
> with equality **if and only if T = I**. Moreover
>
>     det T = (Π b'_i)(Π e'_i) / ((Π b_i)(Π e_i)),
>
> which equals 1 whenever A is symmetric.

**Proof of the main statement.** The map x ↦ (x, y = determined by x) is a
bijection between n-periodic solutions of the recurrence and ker A: given a
periodic x satisfying all the relations, define y by (O_i) — then all the (O_i)
hold by construction and all the (I_i) hold because they are exactly the
relations. Conversely any kernel vector gives such an x. So nullity(A) is the
dimension of the fixed space of T acting on a (2k+2)-dimensional space, which
is at most 2k+2, with equality exactly when T fixes everything, i.e. T = I. ∎

**The determinant.** Each T_i is a companion matrix whose determinant is
γ_(i,−k−1) / γ_(i,k+1). Multiply over i ∈ Z_n; every index set runs over a full
residue system, so the c's cancel and the stated formula drops out.

## 6. Why this is the important theorem

The inequality nullity ≤ 2k+2 is not itself new — it follows from M ≤ Z and the
bootstrap bound Z ≤ 2k+2. What is new and useful is:

1. **The ceiling is exactly 2k+2**, identified precisely, with no slack. So the
   matrix-certificate method could in principle settle the problem completely —
   or it could be provably unable to, if the ceiling were lower. It is not.
2. **The equality criterion is explicit and constructive**: nullity = 2k+2 iff
   the monodromy is the identity. That converts a search over matrices into a
   concrete algebraic condition.
3. **It covers non-symmetric matrices too**, so nothing is lost by enlarging
   the class.
4. It gives an **automatic correctness check**: any claimed certificate with
   nullity above 2k+2 is a bug. This caught two real numerical failures (file
   12).

## 7. An equivalent form worth knowing

For symmetric A with C = diag(c_i), set U = the outer block and
S = C⁻¹ (inner block) C⁻¹. Then

    nullity(A) = dim ker( S U − I ),

the geometric multiplicity of the eigenvalue 1 in a **product of two symmetric
matrices**, one carrying the outer-cycle pattern and one the inner-cycle
pattern, each with free diagonal and nonzero prescribed off-diagonal entries.
This reformulation makes the problem look like a question about pairs of Jacobi
matrices, which may be the right frame for attacking the remaining cases.

## 8. Reconciling with file 07

For a rotation-invariant A, T is the n-th power of a single matrix, and T = I
requires all 2k+2 of its eigenvalues to be n-th roots of unity. Those
eigenvalues are precisely the roots of the symbol (file 08) read through
z + 1/z = s. So "all k+1 roots of F lie on the grid" and "the monodromy is the
identity" are the same statement in two languages.

## 9. Verification

Checked before use: 189 random matrices over 63 pairs (n,k) with 2 ≤ k ≤ 7
confirm the nine-position sparsity, both end-coefficient formulas, and
nullity(A) = dim ker(T − I) ≤ 2k+2; 60 further matrices over 30 pairs, in both
matrix classes, confirm the determinant formula, the SU product form, and the
statement that no kernel vector vanishes on u_0, ..., u_(2k+1).

## 10. What to take away

- Nonzero spokes let you eliminate y entirely.
- What remains is one nine-term recurrence of order exactly 2k+2.
- nullity(A) = dim ker(T − I) ≤ 2k+2, equality iff T = I.
- The order 2k+2 *is* the size of the bootstrap's forcing set — the method's
  ceiling equals the upper bound it is trying to match.
- Any claimed nullity above 2k+2 is a bug, and that fact is a useful alarm.


## The reduction is not special to P(n,k)

The proof of the reduction theorem uses exactly one structural fact: **the row
at an outer vertex meets exactly one inner variable**, and its coefficient is a
spoke weight, so it can be divided out. Nothing in it requires the outer cycle
to have voltage 1.

Why "nonzero" is the wrong word for what matters: the coefficients live in the
ring of *sequences* on Z_n, which has zero divisors. A sequence that is nonzero
somewhere is not invertible. What licenses the division is that the spoke weight
is **nowhere** zero — it is an edge weight, so it is nonzero at every position —
which makes it a *unit* in that ring.

Let B_{p,q,w} be the two-vertex base with a loop of voltage p at u, a loop of
voltage q at v, and one edge uv of voltage w. Every such cover is cubic on 2n
vertices, and P(n,k) = B_{1,k,0}.

**Theorem.** For n > 2(p+q) and every A carrying the pattern, eliminating the
inner coordinates leaves one recurrence supported on the nine offsets

    { -(p+q), -q, -(q-p), -p, 0, p, q-p, q, p+q }

with both extreme coefficients nonzero. Hence null A = dim ker(T - I) <= 2(p+q),
which is the degree span of det M(zeta), with equality iff T = I.

The original reduction theorem is the case p = 1, w = 0, where 2(p+q) = 2k+2.

The extreme coefficient is always a product of one inner edge weight, one outer
edge weight and one spoke weight — all nonzero because they are edges — which is
why no cancellation can occur there. If p = q the nine offsets collapse to five,
but the extreme coefficients and the order are unchanged.

**What it does not cover.** The hypothesis is a genuine restriction. On the theta
base (two vertices joined by three edges, voltages 0,1,2, no loops) the outer row
reads a_i x_i + c_i y_i + f_i y_{i+1} + g_i y_{i+2} = 0 — three inner variables
at once — and no single-step elimination exists. Whether the ceiling still holds
there is open.
