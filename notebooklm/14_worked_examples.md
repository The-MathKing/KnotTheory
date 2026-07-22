# 14 — Fully worked examples

Do these by hand. They are the fastest route to understanding.

## Example 1 — forcing on P(9,2), step by step

P(9,2): outer u_0..u_8 in a cycle, inner v_0..v_8 with edges v_i — v_(i+2),
spokes u_i — v_i.

Start with S = {u_0, u_1, u_2, u_3, u_4, u_5} (six consecutive outer vertices;
2k+2 = 6).

**Step 1 — spokes fire.** Consider u_i for 1 ≤ i ≤ 4. Its neighbours are
u_(i−1), u_(i+1) (both in S) and v_i (white). Exactly one white neighbour, so
v_i is forced. Now v_1, v_2, v_3, v_4 are black.

(u_0 does not fire: its neighbours are u_8 — white — and u_1 and v_0, so it has
*two* white neighbours. u_5 likewise has u_6 and v_5 white.)

**Step 2 — an inner vertex fires.** Consider v_3. Its neighbours are u_3 (in S),
v_1 (black from step 1), and v_5 (white). Exactly one white neighbour, so v_3
forces **v_5**.

**Step 3 — back out to the rim.** Consider u_5. Its neighbours are u_4 (in S),
v_5 (black from step 2), and u_6 (white). Exactly one white neighbour, so u_5
forces **u_6**.

Now the closure contains {u_0, ..., u_6} ⊇ ρ(S) = {u_1, ..., u_6}. By the
Bootstrap Lemma the closure is ρ-invariant, so it contains the whole outer
cycle; by the Closing Lemma everything else follows. Hence Z(P(9,2)) ≤ 6.

The same three steps work for every n, which is the point.

## Example 2 — P(24,5), nullity 12, the headline certificate

**Claim.** The plain adjacency matrix of P(24,5) has nullity 12 = 2k+2, so
Z(P(24,5)) = 12.

**The certificate.** a = 0 (outer diagonal), d = 0 (inner diagonal), all edge
weights 1. That is,

    A = [ P + P⁻¹      I       ]
        [    I      P⁵ + P⁻⁵   ]

which is exactly the adjacency matrix.

**Step 1 — the symbol.** With b = e = c = 1 and a = d = 0, the block determinant
is det M_m = s_m t_m − 1. Using t = L_5(s) = s⁵ − 5s³ + 5s:

    F(s) = s · L_5(s) − 1 = s⁶ − 5s⁴ + 5s² − 1.

**Step 2 — factor it.**

    s⁶ − 5s⁴ + 5s² − 1 = (s − 1)(s + 1)(s⁴ − 4s² + 1).

Check the quartic: s⁴ − 4s² + 1 = 0 gives s² = 2 ± √3, so
s = ±√(2+√3) ≈ ±1.93185 and s = ±√(2−√3) ≈ ±0.51764.

**Step 3 — recognise the factors as cyclotomic.**

    s − 1 = Ψ_6   (root 1 = 2cos(2π/6))
    s + 1 = Ψ_3   (root −1 = 2cos(2π/3))
    s⁴ − 4s² + 1 = Ψ_24   (roots 2cos(2πj/24), gcd(j,24) = 1)

Indeed 2cos(2π/24) = 2cos 15° ≈ 1.93185 ✓ and 2cos(10π/24) = 2cos 75° ≈ 0.51764
✓. And lcm(3, 6, 24) = **24**.

**Step 4 — find the m's.** All six roots lie in Γ_24, at indices
m = 1, 4, 5, 7, 8, 11 (check: 2cos(2π·4/24) = 2cos 60° = 1 ✓,
2cos(2π·8/24) = 2cos 120° = −1 ✓). Each is interior (none is ±2), so each
contributes **2**, via m and 24 − m:

    {1, 23}, {4, 20}, {5, 19}, {7, 17}, {8, 16}, {11, 13}   →   12 indices.

**Step 5 — verify directly.** Equivalently, count m with
2cos(2π·6m/24) + 2cos(2π·4m/24) = 1, i.e. 2cos(πm/2) + 2cos(πm/3) = 1:

| m | 2cos(πm/2) | 2cos(πm/3) | sum |
|---|---|---|---|
| 1 | 0 | 1 | **1** ✓ |
| 2 | −2 | −1 | −3 |
| 3 | 0 | −2 | −2 |
| 4 | 2 | −1 | **1** ✓ |
| 5 | 0 | 1 | **1** ✓ |
| 6 | −2 | 2 | 0 |
| 7 | 0 | 1 | **1** ✓ |
| 8 | 2 | −1 | **1** ✓ |
| 9 | 0 | −2 | −2 |
| 10 | −2 | −1 | −3 |
| 11 | 0 | 1 | **1** ✓ |
| 12 | 2 | 2 | 4 |

Six hits in 1..12, each doubling by m ↦ 24 − m: **12**. ∎

**Step 6 — conclude.** nullity(A) = 12, so M(P(24,5)) ≥ 12, so Z(P(24,5)) ≥ 12
by M ≤ Z. The bootstrap gives Z ≤ 2k+2 = 12. Hence **Z(P(24,5)) = 12**, and
M = Z here. The same works for every n divisible by 24.

## Example 3 — P(60,4), nullity 10

Here a = 1, d = −1, c = 1. The symbol is

    F(s) = (s + 1)L_4(s) − s − 2,   L_4 = s⁴ − 4s² + 2,

which expands to s⁵ + s⁴ − 4s³ − 4s² + s, and factors as

    s · (s⁴ + s³ − 4s² − 4s + 1) = Ψ_4 · Ψ_30.

deg Ψ_4 = φ(4)/2 = 1 and deg Ψ_30 = φ(30)/2 = 4, total 5 = k+1 ✓. And
lcm(4, 30) = **60**. Check admissibility: c² = aα − β = (1)(−1) − (−2) = 1 > 0
✓. All five roots are interior, so nullity = 2 × 5 = **10** = 2k+2, giving
Z(P(n,4)) = 10 whenever 60 | n.

## Example 4 — a deliberate failure, and what it teaches

First, the recovery formulas for k = 2. With L_2 = s² − 2,

    F(s) = (s + a)(s² − 2) + α s + β = s³ + a s² + (α − 2)s + (β − 2a),

so matching against a monic cubic s³ + A_2 s² + A_1 s + A_0 gives

    a = A_2,   α = A_1 + 2,   β = A_0 + 2a,

and the admissibility quantity simplifies neatly:

    c² = a α − β = a(A_1 + 2) − (A_0 + 2a) = **A_2 · A_1 − A_0**.

Now take n = 12 and prescribe the three roots s = −√3, −1, 0 (all in Γ_12):

    (s + √3)(s + 1)s = s³ + (1 + √3)s² + √3 s,

so A_2 = 1 + √3, A_1 = √3, A_0 = 0, and

    c² = A_2 A_1 − A_0 = (1 + √3)(√3) = 3 + √3 ≈ 4.73 > 0.

Admissible — this one works, giving nullity 6. (For the record a = 1 + √3,
α = 2 + √3, β = 2 + 2√3.)

Now try the triple s = 0, 1, √3 instead. The cubic is s³ − (1 + √3)s² + √3 s,
so A_2 = −(1 + √3), A_1 = √3, A_0 = 0, and

    c² = A_2 A_1 − A_0 = −(1 + √3)(√3) = −(3 + √3) ≈ −4.73 < 0.

**Rejected.** A negative c² means the spoke weight c would be imaginary; the
matrix is not real, does not lie in S(P(n,k)), and certifies nothing.

**The lesson.** Getting all the roots onto the grid is necessary but **not
sufficient**. Realisability (c² > 0) is a second, independent hurdle, and it
kills many otherwise perfect candidates — including every rational candidate at
k = 3 that would have given nullity 8.

## Example 5 — why k = 3 has no rational certificate

For k = 3 we need Σ deg Ψ_d = 4 with all d ≥ 3. The complete list of
possibilities and their fates:

- D = {3,4,12}: a = 1, α = 0, β = 0 → c² = **0**. Rejected.
- D = {3,6,8}: a = 0, α = 0, β = 2 → c² = **−2**. Rejected.
- D = {3,9}: c² = **0**. Rejected.
- D = {3,14}: c² = **−1**. Rejected.
- D = {5,8}: c² = **−1**. Rejected.
- D = {5,10}: c² = **−1**. Rejected.
- D = {6,7}: c² = **−1**. Rejected.
- D = {8,10}: c² = **−1**. Rejected.
- … and the rest fail the membership test outright.

Every single one fails. That is why k = 3 is "impossible for rational symbols"
in the completeness table — and yet **irrational** symbols do attain 8, at
n = 40 (with a = −√2) and n = 60 (with c² = 1/φ). Rationality is sufficient,
not necessary.

## What to take away

- The forcing chain is three steps and works for all n.
- P(24,5): symbol s·L_5 − 1 factors as Ψ_6Ψ_3Ψ_24, all roots in Γ_24, twelve
  indices, adjacency matrix, done.
- Roots on the grid is necessary; c² > 0 is a separate and often fatal hurdle.
- Rational symbols are sufficient but not necessary.
