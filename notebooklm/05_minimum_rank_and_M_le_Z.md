# 05 — Maximum nullity, and the inequality M(G) ≤ Z(G)

This file contains the single most important proof in the subject. Everything
the project does for lower bounds rests on it.

## 1. The matrix family of a graph

Let G be a graph on vertex set V. Define

    S(G) = { A real symmetric, indexed by V, with
             A_(u,v) ≠ 0 exactly when uv ∈ E(G), for u ≠ v;
             diagonal entries arbitrary }.

So A is forced to have a nonzero entry on every edge, forced to have a zero
entry on every non-edge, and is completely free on the diagonal.

Define the **maximum nullity**

    M(G) = max { nullity(A) : A ∈ S(G) },

and the **minimum rank** mr(G) = |V| − M(G). Determining mr(G) for all graphs
is the "minimum rank problem", a long-standing question in combinatorial matrix
theory.

## 2. The theorem

> **Theorem.** M(G) ≤ Z(G).

### Proof

Let S be any zero forcing set, and let A be any matrix in S(G). Take x ∈ ker A
with x vanishing on S — that is, x_w = 0 for every w ∈ S. We show x = 0
everywhere.

Claim: x vanishes on cl(S). Induct along the forcing process. Suppose x already
vanishes on a set B, and suppose u ∈ B is a black vertex with exactly one white
neighbour w (so all of u's other neighbours, and u itself, lie in B).

Look at row u of the equation Ax = 0:

    A_(u,u) x_u  +  Σ over neighbours v of u of  A_(u,v) x_v  =  0.

Now examine each term:

- A_(u,u) x_u = 0, because u ∈ B so x_u = 0.
- For each neighbour v ≠ w: v ∈ B, so x_v = 0, so the term vanishes.
- That leaves exactly one surviving term, A_(u,w) x_w.

So A_(u,w) x_w = 0. And A_(u,w) ≠ 0, **because uw is an edge of G and A lies in
S(G)**. Therefore x_w = 0.

That is precisely one application of the colour change rule. Repeating it along
the whole forcing process, x vanishes on cl(S) = V, so x = 0.

Now consider the linear map ker A → R^S sending x to its restriction x|_S. We
have just shown this map is **injective**: only the zero kernel vector restricts
to zero. An injective linear map cannot increase dimension, so

    nullity(A) = dim(ker A) ≤ dim(R^S) = |S|.

This holds for every A ∈ S(G) and every zero forcing set S, so
M(G) ≤ Z(G). ∎

### Where each hypothesis is used

Notice the proof uses exactly one property of A: **A_(u,w) ≠ 0 for every edge
uw**. It never uses the zeros on non-edges, never uses the diagonal, and —
importantly — **never uses symmetry**.

## 3. The non-symmetric generalisation

Because symmetry is unused, the theorem immediately extends. Call A
**combinatorially symmetric** for G if

    A_(u,v) ≠ 0 exactly when uv ∈ E(G), for u ≠ v,

with no requirement that A_(u,v) = A_(v,u); the diagonal is still free. Every
edge carries a nonzero entry in *each* direction, but the two entries may
differ. Write M_cs(G) for the maximum nullity over this larger class. The proof
above goes through verbatim, so

    M(G) ≤ M_cs(G) ≤ Z(G).

**Why this matters practically.** For P(n,k) the symmetric class has 5n free
parameters (n outer edge weights, n spokes, n inner edge weights, 2n diagonals)
while the combinatorially symmetric class has 8n (two per edge instead of one).
Almost doubling the search space costs nothing in rigour. The project searches
both.

**A guardrail learned the hard way.** S(G) sits *inside* the combinatorially
symmetric class. So any search that reports a smaller maximum for the larger
class is broken. That happened during this project — a search reported a
smaller answer for the cs class on P(12,2), which is impossible — and a
conclusion had already been drawn from those numbers before the check caught
it. Seeding the larger search with the symmetric certificate fixed it.

## 4. What a certificate is, and why it is the whole game

To prove **Z(G) ≥ r**, it now suffices to **exhibit one matrix A with the
pattern of G and nullity r**. Nothing has to be ruled out; you produce an
object and check it. That is a completely different kind of task from searching
over all vertex subsets, and it is the reason this route succeeds where the
combinatorial routes of file 04 fail.

Two things must be checked for a claimed certificate:

1. **The pattern is right** — every edge entry nonzero, every non-edge entry
   zero. (A near-zero edge weight is a silent failure; see file 12.)
2. **The nullity really is r** — and for this to be a proof rather than an
   observation, in exact arithmetic.

## 5. Is M = Z in general?

No. M(G) ≤ Z(G) can be strict for general graphs. So the certificate method has
an intrinsic limit: if M(G) < Z(G) for some graph, no matrix certificate can
ever prove the true value of Z(G) for it.

That makes the following question the crux for this project: **how large can
the nullity possibly be for P(n,k)?** If the answer is smaller than 2k+2, the
method is doomed; if it equals 2k+2, the method can in principle settle
everything. File 09 answers it exactly.

## 6. What to take away

- S(G): pattern forced off the diagonal, diagonal free.
- M(G) ≤ Z(G), proved by showing a kernel vector vanishing on a forcing set
  must vanish everywhere — the zero propagates by *exactly* the colour change
  rule.
- Symmetry is never used, so the bound holds for the larger combinatorially
  symmetric class too.
- A lower bound on Z is now an existence problem: build one good matrix.
