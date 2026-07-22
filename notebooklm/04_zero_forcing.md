# 04 — Zero forcing: the colour change rule, closure, Z(G), and forts

## 1. The rule

Colour some vertices of a graph black; the rest are white. Then repeat:

> **Colour change rule.** If a black vertex has **exactly one** white
> neighbour, that white neighbour becomes black.

Apply it until no move is available. The result is the **closure** of the
starting set S, written cl(S). If cl(S) is the whole vertex set, S is a **zero
forcing set**. The **zero forcing number** Z(G) is the size of the smallest
zero forcing set.

### Why "exactly one"

This is the whole subtlety. A black vertex with two white neighbours does
nothing — it cannot decide which one to force. A black vertex with zero white
neighbours does nothing either, having nothing to do. Only the exactly-one case
acts. Think of it as a rumour that can only be passed when there is exactly one
person left who has not heard it: with two listeners the message is ambiguous
and stalls.

## 2. Small examples

**Path on 4 vertices** a–b–c–d. Start with S = {a}. a is black and has exactly
one white neighbour, b, so b becomes black. Now b has exactly one white
neighbour c (a is already black), so c goes black, then d. So {a} forces
everything and Z(path) = 1. Any single endpoint works.

**Cycle on 4 vertices** a–b–c–d–a. Start with S = {a}. a has two white
neighbours, b and d — stuck immediately. Start with S = {a,b}. Now a has one
white neighbour d, so d goes black; b has one white neighbour c, so c goes
black. Done. Z(cycle) = 2, for any cycle.

**Complete graph K_n.** Every vertex is adjacent to all others. A black vertex
has one white neighbour only when exactly one vertex remains white. So you need
n−1 to start: Z(K_n) = n−1.

These three examples are worth doing by hand; they build the right intuition
that Z measures how "spread out and pinned down" you need to start.

## 3. Properties of closure

Three facts, all easy but all used:

1. **Monotone.** If S ⊆ T then cl(S) ⊆ cl(T). More starting information cannot
   hurt.
2. **Idempotent.** cl(cl(S)) = cl(S). Once you have run the process to a halt,
   running it again does nothing.
3. **Commutes with automorphisms.** If σ is an automorphism of G then
   cl(σ(S)) = σ(cl(S)). A symmetry of the graph cannot tell the difference
   between a set and its image, so it cannot tell the difference between their
   closures.

Property 3 is what makes the rotation bootstrap of file 06 work.

## 4. Upper bounds are easy; lower bounds are hard

To prove **Z(G) ≤ m**: exhibit one set of size m and run the rule. That is a
finite, checkable, constructive act.

To prove **Z(G) ≥ m**: you must show that **every** set of size m−1 fails.
There are C(N, m−1) such sets, and no obvious structure to exploit. This
asymmetry is the whole difficulty of the subject, and it is why the open
problem this project attacks is a *lower bound* problem.

Exhaustive search is possible for small graphs — the project's solver does
exactly this, with bitmask closure and symmetry reduction — but it cannot prove
anything for all n.

## 5. Forts: the combinatorial dual

A **fort** is a nonempty set F of vertices such that every vertex outside F has
either 0 or at least 2 neighbours inside F.

**Why a fort is unbreakable.** Suppose all of F is white and some outside
vertex u is black. For u to force into F it would need exactly one white
neighbour. But u has either no neighbours in F (so it cannot reach F at all) or
at least two (so it is paralysed by ambiguity). Either way F is never
penetrated from outside. So no set disjoint from F can be zero forcing.

**Duality theorem.** S is a zero forcing set **if and only if** S intersects
every fort. So Z(G) is a **minimum hitting set** over the collection of forts,
and computing Z becomes an integer program.

That reformulation is appealing but, for this family, it does not deliver:

- **Disjoint forts.** t pairwise disjoint forts force Z ≥ t. But in P(n,k) the
  forts found have 7–13 vertices in a graph with only 2n ≤ 56, and a search
  found at most **two** disjoint forts in every case tested. The certificate
  simply cannot exist at those sizes.
- **The fort LP.** Relaxing the hitting-set integer program to a linear program
  gives a computable lower bound. Here the integrality gap is about **2** —
  LP = 3.21 against Z = 10 for P(18,4) — and it widens with k. (As a side
  benefit this explains why fort-based exact solvers converge slowly on this
  family: branch and bound has to close a factor-2 gap by branching.)
- **Spectral.** A Hoffman-type eigenvalue bound gives values between 1.2 and
  2.9 against true Z of 6–12.

All three fail **in principle**, not merely in practice, and all three degrade
as k grows. That is what motivated abandoning combinatorial lower bounds
entirely and switching to matrices (file 05).

## 6. Known values for this family

- Z(P(n,2)) = 6 for n ≥ 10 (published 2020).
- Z(P(n,3)) = 8 for n ≥ 13. A published 2020 theorem claimed this for n ≥ 12,
  but it is **false**: Z(P(12,3)) = 7. The flawed case analysis never excluded
  7-vertex sets. A July 2026 correction note fixed it and closed by recording
  that determining Z(P(n,k)) for general k — the stabilization threshold and a
  rigorous lower bound for k ≥ 4 — **remains open**.
- The general upper bound is Z(P(n,k)) ≤ 2k+2 (file 06).

The sequences are **not monotone** in n. For k = 6 the values go 6, 8, 8, 10,
10, 12 along coprime n, while the gcd = 2 class reaches 14 at n = 28 and the
coprime class has only reached 12 by n = 29. So extrapolating from a run of
equal values is unsafe, and one of this project's own conjectures was refuted
exactly that way.

## 7. Why anyone cares about Z(G)

Two independent origins:

- **Quantum control.** Whether a spin network can be controlled from a subset
  of sites reduces to a forcing condition on the interaction graph.
- **Power networks.** Placing phase measurement units to observe an entire
  electrical grid is a closely related domination/forcing problem.

And mathematically: Z(G) bounds the **maximum nullity** of the graph, which is
the subject of file 05, and is the reason the parameter is studied at all in
combinatorial matrix theory.

## 8. What to take away

- Force only when a black vertex has exactly one white neighbour.
- cl(S) is monotone, idempotent, and commutes with automorphisms.
- Upper bounds: exhibit a set. Lower bounds: rule out all sets — hard.
- Forts give an exact dual characterisation, but disjoint forts, the fort LP
  and spectral bounds all fail on P(n,k).
