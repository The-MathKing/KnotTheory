# Skeleton — the k = 3 note

**This is not a draft. It is a scaffold.** Every sentence is yours to write.
What is here: the structure, the statements (lifted verbatim from the paper, so
they are already correct), the numbers (from `zf_numbers.tex`, so they are
already right), and a note at each point saying what the prose must accomplish.

**Why a skeleton and not a draft.** ISEF Rule 8: *"all materials presented must
be in the researcher's own words."* A draft would be AI prose you then edit,
which is the thing to avoid. Writing from statements you already own is not.

**Target:** 5–9 pages. One result. It ends when the result is proved.

**Claim it makes:** Conjecture 5 of Krishnan, arXiv:2607.19412, is true.

---

## Title

One line. It should name the conjecture or the result, not the method.

## Abstract — target 120–180 words

Must accomplish, in this order:

1. Rashidi–Shajareh Poursalavati–Tavakkoli (2020), Thm 3.6, claims
   Z(P(n,3)) = 8 for all n ≥ 12.
2. Krishnan (arXiv:2607.19412, July 2026) shows it fails at n = 12, where
   Z(P(12,3)) = 7; gives exhaustive values for 7 ≤ n ≤ 20; and states
   **Conjecture 5**: Z(P(n,3)) = 8 for every n ≥ 13. His stated missing
   ingredient: *"a lower-bound proof valid for all large n."*
3. This note supplies it. **Z(P(n,3)) = 8 for every n ≥ 13, and 13 is optimal.**
4. One sentence on method: a reduction to a linear recurrence of order 8,
   identity tiles, and an interval certification in exact rational arithmetic.

Do not mention Part I. Do not mention k ≠ 3. Do not mention the Ramanujan work.

## §1 — Introduction

What the prose must do: state the problem, the history, and the result, and end
with a one-paragraph outline of the proof. Nothing else belongs here.

Facts available:
- Z(G) = zero forcing number; M(G) = maximum nullity; M(G) ≤ Z(G).
- P(n,k): outer cycle u_i ~ u_{i+1}, inner v_i ~ v_{i+k}, spokes u_i ~ v_i.
- Upper bound Z(P(n,3)) ≤ 8 for n ≥ 9 — rotation bootstrap, your
  Theorem `thm:I` with j = 1, k = 3. Krishnan also has this.
- **The entire content is the lower bound.** Say so explicitly; it is what
  Krishnan says is missing.

## §2 — Setup

Notation only. Enough to state §3 and no more.

- Weights: b_i, b'_i (outer), c_i, c'_i (spokes), e_i, e'_i (inner),
  diagonals a_i, d_i. All of b, b', c, c', e, e' nonzero.
- A carries the pattern of P(n,k) iff A_{xy} ≠ 0 exactly on edges, x ≠ y;
  diagonal free. Symmetry **not** assumed.

## §3 — The reduction  *(your `thm:red`, restated for k = 3)*

> Let n ≥ 9. Eliminating the inner coordinates of any matrix A carrying the
> P(n,3) pattern leaves a single linear recurrence of order 8, and
> null A = dim ker(T − I) ≤ 8, with equality iff T = I.

Proof is short and self-contained: solve the u_i row for y_i, substitute into
the v_i row, read off that the extreme coefficients
γ_{i,4} = −e_i b_{i+3}/c_{i+3} and γ_{i,−4} = −e'_{i−3} b'_{i−4}/c_{i−3}
are nonzero, so the recurrence has order exactly 8.

**Hypothesis check:** n ≥ 2k+3 = 9. State it. The theorem is false below it.

This section is the heart of the note and it is unambiguously yours — it is in
tracked history from 3 September.

## §4 — Tiles

- **Dock.** Fix the first and last 4 positions at b = c = e = 1, a = d = 0.
- **Lemma (tile independence).** With a fixed dock at both ends, a tile's
  transfer product depends only on its interior. *(your `lem:tile`)*
- **Theorem (tiling).** If identity tiles exist of every length in [L, 2L),
  then Z(P(n,3)) = M(P(n,3)) = 8 for every n ≥ L. *(your `thm:tiling`)*
  - Proof is three lines: every n ≥ L is a sum of integers from [L, 2L);
    concatenate; the monodromy is the product, hence I.
  - Say why the full interval is needed: two coprime lengths a, b leave every
    n < (a−1)(b−1) uncovered.

## §5 — Certification

- L = **21**. Identity tiles certified for every ℓ with **21 ≤ ℓ ≤ 43**, which
  is **23** tiles and contains [21, 42).
- Method: T_tile = I is a rational equation, but by §3 the monodromy of the
  one-tile cyclic matrix *is* the tile product, so
  T_tile = I ⟺ null A_one-tile = 8, and that is certified by a Krawczyk
  contraction on the bilinear system A(w)K(X) = 0, whose Jacobian is affine.
- Square subsystem chosen **structurally** — K^T A K is symmetric and its
  antisymmetric part accounts for exactly C(8,2) = 28 dependencies.
- Every Krawczyk test evaluated in **exact rational arithmetic**, not float64.
  α ≤ 1.0 × 10⁻⁹ throughout. No step rests on a floating-point nullity.
- Docking weights pinned at their exact integers, so tiles compose.

One short paragraph on reproducibility: `verification/certify_tiles.py`,
one command, exact.

## §6 — Proof of Conjecture 5

Assemble, in this order:

| Range | Source |
|---|---|
| n ≥ 21 | §4 + §5 |
| 17 ≤ n ≤ 20 | per-n certification (`thm:p17`) — 17 certificates, 17 ≤ n ≤ 33 |
| 13 ≤ n ≤ 16 | exhaustive search: no 7-element forcing set exists |
| n = 11, 12 | exhaustive: Z = 7, so **13 is optimal** |

> **Theorem.** Z(P(n,3)) = 8 for every n ≥ 13, and 13 is optimal.
> Moreover Z = M = 8 for every n ≥ 17.

State plainly that this is Conjecture 5 of [Krishnan], and that the ingredient
he names as missing — a lower-bound proof valid for all large n — is §4–§5.

**Be precise about M vs Z.** For 13 ≤ n ≤ 16 you have Z = 8 by exhaustive
search, not M = 8. Do not let Z carry M along.

## §7 — References

Four, maybe five. Rashidi et al. 2020; Krishnan arXiv:2607.19412; AIM minimum
rank group for Z and M; Gera–Stănică if you cite the spectrum. **Write these
yourself** — Rule 8 names AI-generated citations specifically.

---

## Before posting

- [ ] Every sentence is yours.
- [ ] Hypothesis n ≥ 9 stated wherever §3 is used.
- [ ] M and Z distinguished in the 13–16 range.
- [ ] A dated statement of independent work, and that you learned of the Lean
      PR (`the-omega-institute/trureturing` #10129, merged 26 Sep 2026) after
      obtaining the result. Your tracked history: n ≥ 17 on **3 September**,
      k = 3 complete on **22 September**. Decide whether to cite it; if you do,
      state only what you verified yourself about it.
- [ ] Nothing from Part I, and nothing about k ≠ 3, appears anywhere.
