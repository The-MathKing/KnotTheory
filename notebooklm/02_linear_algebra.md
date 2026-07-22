# 02 — Linear algebra: rank, nullity, eigenvalues, symmetric matrices

This is the engine room. The central object of the whole project is the
**nullity** of a matrix, so this file builds up to that carefully.

## 1. Vectors, matrices, and the kernel

A vector in R^N is a list of N real numbers. An N×N matrix A takes a vector x
to a new vector Ax, by the rule (Ax)_u = Σ_v A_(u,v) x_v — row u of A dotted
with x.

The **kernel** (or null space) of A is

    ker A = { x : Ax = 0 }.

It is a subspace: if Ax = 0 and Ay = 0 then A(x + cy) = 0 too.

The **nullity** of A is dim(ker A) — the number of independent directions that
A crushes to zero. The **rank** is the dimension of the output space. They are
tied together by the **rank–nullity theorem**:

    rank(A) + nullity(A) = N.

Nullity 0 means A is invertible. Large nullity means A is very degenerate.

**Everything in this project is about making nullity as large as possible**,
subject to A having a prescribed pattern of zeros and nonzeros.

## 2. Reading nullity off the equations

Concretely: nullity(A) = r means there are r independent solutions to the
system of N equations Ax = 0. Each row of A gives one equation. If the rows are
highly redundant, the nullity is large.

Worth internalising: **a single explicit nonzero x with Ax = 0 proves nullity
≥ 1.** More generally, r independent vectors in the kernel prove nullity ≥ r.
This is why a "certificate" works: to prove a lower bound you exhibit an
object, you do not have to rule anything out.

## 3. Eigenvalues and eigenvectors

λ is an **eigenvalue** of A with **eigenvector** x ≠ 0 if

    Ax = λx.

Equivalently, (A − λI)x = 0, so λ is an eigenvalue exactly when
nullity(A − λI) ≥ 1. The **geometric multiplicity** of λ is nullity(A − λI).

So: **nullity(A) is the geometric multiplicity of the eigenvalue 0.** Making
the nullity large is the same as making 0 a highly degenerate eigenvalue.

The eigenvalues are the roots of the **characteristic polynomial**
det(A − λI) = 0.

## 4. Symmetric matrices and the spectral theorem

A is **symmetric** if A_(u,v) = A_(v,u).

**Spectral theorem.** A real symmetric N×N matrix has N real eigenvalues
(with multiplicity) and an orthonormal basis of eigenvectors. So it is
completely diagonalisable, with no nasty Jordan blocks. In particular for
symmetric matrices geometric and algebraic multiplicity agree, and nullity is
simply "how many eigenvalues equal 0".

This is why the project uses symmetric matrices by default: nullity is exactly
the count of zero eigenvalues, which is stable and computable.

**Non-symmetric matrices** still have a kernel and a nullity; you just compute
it by rank rather than by eigenvalues, and numerically you use singular values
instead of eigenvalues. The project needs both cases — see file 05.

## 5. Determinants and block matrices

det(A) = 0 exactly when nullity(A) ≥ 1. For a 2×2 matrix,

    det [ p  q ; q  r ] = pr − q².

That tiny formula is used hundreds of times in this project, because the
symmetry of the graphs reduces a big matrix to a pile of 2×2 blocks (file 07).

For a **block matrix** with square blocks,

    M = [ U  C ; C  V ],

if V is invertible then M is equivalent (by a congruence that does not change
rank) to a block-diagonal matrix with blocks V and U − C V⁻¹ C. The matrix
U − C V⁻¹ C is called the **Schur complement**, and

    nullity(M) = nullity(V) + nullity(U − C V⁻¹ C).

More useful here: if C is invertible, you can eliminate one block of variables
entirely. From Ux + Cy = 0 and Cx + Vy = 0, the first gives y = −C⁻¹Ux, and
substituting into the second gives (C − V C⁻¹ U)x = 0. So

    nullity(M) = nullity(C − V C⁻¹ U),

an N/2-sized problem instead of an N-sized one. This single move is the first
step of the main theorem (file 09).

## 6. Why a free diagonal changes everything

Consider the set of matrices that "carry the pattern" of a graph G: A_(u,v) ≠ 0
exactly when uv is an edge, for u ≠ v, with the **diagonal entries completely
unconstrained**.

The freedom on the diagonal is essential. If you fixed the diagonal to zero you
would be talking about the adjacency matrix alone, a single matrix; with the
diagonal free you have a large family, and you get to hunt inside it for a
member with big nullity. Notice that the diagonal is exactly the part of a
matrix that does not correspond to any edge, so leaving it free is the natural
convention: **the graph tells you where the zeros are off the diagonal, and
says nothing about the diagonal.**

## 7. Congruence, inertia, and why signs matter

Two symmetric matrices A and B are **congruent** if B = S^T A S for invertible
S. Congruence preserves the **inertia** — the triple (number of positive, number
of negative, number of zero eigenvalues). It does not preserve the eigenvalues
themselves.

The practical consequence for this project: when a construction produces a
parameter like c² that must be positive for the matrix to be real, that
positivity is a genuine constraint and not an artifact. A construction that
yields c² ≤ 0 does not describe a real symmetric matrix with the right pattern,
and must be discarded. This "realisability" condition is rejected many times in
the searches, and it is not a technicality.

## 8. Numerical nullity is a trap

On a computer, eigenvalues are never exactly zero. You must choose a threshold,
and the threshold must be *relative to the scale of the matrix*. Two real
failures from this project:

- With a loose threshold, a scan reported nullity 7 for a case where the true
  ceiling is 6 — impossible.
- With a threshold relative to max|A|, a badly scaled matrix (one huge diagonal
  entry) reported nullity 48 when the ceiling was 16.

The fixes are (a) test each small block against its own scale, not a global
one, and (b) where it matters, do the arithmetic **exactly** over the rational
numbers or a number field, never in floating point. File 12 covers this.

**Working rule that came out of it:** wrap every numerical search inside a
bound it cannot legally violate. That bound is the only thing that will tell
you an answer is wrong when it looks right.

## 9. What to take away

- nullity = dim ker = geometric multiplicity of eigenvalue 0.
- To prove nullity ≥ r, exhibit r independent kernel vectors. Certificates are
  existence proofs; they do not require ruling anything out.
- Symmetric ⇒ real eigenvalues, nullity = count of zero eigenvalues.
- If C is invertible you can eliminate half the variables: nullity(M) =
  nullity(C − V C⁻¹ U).
- The diagonal being free is what makes the problem a search rather than a
  single computation.
- Numerical nullity needs a scale-aware threshold, and exact arithmetic where
  it counts.
