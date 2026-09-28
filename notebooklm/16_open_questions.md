# 16 — What is genuinely still open, and what to try next

## 1. The state of play, stated precisely

**Settled.**
- Z(P(n,2)) = 6 for n ≥ 10, published in 2020. Our own certificates
  independently give it for 9 ≤ n ≤ 130 except n = 10 — note that this *adds*
  n = 9 and *misses* n = 10, where the period-one symbol has too few distinct
  grid values; n = 10 is covered by the published result, not by us.
- Z(P(n,3)) = 8 for n ≥ 13 (combinatorially, elsewhere); matrix certificates at
  n = 40, 60, 80, 120.
- **Z(P(n,4)) = 10** for every n divisible by 60, 70 or 90.
- **Z(P(n,5)) = 12** for every n divisible by 24.
- **Z(P(60,6)) = Z(P(72,6)) = 14** — numerically certified, not yet exact.
- The ceiling: nullity ≤ 2k+2 for every matrix carrying the pattern, with
  equality iff the monodromy is the identity.

**Open.**
1. Z(P(n,4)) and Z(P(n,5)) for n **outside** those residue classes.
2. Z(P(n,k)) for **k ≥ 7**, for any n at all; and k = 6 for n outside {60, 72}.
5. Exact-arithmetic certification of the k = 6 values.
3. Whether Z(P(n,k)) = 2k+2 for all sufficiently large n (the natural
   conjecture, per gcd class).
4. Whether M(P(n,k)) = Z(P(n,k)) in general.

## 2. What is NOT the obstruction

Two things have been ruled out, which narrows the problem usefully.

**It is not a shortage of dimensions.** For nullity r = 2k+2, a symmetric
matrix needs r(r+1)/2 = (k+1)(2k+3) conditions against 5n free weights, and a
non-symmetric one needs r² against 8n. Both budgets are met comfortably for
every graph tried. So a naive count says 2k+2 ought to be generically available,
and it is not.

**It is not that the rational search was too small.** The enumeration of
rational symbols is **finite and complete** for each k, because deg Ψ_d ≤ k+1
forces φ(d) ≤ 2k+2 and only finitely many d qualify. So "no rational symbol
attains 2k+2" for k = 3, 6, 7, 8, 9 is a theorem, not a search limit. Looking
harder in that direction is provably wasted effort.

## 3. What the obstruction actually is

At k = 7, of 385 rational candidates, **378 fail because F is not in the
three-parameter family** and only 7 fail realisability (c² ≤ 0).

So the binding constraint is the **k − 2 linear membership conditions imposed on
a 3-dimensional family**, and it tightens as k grows: the family stays
3-dimensional while the space of monic degree-(k+1) polynomials grows.

That is a precise diagnosis, and it names its own fix.

## 3b. What the period-d work settled, and what it did not

The parameter shortage is **solved**. The rank law `min(2d+1, k+1)` says the
symbol map becomes surjective at `d ≥ ⌈k/2⌉`, and taking `d = 3` at `k = 6`
produced genuine certificates — the first at `k ≥ 6`, in a range where period 1
is provably incapable.

What it did not settle:

- **Exact certification.** The weights are algebraic numbers from a Newton
  solve, not integers. Choosing the root set as a union of full Galois orbits
  makes the target symbol rational and is the route to fixing this.
- **The degeneracy.** At `n = 48` and `n = 54`, where the root set has no
  slack, *every* solution collapses a spoke, at singular points where the
  Jacobian rank drops. We observe this; we cannot prove it must happen.
- **k = 7, 8.** These need `d ≥ 4` and `n ≥ 72`, `80` respectively. Untried.

## 4. Priority 1 — period-d symbols

A period-d construction (weights repeating with period d | n) commutes with ρ^d
rather than ρ. Fourier over Z_(n/d) splits the matrix into n/d blocks of size
2d, and the construction carries **5d − 1 free ratios** instead of 3, against
the same k+1 coefficients. So

    5d − 1 ≥ k + 1   ⟺   d ≥ (k + 2)/5

restores the parameter count. For k = 6 that is d ≥ 2; for k = 13, d ≥ 3.

This is the one change that addresses the actual obstruction rather than
working around it. Concretely, the programme is:

- Derive the period-d symbol explicitly (the 2k+2 Floquet multipliers are the
  roots of a real reciprocal polynomial of degree 2k+2; equivalently a
  degree-(k+1) polynomial in s' = 2cos(2πℓ/(n/d))).
- Characterise the membership conditions, as the k−2 conditions were
  characterised in the period-1 case.
- Search for rational (hence Galois-closed) symbols, exactly as before.

**Caveat from experience.** The earlier period-two work found that the extra
parameters brought a *new* difficulty: fitting five points determined the curve
uniquely and forced c² ≤ 0, so only four points could be fitted. Realisability
may become the binding constraint once the parameter count is fixed. That is
worth anticipating rather than rediscovering.

## 5. Priority 2 — general n, not more special n

The gap between this project and a clean general theorem is that the results
hold on congruence classes. **One construction valid for all sufficiently large
n is worth more than ten more residue classes.**

And there is a strong reason to want it: by the ceiling theorem, such a
construction would **settle the problem outright** for that k, because the
method's ceiling equals the upper bound. There is no residual gap to close
afterwards.

Two routes: a period-d family whose modulus can be taken to be any n, or an
argument that for large n the grid Γ_n always contains a compatible
configuration of k+1 points.

## 6. Priority 3 — irrational symbols for k ≥ 6

Rationality is sufficient, not necessary: at k = 3 no rational symbol works but
irrational ones do, at n = 40, 60, 80, 120. The exhaustive triple scan finds
these, and it is complete for nullity ≥ 6 (since three grid roots determine the
parameters, every symbol with ≥3 grid roots arises from some triple).

Over n ≤ 130 that scan reaches 2k+2 for k ≤ 5 but only 8, 10, 8 for k = 6, 7, 8
against ceilings 14, 16, 18. Whether that reflects a real limit of period-one
symbols or merely the search range is **unknown**, and extending the scan is
cheap relative to priority 1. Worth a bounded run first.

## 7. Priority 4 — prove the obstruction is real

The complementary outcome: show that for certain (n,k), M(P(n,k)) < 2k+2. That
would turn a computational gap into a theorem, and would prove that
M(G) < Z(G) for this family — itself a result of interest, since it would mean
no matrix certificate can ever settle those cases.

Current evidence: searches over both matrix classes plateau near 10⁻⁴ for
r = 7, 8 on P(12,3) over hundreds of independent starts, against 10⁻¹⁶ when a
solution exists. Suggestive, but **no proof, and no single (n,k) is proved to
have M < 2k+2.** Do not overstate this.

## 8. Deprioritised

- More exhaustive Z values by brute force. Cost grows as C(2n−1, m−1); (3,5)
  would take some 10⁴ years. The marginal value is low.
- The DP(n,k) family. The ceiling argument should transfer, and no lower bounds
  exist there, so it is genuinely open — but it is breadth, not depth.
- Adding an "application". Field data says applications sit *on top of* a
  theorem rather than substituting for one.

## 9. The honest summary

The method is now completely understood in the period-one case: its ceiling is
known exactly, the mechanism that reaches the ceiling is identified, and the
search over rational symbols is provably exhausted. What remains is to enlarge
the family — which is a well-posed construction problem with a clear parameter
count, not a search for inspiration.


## The ceiling question, sharpened

Previously stated as: *is the nullity ceiling a property of the cover, or only of
matrices respecting the rotation?* That is now a better question.

**Settled.** For every two-vertex base B_{p,q,w} — a loop of voltage p, a loop of
voltage q, one connecting edge of voltage w — the ceiling holds for *every*
matrix carrying the pattern, not just equivariant ones: null A <= 2(p+q). See
file 09. P(n,k) is the case p=1, w=0.

**Why it works there.** The outer row meets exactly one inner variable, whose
coefficient is nowhere-zero and hence a unit in the ring of sequences on Z_n.

**Still open, and now precisely stated.** *Which bases admit that elimination?*
The condition is a splitting V(B) = S ∪ T under which each S-row meets exactly
one T-variable. Concretely the first unknown case is the theta base: three edges
between two vertices, voltages 0,1,2, no loops. Its outer row meets three inner
variables at once and no single-step elimination exists, so nothing here applies
and the ceiling is unknown there.

**Why the numerical route is closed.** Four search instruments were built to look
for a counterexample; all four failed their controls, the last by missing a
matrix that is explicitly constructible (file 13). A search can establish
attainment — a found matrix is independently checkable — but only a proof can
establish a ceiling. Any further progress here is a proof problem.
