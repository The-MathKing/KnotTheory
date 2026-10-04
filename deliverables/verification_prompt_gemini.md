# Cross-model verification prompt

**Why this exists.** Every check on this project so far has been run by Claude
models. One model family's blind spots are correlated across its own sessions:
this session found a flat self-contradiction in the paper that 141 automated
checks had not caught, and an earlier session recorded a refutation that the
suite missed and an outside read found. A different model is a different
method, which is the only reason to run this.

**The asymmetry that matters most.** Claude's knowledge cutoff is May 2026.
Several load-bearing facts in this project are dated after that — a July 2026
arXiv note, a September 2026 pull request, and the ISEF 2026 results table that
the whole strategy is built on. **No Claude session could verify any of them.**
They were taken from the author or produced by a model that could not check
them. That is the first thing to verify and the most likely place for a
fabrication to be sitting undetected.

**How to use this.** Paste everything below the line into Gemini with search
enabled and reasoning set high. Attach, in this order:

1. `manuscript/zf_paper.tex` — **the `.tex`, not the `.pdf`.** The PDFs are
   currently stale against the source.
2. `results/zero_forcing/verify_all.txt` — the 141-check transcript
3. `deliverables/assistance_record.md` — what was AI-produced, result by result
4. `deliverables/COMPLETION_PLAN.md` — contains the comparables table in §1

Do not attach the paper first and ask for an opinion. Ask for the reference
check first; it needs no mathematics and it is where the risk is.

---

You are fact-checking a high school mathematics research project for
fabrications and errors. A substantial fraction of it was produced by an AI
assistant (Claude), and the author's concern is specifically **hallucination**:
invented citations, invented theorem numbers, claims that drifted from what was
actually proved, and numerical results described as certified.

I want adversarial verification, not a review and not encouragement. **If you
cannot verify something, say UNVERIFIED. Never substitute plausibility for
checking.** A confident "this looks correct" about a reference you did not
search for is the exact failure mode I am trying to catch, and you reproducing
it would make this worthless.

## Priority 1 — External references, especially post-May-2026 ones

Claude could not check any of these. Search for each. Report EXISTS /
DOES NOT EXIST / UNVERIFIED, with what you actually found.

- **`arXiv:2607.19412`**, attributed to "Krishnan", described as a July 2026
  note that (a) corrects an error in Rashidi et al. and (b) contains a
  "Conjecture 5" stating $Z(P(n,3))=8$. Verify the identifier resolves, the
  author, the date, that it contains a Conjecture 5, and that Conjecture 5 says
  what is claimed. **The project claims to prove this conjecture**, so if the
  note or the conjecture does not exist, a headline result loses its meaning.
- **Rashidi et al.**, a published theorem $Z(P(n,3))=8$ for $n\ge12$, cited as
  **Theorem 3.6**. An earlier draft cited it as "Theorem 3.3" and that was an
  invented number. Verify the paper, the venue, and the theorem number.
- **A merged pull request #10129** in a repository named
  `the-omega-institute/trureturing`, dated 26 September 2026, claimed to contain
  a complete Lean-checked proof of Krishnan's Conjecture 5 by "an isoperimetric
  argument on forcing sets". Verify the repository exists, the PR exists, it is
  merged, and it proves what is claimed. The project's posting strategy is built
  on this being a real priority threat.
- **Gera and Stănică**, *The spectrum of generalized Petersen graphs*,
  Australas. J. Combin. **49** (2011) 39–45, and specifically its
  **Theorem 2.4**, a spectral decomposition. The entire Part I argument is built
  on it. Verify the citation and that Theorem 2.4 is the decomposition described.
- **Akbari, Vatandoost, Golkhandy Pour** on zero forcing for cubic graphs,
  cited as reaching $Z=3$ and $Z=4$.
- **Barioli–Fallat** for tree-like strict separations of $M$ and $Z$; the
  **Fallat–Hogben** minimum-rank surveys; the **AIM 2006** workshop; the
  **delta conjecture** and **Graph Complement Conjecture**.
- Any other reference in the bibliography you can check. Flag every entry whose
  existence, authorship, venue, year, or numbering you cannot confirm.

## Priority 2 — The comparables table (`COMPLETION_PLAN.md` §1)

This table ranks the project against named ISEF 2026 Mathematics winners and is
driving the entire strategy and timeline. It is the most hallucination-prone
artifact in the project: specific names, specific arXiv numbers, specific prize
amounts, specific mentors. Verify each:

- "Veselinov — *Solvability of meromorphic equations in elementary functions*",
  1st place + **$50k RYSA**, **arXiv:2602.09253**, co-authored with M. Marinov
- "Fan — *Detecting causality with conjugation quandles over dihedral groups*",
  2nd, **arXiv:2509.03544**, mentored by Chernov (Dartmouth) and Maguire (MIT)
- "Chand — *Universal matrices for Fibo-/C-multinomial coefficients*", 2nd,
  **arXiv:2508.18461**
- The claim that ISEF 2026 Mathematics had **41 finalists and 10 awards**
- The 3rd and 4th place titles listed

If these are fabricated, the plan's central conclusion — "2nd–3rd award is the
realistic target" — rests on nothing, and the author needs to know before
spending 200 hours against it.

## Priority 3 — Internal consistency of the manuscript

A self-contradiction was found in this paper yesterday and had survived for some
time: one passage said $M(P(10,2))=Z(P(10,2))=6$ while two others, including the
Status-of-claims section, said "we expect $M(P(10,2))<Z(P(10,2))$, a strict
gap". The automated suite could not catch it because it checks arithmetic, not
agreement between passages. **Assume more of these exist.** Specifically:

- Read the **Status-of-claims** section against the actual theorem statements.
  Every item marked proved/certified/numerical/conjectural/refuted must match
  what the body says. This section has drifted repeatedly.
- Check every **threshold and quantifier**. A known past error: the abstract and
  board said $Z=M=2k+2$ "for all $n$ at $k=2,3,4$" while the theorems require
  $n\ge17$ at $k=3$ and $n\ge29$ at $k=4$, with small cases covered separately
  and $Z(P(11,3))=Z(P(12,3))=7$. Hunt for surviving instances of this pattern.
- Check **attribution**. The correction to Rashidi is **Krishnan's**, not this
  project's; the project proves his conjecture. Earlier drafts claimed the
  correction. Verify no passage still overclaims it.
- Check that **nothing withdrawn survives anywhere**. Two claims were refuted:
  a conjecture that $M(B^n)=6$ on a $K_4$ cover family, and an unconditional
  bound $Z(B^n)\ge D$. Search the whole document for survivals.
- Check the **three meanings of $D$** are now disambiguated: a divisor set
  (should read $\mathcal D$), the degree span (should read $D$), and the Part I
  criterion polynomial $D_k$.

## Priority 4 — Claims to spot-check mathematically

You will not re-derive the paper. Check these for internal coherence, and flag
any that is stated more strongly than its evidence supports:

- **Monodromy ceiling.** Eliminating inner coordinates of any matrix on the
  $P(n,k)$ pattern gives a scalar recurrence of order exactly $2k+2$, so
  $\operatorname{null}A=\dim\ker(T-I)\le2k+2$, equality iff $T=I$. Is this a
  standard transfer-matrix argument? Say so plainly if it is — the project's
  own assessment says a referee will ask exactly this.
- **Corner criterion.** $D_k$ is a difference of squares; under
  $x=\cos(\pi j(k+1)/n)$, $y=\cos(\pi j(k-1)/n)$ both factors collapse to
  $Q(x,y)=4x^2+4y^2-8\sqrt2|xy|+3$, which does not involve $k$. Verify the
  substitution and that $Q$ is genuinely $k$-free. Check the stated forbidden
  area $3/2-\sqrt2+\tfrac38\log\frac{1+\sqrt2}{3}$.
- **Dirichlet bound.** Failure is forced for every $k$ once $n\ge231$. Check the
  application of Dirichlet's approximation theorem is valid and the constant is
  right.
- **Classification.** Exactly **460** pairs $(n,k)$, **324** isomorphism
  classes, largest $n=112$, nothing past $k=45$, from 13,110 cases. Check these
  are mutually consistent.
- **$M(P(10,2))=6$.** An integer matrix with entries in
  $\{-375,-125,-25,-5,-1,5,25\}$, rank 14 over $\mathbb Z$ on 20 vertices. The
  derivation requires rational entries so two Fourier blocks are Galois
  conjugate over $\mathbb Q(\sqrt5)$, giving $st+2sf+2et-ef=0$. **Check that
  Galois-conjugacy step** — it is the load-bearing one and it is new.
- **Period-one ceiling.** Claim: singular period-one Fourier blocks must have
  pairwise distinct $y_j=2\cos(2\pi jk/n)$, hence a closed-form bound. Used to
  conclude $M(P(24,4))$ *cannot* be certified by a rotation-invariant matrix
  (bound 8 vs ceiling 10). Verify the distinctness argument, and verify it is
  stated as an **upper** bound only.
- **`thm:k4rankone`.** Rank-one blocks on zero-voltage triangles give
  $\operatorname{null}A\ge n$, so $M(B^n)\ge n$ against $D=6$, and
  $Z-M\le2$ where $Z=n+2$. Check the rank count $\operatorname{rank}A\le3n$.
- **A deliberately uncertified claim.** At $n=4$ a search reached nullity 5
  ($=n+1$) with the five smallest singular values at $10^{-9}$–$10^{-11}$ and
  the sixth at $0.24$, but **exact rationalisation failed** so it is labelled
  *numerical*. Confirm the paper does not anywhere treat it as proved. **Do not
  help me upgrade it** — tell me if the labelling is honest.

## Priority 5 — This project's actual failure history

These all really happened. Look for more of each kind:

1. A **failed search reported as impossibility** (an adversarial search found
   "no counterexample" with the counterexample among its inputs).
2. A **near-miss optimum mistaken for a rank deficiency** (a stall at
   $6\times10^{-6}$ read as a strict gap that did not exist).
3. An **invented theorem number** in a citation.
4. **Overclaimed quantifiers** ("all $n$" for a theorem with a threshold).
5. **Misattributed credit** (another author's correction claimed as the
   project's).
6. A **self-contradiction between the Status section and the body.**
7. A **silently partial automated edit** (a refactor that reported 61 changes
   when 82 were needed, because the tool missed a syntax class).

## Provenance — read before assessing

The author is a high school student. Per `assistance_record.md`: the monodromy
ceiling, the tiling construction, the Krawczyk certification, the $k=2,3,4$
values, the $D_k$ criterion, the uniform finiteness bound, the corner
substitution $Q(x,y)$, and the verification suite are the student's own and
predate the assistance. Produced by AI: the Dirichlet bound, the 460-graph
classification, the cubic-cover generalisation, the path/cycle ceiling theorems,
the refutation of the arbitrary-base ceiling, the independent-set obstruction,
the $K_4$ family, the period-one ceiling, the $M(P(10,2))$ certificate, roughly
2,000 lines of verification code, and large parts of the prose.

Treat this as load-bearing: it tells you which passages were written by a system
capable of fabricating a citation, and those are where to look hardest.

## Output format

1. **Reference audit** — a table: claim / EXISTS / DOES NOT EXIST / UNVERIFIED /
   what you found. Lead with anything fabricated.
2. **Comparables audit** — same, for §1 of the plan.
3. **Internal inconsistencies** — every one you find, quoted, with both
   locations and which is correct.
4. **Overclaims** — statements stronger than their evidence, quoted, with the
   weaker true version.
5. **Mathematical concerns** — ranked, separating "this is wrong" from "this
   needs a hypothesis" from "this is standard and should be described as such".
6. **What you could not check**, explicitly.
7. **The single most likely undetected fabrication** in this project, and how
   you would test it.

Do not soften anything. If a central reference does not exist, lead with that
and let the rest wait.
