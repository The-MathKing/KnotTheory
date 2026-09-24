# Research Plan

**Project.** Maximum Nullity of Cyclic Covers of Graphs: A Monodromy Ceiling and
the Zero Forcing Number of Generalized Petersen Graphs
**Category.** Mathematics · **Finalist.** Aryan Padarthi

---

## A. Rationale

Zero forcing began in two unrelated places: controllability of quantum spin
systems, and placement of phasor measurement units in electrical grids. It was
then connected to linear algebra by the inequality M(G) ≤ Z(G), where M(G) is
the largest nullity attainable by a symmetric matrix whose off-diagonal support
is the edge set of G. The inequality makes Z a combinatorial ceiling on a purely
algebraic quantity, and makes lower bounds on Z obtainable by exhibiting a
matrix.

The generalized Petersen graphs P(n,k) are a standard cubic test family. Rashidi,
Shajareh Poursalavati and Tavakkoli (2020) proved Z(P(n,k)) ≤ 2k+2 and determined
Z(P(n,2)). Their Theorem 3.6, asserting Z(P(n,3)) = 8 for n ≥ 12, is false:
Krishnan's July 2026 correction note (arXiv:2607.19412) exhibits Z(P(12,3)) = 7,
the error being a case analysis that never excludes 7-vertex sets. That note
leaves open the stabilization threshold and any rigorous lower bound for k ≥ 4.

This project addresses those two open problems.

## B. Research question

1. Is there an intrinsic ceiling on what a matrix certificate can prove about
   Z(P(n,k)), and where does it sit relative to the known upper bound?
2. Can that ceiling be attained, and by an explicitly checkable matrix?
3. Can Z(P(n,k)) be determined for **all** n rather than for sparse families of n?

## C. Procedures

This is a theoretical mathematics project. There are no human participants, no
vertebrate animals, no potentially hazardous biological agents, and no hazardous
chemicals, activities or devices. All work is proof and computation performed by
the finalist on a personal computer.

**C1 — Structure.** Eliminate the inner coordinates from the kernel equations of
an arbitrary matrix carrying the P(n,k) pattern and identify the resulting scalar
recurrence, its order, and the leading coefficients. Establish when the nullity
equals the recurrence order.

**C2 — Construction.** For rotation-invariant matrices, reduce singularity to a
polynomial condition on a discrete grid and construct matrices meeting the
ceiling. Determine exactly when such a matrix is admissible.

**C3 — Obstruction.** Determine whether the divisibility conditions arising in C2
are intrinsic, and prove the answer rather than observing it.

**C4 — General n.** Construct matrices from repeated blocks whose contributions
compose, so that one finite family of blocks settles an infinite set of n.

**C5 — Certification.** Verify every constructed matrix at the highest standard
available: exact integer or rational arithmetic where possible, and otherwise an
interval (Krawczyk) contraction proof that a true real solution exists. Record
which standard each claim meets.

**C6 — Independent checking.** Compute Z directly by exhaustive search over
vertex subsets for all sizes reachable, validate that solver against every
published value, and reproduce each theorem numerically before relying on it.

## D. Data analysis

Results are theorems and explicit matrices, not measurements, so analysis is
verification rather than statistics. Every computational claim is re-derived by a
single script that reports pass or fail per check. Numerical searches are always
wrapped in a bound they cannot legally exceed (the ceiling of C1), so that an
impossible answer is detected rather than believed. Where a search fails, the
residual and the computational budget are both recorded, because a failure at a
small budget is not evidence of impossibility.

## E. Risk and safety

None. No laboratory work, no fieldwork, no subjects of any kind.

## F. Bibliography

1. S. Rashidi, N. Shajareh Poursalavati, M. Tavakkoli. Computing the zero forcing
   number for generalized Petersen graphs. *J. Algebra Combin. Discrete Struct.
   Appl.* 7(2) (2020) 183–193.
2. A. Krishnan. A correction to the zero forcing number of the generalized
   Petersen graphs P(n,3). arXiv:2607.19412 (2026).
3. AIM Minimum Rank Special Graphs Work Group. Zero forcing sets and the minimum
   rank of graphs. *Linear Algebra Appl.* 428 (2008) 1628–1648.
4. J. H. Conway, A. J. Jones. Trigonometric diophantine equations. *Acta Arith.*
   30 (1976) 229–240.
5. I. Niven. *Irrational Numbers.* Carus Mathematical Monographs 11, MAA, 1956.
6. R. E. Moore, R. B. Kearfott, M. J. Cloud. *Introduction to Interval Analysis.*
   SIAM, 2009. (Krawczyk existence test.)
