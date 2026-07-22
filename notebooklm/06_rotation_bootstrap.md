# 06 — The rotation bootstrap: how the upper bounds are proved

This file explains how one finite computation becomes a theorem valid for all
sufficiently large n.

## 1. The problem it solves

To prove Z(G) ≤ m for a *single* graph you exhibit a set of size m and run the
colour change rule. But P(n,k) is an infinite family. Running the rule for
every n is impossible. The bootstrap converts one finite check into a statement
about all n in range.

## 2. The two lemmas

### Bootstrap Lemma

> Let ρ be an automorphism of a finite graph G, and let S be a set of vertices
> with ρ(S) ⊆ cl(S). Then ρ(cl(S)) = cl(S).

**Proof.** Closure commutes with automorphisms, and is monotone and idempotent
(file 04). So

    ρ(cl(S)) = cl(ρ(S)) ⊆ cl(cl(S)) = cl(S).

So ρ maps cl(S) into itself. But ρ is a permutation of the finite vertex set,
so ρ(cl(S)) and cl(S) have the same number of elements. A subset of the same
finite size must be the whole thing, so ρ(cl(S)) = cl(S). ∎

The finiteness step is the one people skip. On an infinite graph the lemma is
false — an injective self-map of an infinite set need not be onto.

**What it buys you.** cl(S) is ρ-invariant. So if cl(S) contains even one
vertex, it contains that vertex's entire ρ-orbit. Since ρ is the rotation and
the orbit of any outer vertex is *all* outer vertices, getting one outer vertex
into the closure gets you all of them.

### Closing Lemma

> Let G be cubic with vertices split as O ⊔ I, such that every vertex of I has
> exactly one neighbour in O, every vertex of O has exactly one neighbour in I,
> and the other two neighbours of each vertex of O lie in O. If O ⊆ cl(S) then
> cl(S) = V(G).

**Proof.** Suppose some w ∈ I is still white, and let o ∈ O be its unique
neighbour in O. The other two neighbours of o lie in O, hence are black. So w
is the *unique* white neighbour of the black vertex o, and is forced. ∎

In P(n,k), O is the outer vertices and I the inner ones: each inner vertex has
exactly one spoke, each outer vertex has exactly one spoke, and an outer
vertex's other two neighbours are outer. So once the whole outer cycle is
black, everything else falls for free.

## 3. The recipe

To prove an upper bound for a whole family:

1. Write down a candidate set S, described uniformly in n.
2. Verify by an **explicit finite forcing chain** that ρ(S) ⊆ cl(S).
3. Bootstrap Lemma ⇒ cl(S) is ρ-invariant, so it contains the full outer orbit.
4. Closing Lemma ⇒ cl(S) = V.
5. Conclude Z(G) ≤ |S| for **every** n in range.

Step 2 is the only work, and it is a bounded computation independent of n.

## 4. The I-graph theorem

> **Theorem.** For all j, k ≥ 1 and n ≥ 2(j+k)+1, Z(I(n,j,k)) ≤ 2(j+k).

**Proof sketch.** Put m = 2(j+k) and S = {u_0, ..., u_(m−1)} — m consecutive
outer vertices. Since n ≥ m+1 the indices 0..m are distinct mod n.

*Step 1.* The outer neighbours of u_i are u_(i±j), both in S exactly when
j ≤ i ≤ m−1−j. For those i, the spoke neighbour v_i is the unique white
neighbour of u_i, so it is forced. This fills v_j, ..., v_(j+2k−1).

*Step 2.* Look at v_(j+k). Its neighbours are u_(j+k) ∈ S, v_j (filled in
step 1), and v_(j+2k) (not filled — step 1 stopped at index j+2k−1). So
v_(j+k) forces v_(j+2k).

*Step 3.* Look at u_(j+2k) = u_(m−j). Its neighbours are u_(2k) ∈ S, the
vertex v_(j+2k) just filled, and u_m, which is white. So u_(j+2k) forces u_m.

Hence ρ(S) = {u_1, ..., u_m} ⊆ cl(S). Apply the two lemmas. ∎

**Corollary.** Taking j = 1 gives **Z(P(n,k)) ≤ 2k+2** for n ≥ 2k+3. This is
the upper bound the whole project is trying to match from below.

Every step of the chain was verified by computer for 1 ≤ j ≤ 4, 1 ≤ k ≤ 5 and
six values of n per pair — 106 cases.

### An important scope caveat

This should **not** be read as 2(j+k) new bounds. If gcd(n,j) = 1 then
I(n,j,k) ≅ P(n, j⁻¹k), so those graphs are generalized Petersen graphs and the
corollary already covered them. The genuinely new content is confined to
gcd(n,j) > 1, and in that regime the bound is usually far from sharp —
I(20,5,8) has Z = 10 against a bound of 26. The project originally overstated
this and now says so.

## 5. The DP theorem

> **Theorem.** For all k ≥ 1 and n ≥ 2k+3, Z(DP(n,k)) ≤ 4k+4.

Take S = {u_0, ..., u_(2k+1)} ∪ {x_0, ..., x_(2k+1)}, so |S| = 4k+4, and run a
three-step chain symmetric in the two halves. Here ρ has *two* orbits on the
outer set, and the closure meets both, so the lemmas still close the argument.

No zero forcing results for DP(n,k) appear in the literature; the family is
studied for Hamiltonicity, super-connectivity and automorphisms. The bound is
attained (so sharp) at k = 1 and k = 2.

## 6. The critical observation for later

The forcing set produced by the bootstrap for P(n,k) is

    { u_0, u_1, ..., u_(2k+1) }  —  2k+2 **consecutive outer vertices**.

Remember that number and that shape. In file 09 an apparently unrelated
computation — eliminating variables from a matrix kernel — produces a recurrence
whose **order is exactly 2k+2**, and the coincidence is not a coincidence: the
order of the recurrence *is* the size of this forcing set. That is what makes
the ceiling of the matrix method equal the upper bound.

## 7. What to take away

- ρ(S) ⊆ cl(S) ⇒ cl(S) is ρ-invariant (needs finiteness).
- Fill the outer cycle and the inner vertices follow automatically.
- One finite forcing chain ⇒ a bound for all n in range.
- Z(P(n,k)) ≤ 2k+2, witnessed by 2k+2 consecutive outer vertices.
