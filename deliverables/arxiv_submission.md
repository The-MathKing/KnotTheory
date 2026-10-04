# arXiv and journal submission

> **Added 1 October 2026 — read first.** A pull request merged on 26 September
> 2026 in an automated proof repository
> (`the-omega-institute/trureturing`, PR #10129) claims a complete Lean-checked
> proof of Krishnan's Conjecture 5 by an isoperimetric argument on forcing
> sets. It is unreviewed and not on arXiv, but it is dated. Krishnan's own note
> (arXiv:2607.19412, July 2026) already contains the Rashidi correction and the
> table for $n\le20$. **Post the $k=3$ note first, this week, on its own**
> — 4–6 pages, your own prose, citing both — and split the rest afterwards.
> Everything below still applies to the full split.

Work that is posted and under review is a different object to a judge, and the
process forces the writing to meet a standard that is not your own. This is the
step that converts "a very good science fair project" into "a preprint with a
competition attached."

---

## 1. Split it first

**Do not submit the current document to a journal.** At 54 pages with two
largely independent halves, a long technical abstract and a Status-of-claims
section, it is shaped like a binder, not a paper. Referees reject on shape.

Split into two:

| | Contents | Target |
|---|---|---|
| **Paper A** (the stronger one) | The monodromy ceiling, the tiling construction, $Z=M=2k+2$ for $k=2,3,4$ (all large $n$; every $n$ with exhaustive search), the proof of Krishnan's Conjecture 5 (the correction to Rashidi et al. is Krishnan's, cite it), the cover reductions (thm:red2, thm:theta, thm:redpath, thm:redcycle), the two refutations and conj:leading | *Linear Algebra Appl.*, *Discrete Appl. Math.*, or *Electron. J. Linear Algebra* |
| **Paper B** | The corner criterion, the uniform and Dirichlet bounds, the complete classification, the cubic-cover generalisation, the deficit | A combinatorics journal — *Australas. J. Combin.* published the Gera–Stănică spectrum paper this builds on |

Post both to arXiv **at the same time**, cross-referencing each other. Post
before submitting, not after — arXiv priority is the thing that protects you if
someone is working nearby.

---

## 2. arXiv metadata

**Primary category:** `math.CO` (Combinatorics).
**Cross-list:** `math.SP` (Spectral Theory) for Paper B; `math.RA` or
`math.NA` for Paper A if you keep the interval-certification material.

**MSC 2020 (check these against the current scheme before submitting):**
05C50 (graphs and linear algebra) primary; 05C25 (graphs and groups); 15A03
(vector spaces, rank); 11M41 (zeta and $L$-functions in other settings) for
Paper B; 65G20 (interval arithmetic) for Paper A.

---

## 3. Draft arXiv abstract — Paper A

> For a graph $G$, the maximum nullity $M(G)$ over symmetric matrices with
> off-diagonal support $E(G)$ is bounded by the zero forcing number $Z(G)$. We
> study both for cyclic covers. Eliminating the inner coordinates of any matrix
> carrying the pattern of the generalized Petersen graph $P(n,k)$ — not one
> certificate, but the whole class — leaves a single scalar recurrence of order
> exactly $2k+2$, so $\operatorname{null} A = \dim\ker(T-I) \le 2k+2$ with $T$
> the monodromy of one period, and equality precisely when $T=I$. Since $2k+2$
> is also the best known upper bound on $Z(P(n,k))$, the matrix-certificate
> method either settles $Z$ completely or cannot settle it at all. We show it
> settles it. Rotation-invariant certificates provably confine $n$ to a single
> divisibility class; assembling matrices from tiles that each contribute the
> identity to the monodromy removes the restriction, reducing an all-$n$ claim
> to finitely many finite problems. Certifying every tile by a Krawczyk
> contraction evaluated in exact rational arithmetic gives
> $Z(P(n,k)) = M(P(n,k)) = 2k+2$ for every $n \ge 17$ at $k=3$ and every
> $n \ge 29$ at $k=4$; with exhaustive search below those thresholds,
> $Z(P(n,k))$ is determined for every $n$ at $k=2,3,4$. In particular
> $Z(P(n,3)) = 8$ for all $n \ge 13$, which proves Conjecture 5 of Krishnan's
> correction note and fixes the stabilization threshold left open there. The
> reduction is not special to $P(n,k)$: we prove the corresponding ceiling for
> every two-vertex base, for path-with-loops bases of arbitrary size, and for
> cycle bases, in each case with the degree span of $\det M(\zeta)$ as the
> bound; and we show by a cubic cover of $K_4$ that it fails for a regular base
> in general, isolating the condition on the leading coefficient of
> $\det M(\zeta)$ that the proofs use.

## 4. Draft arXiv abstract — Paper B

> A $(q+1)$-regular graph satisfies the Riemann Hypothesis for its Ihara zeta
> function exactly when it is Ramanujan. We determine which generalized Petersen
> graphs do. Clearing both radicals in the eigenvalue comparison — each squaring
> an equivalence, since both sides are provably positive — reduces the condition
> to the nonnegativity of a single integer polynomial $D_k$ on the cyclotomic
> grid. $D_k$ is a difference of squares, and under the substitution
> $x = \cos(\pi j(k+1)/n)$, $y = \cos(\pi j(k-1)/n)$ both factors collapse to
> the quadratic form $Q(x,y) = 4x^2+4y^2-8\sqrt2\,|xy|+3$, which does not
> involve $k$: the forbidden set is four fixed regions at the corners of the
> square, occupying $3/2-\sqrt2+\frac38\log\frac{1+\sqrt2}{3}$ of its area, and
> $k$ enters only through the map into the square. Failure is then a
> simultaneous Diophantine condition, and Dirichlet's approximation theorem
> forces it for every $k$ once $n \ge 231$, so the family is finite in both
> parameters. Exhausting the remaining region in exact arithmetic gives the
> complete classification: exactly 460 pairs $(n,k)$, falling into 324
> isomorphism classes, with largest $n = 112$ and no member for $k > 45$. The
> argument uses only that the cover is cubic over a two-vertex base, so it
> classifies every such cover; and on any fixed cubic base only finitely many
> covers are Ramanujan, a quantitative form of the known fact that abelian
> covers do not expand.

---

## 5. Checklist before posting

- [ ] **Provenance statement resolved.** The same disclosure question applies
      here as on the board, and arXiv is public and permanent.
- [ ] Split into two documents; each self-contained, each with its own
      bibliography.
- [ ] Drop the Status-of-claims section from the journal version — keep it in
      the arXiv version if you like, it is unusual but honest. Keep the
      "What this contributes" section; referees like being told the size of a
      claim.
- [ ] Every generated number (`zf_numbers.tex`) regenerated immediately before
      the final build, so nothing is stale.
- [ ] `verify_all.py` passing, and the repository public with a README that
      says how to run it in one command.
- [ ] Rerun the notation check and a full read for the claims you have
      withdrawn — make sure none survives anywhere in the text.
- [ ] Send the Gera/Stănică and expert-review emails **before** posting, so a
      "this is known" reply arrives while you can still reposition.
