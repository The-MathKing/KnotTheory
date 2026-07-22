# 03 — Graphs, cubic graphs, and the three families

## 1. Basic vocabulary

A **graph** G is a set of **vertices** V and a set of **edges** E, each edge
joining two distinct vertices. Two vertices joined by an edge are
**neighbours** or **adjacent**. The **degree** of a vertex is its number of
neighbours. N[u] denotes the **closed neighbourhood**: u together with its
neighbours.

A graph is **cubic** (or 3-regular) if every vertex has degree exactly 3. Every
graph in this project is cubic — a useful uniformity, since it means every
vertex equation has exactly four terms (itself plus three neighbours).

A **cycle** of length L is L vertices joined in a closed loop.

An **automorphism** is a relabelling of the vertices that maps edges to edges —
a symmetry of the graph. The graphs here all carry a **rotation** automorphism.

## 2. The adjacency matrix

Index the vertices 1..N. The **adjacency matrix** has a 1 in position (u,v)
when uv is an edge and 0 otherwise. It is symmetric, and its diagonal is zero.

The adjacency matrix is one particular member of the family "matrices carrying
the pattern of G" described in file 02 — the member with all edge weights 1 and
all diagonal entries 0. Keep it in mind: one of the main results of this
project turns out to be a statement about the adjacency matrix itself.

## 3. The generalized Petersen graph P(n,k)

Fix n and k with 2k < n. P(n,k) has **2n vertices**:

- **outer** vertices u_0, u_1, ..., u_(n−1)
- **inner** vertices v_0, v_1, ..., v_(n−1)

and three kinds of edges:

- **outer edges** u_i — u_(i+1), forming one n-cycle (indices mod n);
- **inner edges** v_i — v_(i+k), the "skip-k" edges;
- **spokes** u_i — v_i, one per index.

Every vertex has degree 3: an outer vertex has two outer neighbours and one
spoke; an inner vertex has two inner neighbours and one spoke. So P(n,k) is
cubic on 2n vertices.

P(5,2) is the famous **Petersen graph**. P(n,1) is a prism.

### Picture it

Draw a big circle of n dots (the outer cycle), and a smaller concentric circle
of n dots (the inner vertices). Join each outer dot to the inner dot directly
beneath it — those are the spokes. On the inner circle, instead of joining
neighbours, join each dot to the one k steps around. For k = 2 you get a
pentagram-like star; for larger k, a denser star.

### The inner structure is gcd, exactly as in file 01

The inner edges join i to i+k. By the clock fact, they decompose the inner
vertices into **gcd(n,k) separate cycles**, each of length n/gcd(n,k). So:

- if gcd(n,k) = 1, the inner vertices form a single n-cycle (visited in a
  scrambled order);
- if gcd(n,k) = d > 1, they form d disjoint cycles.

This is why gcd(n,k) keeps appearing in the data. For example the exact values
of Z(P(n,6)) sort cleanly by gcd(n,6) into four separate families, each of
which climbs on its own schedule.

## 4. The rotation

Define ρ by ρ(u_i) = u_(i+1) and ρ(v_i) = v_(i+1), all indices mod n. This maps
outer edges to outer edges, inner edges to inner edges, and spokes to spokes,
so it is an automorphism. It has order n, and its orbits on the outer vertices
form the single set {u_0, ..., u_(n−1)}.

ρ is the reason everything in this project works. It is used twice, in two
completely different ways:

1. **Combinatorially** (file 06): if a starting set S "reproduces itself one
   step rotated", then by symmetry it fills the whole graph. This converts one
   finite check into a statement for all n.
2. **Algebraically** (file 07): a matrix commuting with ρ can be
   block-diagonalised by Fourier analysis into n tiny 2×2 blocks.

## 5. The I-graphs I(n,j,k)

Generalise by also letting the outer cycle skip:

- outer edges u_i — u_(i+j)
- inner edges v_i — v_(i+k)
- spokes u_i — v_i

So P(n,k) = I(n,1,k). Now the outer vertices form gcd(n,j) cycles and the inner
ones gcd(n,k) cycles.

**Scope warning.** If gcd(n,j) = 1, multiplying all indices by the inverse of j
mod n is an isomorphism I(n,j,k) ≅ I(n,1,j⁻¹k) = P(n, j⁻¹k). So in the coprime
case the I-graphs are not new objects, they are generalized Petersen graphs in
disguise. Genuinely new content only appears when gcd(n,j) > 1. This project
originally overstated the reach of its I-graph theorem for exactly this reason,
and the paper now says so explicitly.

## 6. The double generalized Petersen graphs DP(n,k)

4n vertices: two outer cycles u_i and x_i, and inner vertices w_i and y_i, with

- outer edges u_i — u_(i+1) and x_i — x_(i+1)
- inner edges w_i — y_(i+k) and y_i — w_(i+k)  (note the cross-pairing)
- spokes u_i — w_i and x_i — y_i

Also cubic. The literature studies DP(n,k) for Hamiltonicity and connectivity,
but no zero forcing results existed for it before this project.

## 7. Why this family is a good research target

- It is an **infinite family with a parameter**, so a result can be a theorem
  rather than a table.
- It has a **nontrivial symmetry group**, which gives you leverage.
- It is **sparse and cubic**, so the linear algebra stays small and structured.
- There is a **specific, recently stated, attributed open problem** about it.
- It is small enough that exhaustive computation is possible for moderate n,
  so conjectures can be tested rather than guessed at.

## 8. What to take away

- P(n,k): 2n vertices, outer cycle, skip-k inner edges, spokes; cubic.
- Inner edges split into gcd(n,k) cycles — the clock fact from file 01.
- The rotation ρ is used both combinatorially (upper bounds) and algebraically
  (lower bounds).
- I(n,j,k) is only genuinely new when gcd(n,j) > 1.
