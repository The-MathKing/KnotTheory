# Prompt for an independent assessment

**How to use this.** Paste everything below the line into a fresh conversation
with a model that has no context from this project. Do not attach the paper
first — the point is an outside read, and feeding it 60 pages invites agreement
rather than assessment. If it asks for the paper afterwards, send it then.

**One design note, which matters.** §4 of the prompt discloses the AI assistance
honestly. It is tempting to leave that out, because it will lower the assessment.
Leave it in. A plan built on a false picture of how the work was produced is
worth nothing, and the thing you most need an outside view on is precisely
whether that changes what you should do.

---

You are assessing a high school mathematics research project against the
standard required for a top award at ISEF (International Science and Engineering
Fair), in the Mathematics category. I want a frank evaluation and a concrete
plan, not encouragement. If your honest answer is that the project is not
first-place material and cannot become so by May, say that plainly and explain
what it realistically competes for instead.

## 1. The mathematics

The project studies the generalized Petersen graphs $P(n,k)$ and, more
generally, **cyclic covers**: given a base multigraph $B$ with edge voltages in
$\mathbb{Z}_n$, the derived graph $B^n$ on $V(B)\times\mathbb{Z}_n$. $P(n,k)$ is
the cover of a two-vertex base with loops of voltage $1$ and $k$ and a
connecting edge of voltage $0$.

**Part II — maximum nullity and zero forcing.** For a graph $G$, $M(G)$ is the
maximum nullity over real symmetric matrices whose off-diagonal support is
exactly $E(G)$ (diagonal free), and $Z(G)$ is the zero forcing number;
$M(G)\le Z(G)$ always.

- *Monodromy ceiling.* Eliminating the inner coordinates of **any** matrix
  carrying the $P(n,k)$ pattern — the whole class, not one certificate — leaves
  a single scalar recurrence of order exactly $2k+2$, so
  $\operatorname{null}A=\dim\ker(T-I)\le 2k+2$ with $T$ the monodromy of one
  period, equality iff $T=I$. Since $2k+2$ is also the best known upper bound on
  $Z(P(n,k))$, the matrix-certificate method either settles $Z$ completely or
  cannot settle it at all.
- *It settles it.* Rotation-invariant certificates provably confine $n$ to one
  divisibility class; assembling matrices from tiles each contributing the
  identity to the monodromy removes that, reducing an all-$n$ claim to finitely
  many finite problems. 77 tiles certified by Krawczyk contraction in exact
  rational arithmetic give $Z(P(n,k))=M(P(n,k))=2k+2$ for every $n$ at
  $k=2,3,4$.
- *Consequences.* A published theorem (Rashidi et al., $Z(P(n,3))=8$ for
  $n\ge12$) is false; this replaces it, proves Conjecture 5 of a 2026 arXiv note
  by Krishnan, and fixes the stabilization threshold at 13. The $k=4$ values
  appear to be the first exact ones at that parameter.
- *Generalization.* The ceiling is proved for all two-vertex bases, for
  path-with-loops bases of any size, and for cycle bases (for equivariant
  matrices on any base, provided $\det M(\zeta)\not\equiv0$). For an **arbitrary**
  base it is **false**: a base vertex of degree 1 lifts to pendant vertices, and
  zeroing their (free) diagonals gives $\operatorname{null}A=n$ against a degree
  span of 2. Requiring minimum degree 2 does not repair it ($K_{2,3}$). What
  blocks the obstruction is regularity: for independent $S$ one gets
  $M(G)\ge|S|-|N(S)|$, and no regular graph has an independent set with
  $|S|>|N(S)|$ — but regularity blocks only that mechanism, not the general
  one (next bullet).
- *A refuted result, kept on purpose.* On the $K_4$ base with voltages
  $(0,1,0,2,0,1)$, every cyclic cover is cubic and connected on $4n$ vertices,
  the generic degree span of $\det M(\zeta)$ is $D=6$, an explicit integer
  matrix attains nullity 6, and $Z=n+2$ by CP-SAT with optimality proved for
  $n=4,\dots,8$. The project conjectured $M=6$ — an unbounded cubic gap — and
  claimed the *equivariant* maximum nullity was 6 unconditionally. **Both are
  false:** the three zero-voltage edges form a triangle, a rank-one block on
  each triangle fibre gives $\operatorname{null}A=n$ exactly (so $M\ge n$,
  gap $\le2$), and that matrix is equivariant with $\det M(\zeta)\equiv0$, so
  the equivariant theorem needed a hypothesis it did not state. The
  regular-base conjecture is therefore refuted; the replacement conjecture is
  that the ceiling holds whenever the top coefficient of $\det M(\zeta)$ is a
  monomial in edge weights (true on every proved base, false on every refuted
  one, proved on none beyond those). A numerical search reaches nullity $n+1$
  at $n=4$; it did not rationalise and is labelled numerical.

**Part I — the graph Riemann Hypothesis.** A $(q+1)$-regular graph satisfies the
Riemann Hypothesis for its Ihara zeta function exactly when it is Ramanujan
(every nontrivial eigenvalue $\le 2\sqrt q$ in modulus). The project determines
which $P(n,k)$ do.

- Clearing both radicals (each squaring an equivalence, both sides provably
  positive) reduces the condition to one integer polynomial $D_k\ge0$ on the
  cyclotomic grid.
- $D_k$ is a difference of squares; under $x=\cos\frac{\pi j(k+1)}{n}$,
  $y=\cos\frac{\pi j(k-1)}{n}$ both factors collapse to
  $Q=4x^2+4y^2-8\sqrt2|xy|+3\ge0$, which **does not involve $k$**: one fixed
  forbidden set, four corner regions covering $0.43\%$ of the square.
- Failure is then a simultaneous Diophantine condition, and Dirichlet's
  approximation theorem forces it for every $k$ once $n\ge231$ — so the family
  is finite in **both** parameters.
- Exhausting the rest: exactly **460** pairs $(n,k)$, 324 up to isomorphism,
  from 13,110 cases in exact arithmetic; largest $n=112$; nothing past $k=45$.
- The argument uses only "two-vertex base, cubic cover", so it settles every
  such cover; and on any fixed cubic base only finitely many covers are
  Ramanujan — a quantitative form of the known fact that abelian covers do not
  expand (the principle is *not* claimed as new).

**Verification.** 141 automated checks, all passing. Exact arithmetic wherever a
decision is made; a floating-point control with no authority that fails the run
on disagreement rather than picking a winner; every number in the manuscript
generated from certificates rather than typed.

## 2. What is proved, conjectural, and numerical

Please weigh these differently.

- **Proved:** the monodromy ceiling; the tiling and the $k=2,3,4$ values;
  the Ramanujan classification; the Dirichlet bound; the cover results for
  two-vertex, path-with-loops and cycle bases; the refutations for arbitrary
  bases and for regular bases ($K_4$); the independent-set and
  low-rank-subgraph obstructions; $M(P(10,2))=6$ by an exact integer
  certificate; a period-one ceiling showing no rotation-invariant matrix
  attains $2k+2$ at $(24,4)$ or $(10,2)$.
- **Conjectural:** the leading-coefficient criterion for the cover ceiling;
  the thresholds $N(k)$ for $k\ge6$.
- **Numerical, not certified:** nothing in Part II. $M(P(10,2))=6$ was the last
  such item and is now certified by an exact integer matrix (nullity $6$ by rank
  over $\mathbb{Z}$); the previously undetermined $M(P(24,4))$ is now explained
  rather than certified — no rotation-invariant matrix can attain the ceiling
  there, so the missing certificate is an impossibility for that method and not
  a failed search.

## 3. Context on the field

The minimum rank / inverse eigenvalue problem programme (AIM workshop 2006;
Fallat–Hogben surveys) has two named open conjectures — the delta conjecture
$M(G)\ge\delta(G)$ and the Graph Complement Conjecture — and a standing
question: sufficient conditions for $M(G)<Z(G)$, and whether there is a graph
parameter $Y$ with $M(G)\le Y(G)<Z(G)$ explaining the gap. Documented strict
separations appear to be tree-like (Barioli–Fallat). Published results on cubic
graphs reach $Z=3$ and $Z=4$ (Akbari–Vatandoost–Golkhandy Pour).

Nothing has been submitted to a journal or posted to arXiv. No expert outside
the project has read any of it. Two emails to researchers are drafted and
unsent.

## 4. Provenance — read this before assessing

The student is a high school student. A substantial fraction of the mathematics
above was produced by an AI assistant (Claude) across several working sessions,
with the student directing the work. Specifically:

- **The student's own**, predating the assistance: all of Part II's core — the
  monodromy ceiling, the tiling construction, the Krawczyk certification, the
  $k=2,3,4$ values, the Rashidi correction and Krishnan's conjecture; the
  foundations of Part I including the $D_k$ criterion, the uniform finiteness
  bound and the parity law; the corner substitution $Q(x,y)$; and the
  verification discipline and suite.
- **Produced by the AI:** the Dirichlet absolute bound and the complete 460-graph
  classification; the generalization to cubic cyclic covers; the
  divisor-locality and gcd-safety structure; the path-with-loops and cycle
  theorems; the refutation of the arbitrary-base ceiling; the independent-set
  obstruction; the entire $K_4$ gap family including the integer certificate;
  roughly 1,900 lines of new verification code; and large parts of the current
  manuscript prose.

The AI also introduced several errors that the student's verification
infrastructure caught, including a false negative written into the paper as
evidence for a conjecture later refuted.

The student has not yet written a disclosure statement; the board currently
carries a placeholder and the build refuses to mark it printable until it is
completed.

**Treat this as load-bearing.** "Degree of independence" is a scored interview
criterion at ISEF, and rules on AI assistance are evolving. Assess what this
means both for eligibility/compliance and for how the project will actually fare
with judges who probe.

## 5. What I want from you

1. **A frank comparison** to what actually wins top Mathematics awards at ISEF.
   Be concrete about the gap. If recent winners typically have mentors,
   preprints, or results experts call surprising, say so.
2. **A judgement on the mathematics itself**, at the level a referee would give:
   is any of this a genuine contribution, and how large? Separate the Part I and
   Part II assessments.
3. **An explicit view on the provenance question** — what an honest disclosure
   should contain, whether the project remains competitive once it is disclosed,
   and whether there is a version of this that is both honest and strong.
4. **A full plan**, with a timeline running to roughly May, ordered by expected
   value and marked for risk. Distinguish what raises the ceiling from what
   raises the student's ability to *defend* the work, and say which matters more
   here.
5. **The strongest counterargument to your own plan.**

Do not soften the assessment to be encouraging. The student has asked a version
of "how do I reach first place" seven times and been told "more polish will not
do it" each time; what is useful now is an outside view that is willing to say
something different, including that the target may be wrong.
