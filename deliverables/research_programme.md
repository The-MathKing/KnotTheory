# A research programme toward a category-changing result

> **Status, 1 October 2026 — the target statement of this programme is false.**
> The regular-base ceiling (§"Statement to prove") fails on the $K_4$ family
> this document proposed as its prize: the zero-voltage edges of that base form
> a triangle, a rank-one block on each triangle fibre gives
> $\operatorname{null}A\ge n$ against $D=6$ (exact over $\mathbb Q$,
> $n=4,\dots,10$; `verification/k4_rank_one.py`), so $M\ge n$ and the gap to
> $Z=n+2$ is at most $2$. The "unconditional" equivariant statement was also
> false: `thm:cover` needs $\det M(\zeta)\not\equiv0$. Route 3 below was
> wrong — regularity controls only the independent-set case of the general
> obstruction $M(G)\ge|V|-\operatorname{mr}(G[S])-2|V\setminus S|$. The
> replacement hypothesis is the leading-coefficient criterion (`conj:leading`
> in the paper): the top coefficient of $\det M(\zeta)$ is a monomial in edge
> weights. Everything below is kept as the record of a programme that failed,
> and of how. See `external_assessment.md` §2 and log Entry 35.


**Written for:** you, and whoever you eventually show this to as a mentor. It
assumes the contents of `zf_paper.tex` and nothing else.

**What this is.** Six times you have asked what would lift this project into
first-place territory, and six times the honest answer has been "not more
polish." This document is the attempt to answer it properly: what the field
actually considers open, where this project's machinery touches it, and which
single theorem would change the category of the result. It ends with a concrete
attack and an honest estimate of whether it will close.

---

## 1. The honest starting position

What you have, as a referee would grade it:

| Asset | Referee's likely verdict |
|---|---|
| Monodromy ceiling: $\operatorname{null}A \le 2k+2$ for **every** $A\in\mathcal S(P(n,k))$ | The best thing in the paper. A structural statement about the *method*, not the family. |
| $Z=M=2k+2$ for all $n$ at $k=2,3,4$; Rashidi et al. corrected; Krishnan's Conjecture 5 proved | Solid, citable, publishable. Closes attributed gaps. |
| Corner criterion, Dirichlet bound, complete Ramanujan classification | A complete classification of a recognised genre. A note, not a breakthrough. |
| `thm:redpath`, `thm:redcycle`, `thm:cexcover` | Careful. The refutation is of *your own* stated conjecture, not the literature's. |
| 126 certified checks, exact arithmetic throughout | Unusual rigour. Methodology, not mathematics. |

The honest summary: **two publishable notes, about one family.** Everything is
correct and almost nothing is surprising. The category change requires a theorem
that is about a *class of objects* and that answers something the field has
already asked.

---

## 2. What the field has actually asked

Sources at the end. The minimum rank / inverse eigenvalue problem programme
(AIM workshop 2006, and the Fallat–Hogben surveys you already cite as `[FH]`)
has two named conjectures and one standing question.

**Delta conjecture.** $M(G) \ge \delta(G)$ for every graph. Open since 2006.
Known for trees, bipartite graphs, and every graph with $\delta(G)\le3$.

**Graph Complement Conjecture (GCC).** $\operatorname{mr}(G)+\operatorname{mr}(\overline G)\le |G|+2$.
Open, with strengthenings in terms of $\operatorname{mr}^+$ and the Colin de
Verdière parameter $\nu$.

**The $M$ versus $Z$ question.** $M(G)\le Z(G)$ always, and *a full
classification of the graphs with $M(G)=Z(G)$ is open.* The survey literature
asks, in substance: what are sufficient conditions for $M(G)<Z(G)$, and **is
there a graph parameter $Y$ with $M(G)\le Y(G)<Z(G)$** that explains the gap?

That last question is the one your machinery is built to answer, and you did not
know it was being asked.

### Where the cubic case stands

This matters because every cover in your paper is cubic.

- Akbari, Vatandoost and Golkhandy Pour (arXiv:1705.09773) characterise all
  cubic graphs with $Z(G)=3$ and show $M(G)=3$ there; they exhibit a family with
  $M(G)=Z(G)=4$.
- The companion subcubic paper (arXiv:1903.08614) characterises graphs of
  maximum degree $\le3$ with forcing number $3$.

So the published cubic landscape reaches $Z=3$ and $Z=4$. **Your exact values at
$Z=M=6,8,10$ for infinite families are already past the literature.** That is
worth knowing and worth saying.

### The gap in the known separations

Every well-documented graph with $M(G)<Z(G)$ in the literature is tree-like —
the Barioli–Fallat tree and a 16-vertex graph derived from it. **No regular
example, and no cubic example, appears in the standard sources.**

---

## 3. The target

> **Programme A.** Prove the cover ceiling for **regular** bases. Deduce an
> exact formula for maximum nullity on an infinite family of cubic graphs. Use
> it to exhibit cubic graphs with $M(G)<Z(G)$, with the gap explained by a
> computable parameter.

### Statement to prove

Let $B$ be a connected regular base with voltages in $\mathbb Z_n$, let
$D=D(B)$ be the degree span of $\det M(\zeta)$, and let $A\in\mathcal S(B^n)$
have all edge weights nonzero. Then
$$\operatorname{null}A \;\le\; D .$$

Combined with the construction already in the paper (prescribing $D/2$ interior
grid values gives nullity exactly $D$), this yields $M(B^n)=D$ — an exact
maximum nullity, read off the base's voltages by a determinant.

### Why this is the category change

1. **It is a theorem about a class**, not a family. "The maximum nullity of a
   cyclic cover of a regular base equals the degree span of its symbol" is a
   sentence about cyclic covers. $P(n,k)$ becomes a corollary.
2. **It answers the field's standing question.** $D$ is the parameter $Y$: it is
   computed from the base alone, it bounds $M$, and where $Z>D$ it *explains*
   the gap rather than merely exhibiting it.
3. **It produces cubic separations, which appear to be unknown.** And not just
   one — the evidence suggests an infinite family with **unbounded** gap.

### The evidence already in hand

Exhaustive $Z$ (exact, by subset search) against $D$ (symbolic, from voltages),
on connected cubic covers:

| cover | $n$ | $\lvert V\rvert$ | $D$ | $Z$ | |
|---|---|---|---|---|---|
| theta$(0,1,2)$ | 4–9 | 8–18 | 4 | 4 | $Z=D$ throughout |
| theta$(0,1,3)$ | 7,8,9 | 14–18 | 6 | 6 | $Z=D$ once $n$ is large enough |
| $P(n,2)$ two-loop | 7,9 | 14,18 | 6 | 6 | $Z=D$ |
| **$K_4$** | 4 | 16 | 6 | 6 | $Z=D$ |
| **$K_4$** | 5 | 20 | 6 | **7** | $Z-D=+1$ |
| **$K_4$** | 6 | 24 | 6 | **8** | $Z-D=+2$ |

$D$ is constant in $n$; on the $K_4$ base $Z$ grows. A nullity-$6$ matrix was
found on the $n=6$ cover ($\sigma$-residual $3\times10^{-18}$), so $M\ge D=6$
there. **If the ceiling holds, $M=6$ while $Z=8$ — a cubic graph with a strict
gap — and the gap grows with $n$.**

That last clause is the prize: an infinite family of cubic graphs with $M$
bounded and $Z$ unbounded, i.e. $Z-M\to\infty$, with an exact formula for $M$.

### Why the hypothesis is *regular* and not something else

Because the irregular cases are already refuted, by you:

- A base vertex of degree 1 lifts to **pendant** vertices; the diagonal is free
  in $\mathcal S(G)$, so zeroing it forces the neighbour to vanish and frees a
  parameter per fibre index. On the star-with-a-loop base,
  $\operatorname{null}A=n$ against $D=2$ (`thm:cexcover`).
- Minimum degree 2 does not repair it: $K_{2,3}$ gives $6$ against $D=4$
  (`rem:mindeg`).
- Every regular base attacked — $C_3$, theta, 4-theta, two-loop, $K_4$,
  $K_{3,3}$, prism — survives both the diagonal-zeroing construction and a
  gradient search.

So the hypothesis is not a guess fitted to success; it is what is left after two
exact counterexamples.

---

## 4. How to attack it

Four routes, in the order I would try them.

### Route 1 — The difference system on $\mathbb Z$ (most likely to work)

This is the frame `thm:red2`, `thm:redpath` and `thm:theta` already use, made
general. Lift the cover to $B^{\mathbb Z}$ with $n$-periodic coefficients. Then
$$\ker A \;\cong\; \{\text{$n$-periodic solutions of a difference system on }\mathbb Z\},$$
the monodromy $T$ over one period acts on the solution space, and $\ker A$ is
its fixed space. **If the solution space has dimension $D$, the theorem
follows.**

So the whole problem is: *show the system reduces to order $D$.* For constant
coefficients this is classical — the solution space of $P(S)x=0$ has dimension
equal to the degree span of $\det P$. For $n$-periodic coefficients the
corresponding statement is what must be established.

The technical obstacle is real and worth naming: the natural ring here —
diagonal matrices together with the cyclic shift — is **not a domain** (it is
all of $M_n(\mathbb C)$), so Ore/Jacobson normal-form theory does not apply off
the shelf. The repair is that your hypothesis makes the relevant coefficients
*nowhere zero*, hence units, so Gaussian elimination over the skew polynomial
ring $R_0[S;\sigma]$ can be carried out provided every pivot's leading
coefficient is nowhere vanishing. **That condition is where regularity must
enter, and finding out why is the mathematical heart of the programme.**

### Route 2 — Injectivity on a window

Equivalent reformulation, already isolated in
`verification/cover_ceiling_sharp.py`: the theorem holds iff no nonzero kernel
vector vanishes on $D$ suitably chosen coordinates. This is the same shape as
the standard proof of $M(G)\le Z(G)$ via zero forcing, and it converts an
analytic question into a combinatorial one about which $D$ coordinates form a
determining set. Worth pursuing in parallel because it may be easier to see
where regularity bites.

### Route 3 — Understand the counterexamples structurally

Both refutations work by *spending* a vertex's equation to annihilate a
neighbour: a pendant row reads $w\,x_u=0$, a degree-2 row with zero diagonal
reads $a x_u + b x_w = 0$. In a regular base of degree $d$, every row has $d$
off-diagonal terms and no row can be spent so cheaply. Make that precise and it
may *be* the proof. This is the cheapest thing to try and should be done first.

### Route 4 — Specialisation

Prove the bound off a proper algebraic subset of weight space, then handle the
closed locus. **Flagged as a trap:** nullity is maximised precisely on special
loci, so a generic statement misses the entire question. Do not spend time here
unless Routes 1–3 all stall.

---

## 4a. Status — what has since been executed

Everything in §5 items 1–3 and 5 is **done**. What follows is the record; §5 is
left in place as written so the plan and the outcome can be compared.

**Route 3 closed, and it was short.** Both counterexamples work by *spending* a
row. The general form: let $S$ be an independent set and zero the diagonals on
$S$. Each row at $v\in S$ reduces to $a_{vv}x_v=0$ (every neighbour of $v$ lies
outside $S$), which holds identically; each row at $u\in N(S)$ becomes one
relation on $x|_S$. So vectors supported on $S$ are cut out by $|N(S)|$
conditions on $|S|$ coordinates:

> **Proposition.** For any independent set $S$, $\;M(G)\ge|S|-|N(S)|$.

On the star-with-a-loop cover, $S$ = the two pendant fibres gives $2n-n=n$ —
*exactly* the nullity exhibited. On $K_{2,3}$, $3n-2n=n$ against $D=4$.

> **Corollary.** If $G$ is $d$-regular then $|N(S)|\ge|S|$ for every independent
> $S$, so the obstruction is vacuous.

Proof: $S$ independent, so all $d|S|$ edges from $S$ land in $N(S)$, and each
vertex there absorbs at most $d$; hence $d|S|\le d|N(S)|$. Verified on 17,342
(regular graph, independent set) pairs with no violation.

**That is why the hypothesis is regularity and not minimum degree.** $K_{2,3}$
has minimum degree 2 and three fibres neighbouring only two. A regular base has
no such set at any degree. Both statements are now in the paper as
`prop:indobs` and `cor:regblocks`. This rules out one mechanism, not all of
them — it is not the ceiling — but it explains every counterexample found and
pins the hypothesis.

**The evidence table extended, by CP-SAT with optimality proved.** On the $K_4$
base, $D=6$ for every $n$ while

| $n$ | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|
| $\lvert V\rvert$ | 16 | 20 | 24 | 28 | 32 |
| $Z$ | 6 | 7 | 8 | 9 | 10 |
| $Z-D$ | 0 | +1 | +2 | +3 | +4 |

so $Z=n+2$ and the gap grows linearly.

**An exact certificate at the span.** $\det M(\zeta)$ is palindromic, hence a
cubic in $x=\zeta+\zeta^{-1}$; the minimal polynomial of $2\cos(2\pi/7)$ is
also a cubic. Matching them forces all four coefficients of
$\zeta^3\det M$ equal, which with equal edge weights means $d_0=d_1=d_3=:t$ and
$d_2=(3t+4)/((t-1)(t+2))$. At $t=2$, scaling by 2 clears the denominator:
**every edge weight 2, diagonals $(4,4,5,4)$**, an integer matrix whose symbol
is $16(\zeta^7-1)/(\zeta-1)$ — vanishing at all six primitive 7th roots of
unity. Exact rank over $\mathbb Z$ confirms nullity $6=D$ at $n=7$ and $n=14$.
This is `prop:k4cert`; the $Z$ values are `prop:k4z`; both are in
§`sec:gapfamily` with a new `conjecture`.

**What is now unconditional.** `thm:cover` bounds every *equivariant* matrix by
$D=6$, and the certificate attains it. So the equivariant maximum nullity is
exactly 6 while $Z=n+2$: the gap between $Z$ and anything a rotation-invariant
certificate can reach is $n-4$, unbounded, with no conjecture involved. The
conditional part is only the step from equivariant to all matrices.

**Still open, and now the single remaining step:** the regular-base ceiling.
With it, $M=6$ and $Z-M=n-4\to\infty$ on cubic graphs.

**The expert email** has been rewritten to lead with this rather than with the
ceiling theorem alone, and now asks two questions: is the ceiling new, and is a
cubic family with bounded $M$ and unbounded $Z$ known.

---

## 5. What to do first, in order

1. **Route 3, on paper, this week.** Write out exactly which rows can be spent
   in the two counterexamples, and show a $d$-regular row cannot be. If this
   works it is short, and it would be the whole theorem.
2. **Extend the evidence table.** Compute $Z$ for the $K_4$ cover at $n=7,8$
   (28, 32 vertices — needs a better forcing solver than exhaustive subsets;
   an ILP or the existing CP-SAT path in `crossvalidate_z.py` will do). If
   $Z$ keeps growing while $D$ stays at 6, the unbounded-gap claim firms up.
3. **Certify one nullity-$D$ witness exactly** on the $K_4$ cover at $n=6$,
   using the Krawczyk machinery already in the repo. That upgrades $M\ge6$ from
   numerical to certified, which matters because half the claim rests on it.
4. **Then** attempt Route 1 properly, with Route 2 as the cross-check.
5. **Send the expert email** (`email_expert_review.md`) revised to lead with
   this programme rather than with the ceiling theorem alone. A resolved
   conjecture plus a candidate answer to a standing question is a far better
   reason for a researcher to spend an hour.

---

## 6. Two alternative programmes, and why they rank lower

**Programme B — the delta conjecture on covers.** If the ceiling gives $M=D$
exactly, then $M\ge\delta$ on covers reduces to $D\ge\deg(B)$, a voltage
computation. *Lower value:* the delta conjecture is already known for
$\delta\le3$, and your covers are cubic, so the interesting cases ($d\ge4$) are
a side road rather than the main result.

**Programme C — extend the Ramanujan classification.** Push the corner criterion
to $(q+1)$-regular covers for $q+1\ge4$, or to non-cyclic abelian covers.
*Lower value:* the genre is established, the answer shape ("only finitely many")
is predictable from the abelian-covers-do-not-expand principle, and the result
would be another note rather than a theorem about a class.

---

## 7. Honest risk assessment

**This may not close.** Route 1 is a genuine research problem; the ring-theoretic
obstacle is real and I do not know that regularity resolves it. Weeks to months,
not sessions, and it may simply not work.

**What you keep if it fails.** The refutation and the two positive theorems
stand regardless — they are already written and certified. The evidence table is
publishable on its own as "cyclic covers with $Z-M$ apparently unbounded,
conditional on the ceiling." And the programme itself, written up honestly as a
conjecture with evidence and a stated obstruction, is a legitimate thing to put
in a paper and to show a judge: *this is what I think is true, here is why, here
is exactly where I am stuck.*

**What it costs you if it succeeds.** More material to own. Every theorem added
is another derivation you must be able to produce cold at a table. Weigh that
honestly against the gain — it is the reason §5 puts the one-week paper attempt
first and the open-ended proof attempt fourth.

**The two items this does not touch** remain the provenance statement and the
emails, and they are still the binding constraints on everything else.

---

## Sources

- [Variants on the minimum rank problem: A survey II](https://arxiv.org/pdf/1102.5142) — Fallat & Hogben; delta conjecture, GCC, and the state of the programme. Already cited in your paper as `[FH]`.
- [Maximum nullity and zero forcing number on cubic graphs](https://arxiv.org/abs/1705.09773) — Akbari, Vatandoost, Golkhandy Pour; cubic $Z=3$ characterisation, $M=Z=4$ family.
- [Maximum Nullity and Forcing Number on Graphs with Maximum Degree at most Three](https://arxiv.org/abs/1903.08614) — subcubic forcing number 3.
- [Zero forcing parameters and minimum rank problems](https://www.sciencedirect.com/science/article/pii/S0024379510001278) — the $M$ vs $Z$ question and the search for an intermediate parameter.
- [Zero forcing sets and the minimum rank of graphs](https://people.math.ethz.ch/~sudakovb/zero-forcing-sets.pdf) — AIM Minimum Rank Special Graphs Work Group; the original $M\le Z$ bound.
