# Independent assessment (response to external_assessment_prompt.md)

*Produced 2026-10-01 from the prompt alone, without reading the manuscript, per the prompt's design note. Where a conclusion depends on a detail the prompt does not give, it is marked as conditional. Literature and rules were checked online; sources at the end.*

## 0. The short version

- Not first-place material by May, and the target is partly wrong. The realistic ISEF ceiling is a Mathematics category award (second to fourth; first is possible only if one specific thing lands). The thing worth optimizing is a dated, student-written arXiv note plus one expert who has read it, because that outlasts the fair and is what the fair's judges actually respond to.
- Two external facts change the plan more than anything internal. (1) Krishnan's July 2026 note (arXiv:2607.19412) already contains the Rashidi correction — Z(P(12,3)) = 7, values for n ≤ 20 — so "a published theorem is false; this replaces it" is not this project's discovery; the project's contribution is the uniform lower bound for n ≥ 13. (2) On 26 September 2026 an automated proof pipeline merged a pull request claiming a complete Lean-checked proof of Krishnan's Conjecture 5. It is unreviewed and not on arXiv, but it is dated. The project's note needs to be on arXiv within days, not months.
- The newest result (the K_4 "unbounded gap" family) is very likely wrong as stated, and the reason generalizes: the degree-span ceiling bounds nullity only when the leading coefficient of det M(ζ) cannot vanish, and for the K_4 base that coefficient contains a free diagonal. If the three voltage-0 edges form a triangle, M ≥ n by a four-line rank argument, and the gap to Z = n+2 is at most 2. Details in §2.
- The provenance is survivable if disclosed properly and fatal if not. The honest version and the strong version coincide: the student's own core is the best part of the project, and the AI-produced parts are where the errors live.

## 1. Comparison to what wins

What actually took the Mathematics first award and a $50,000 top prize at ISEF 2026: Nikola Veselinov, "Solvability of Meromorphic Equations in Elementary Functions" — a classical question in differential algebra with a result a working analyst recognizes as an answer to something they had wondered about. 2025 first awards included Serene Feng, "Combinatorial Invariants of Stable Curves in Genus 4" (algebraic geometry, clearly a mentored research-programme problem) and Ryan Xu on epidemic thresholds on random hypergraphs. The pattern over recent years:

- a university mentor, usually through PRIMES, RSI, or a local faculty contact, who chose or shaped the problem;
- a problem in the mentor's own area, so the result is "the next question in a programme" rather than a self-selected curiosity;
- an expert who can say, in a recommendation or at the fair, that the result surprised them or resolves something they cared about;
- frequently a preprint, sometimes a submission, before the fair.

This project has none of the four. The topic — zero forcing and maximum nullity on a specific graph family — is an active area, but the pure mathematicians who typically sit on ISEF Mathematics panels regard "compute parameter X on family Y" as competent rather than exciting, however clean the method. The Ramanujan half will read to those judges as a finite computation dressed in a famous name (see §2). The verification discipline is genuinely unusual for a student project and judges will respect it, but reproducibility raises the floor, not the ceiling.

The concrete gap to first: no expert has read it; nothing is dated; the headline theorem is a specialist's result; the one claim that would make an expert sit up (an infinite cubic family with Z − M → ∞) is conjectural, AI-produced, and probably false.

## 2. The mathematics, as a referee

### Part II — maximum nullity and zero forcing

**The monodromy ceiling.** As a *bound*, null A ≤ 2k+2 is already implied by M ≤ Z ≤ 2k+2 (Rashidi et al., Theorem 2.2, which Krishnan cites). The ceiling is not new; the mechanism is what has value: null A = dim ker(T − I), with equality iff T = I, converting an all-n existence problem into finitely many finite problems via tiles with identity monodromy. That is a transfer-matrix / Floquet idea, standard in spirit (periodic Jacobi matrices, block-Toeplitz nullity), applied well. Why it is a theorem for P(n,k): eliminating the inner vertex v_i from rows u_i and v_i gives a recurrence whose extreme coefficient is a product of edge weights only — the free diagonals never enter it — so the order is exactly 2k+2 for every matrix in the pattern. Keep that sentence; it is the key to everything below.

**The k = 2,3,4 values.** This is real and publishable (Linear Algebra and its Applications, Electronic Journal of Linear Algebra, or Discrete Applied Mathematics level). Two corrections to how it is described:

- The prompt says Z = M = 2k+2 "for every n". Krishnan's exhaustive table gives Z(P(11,3)) = 7 and Z(P(12,3)) = 7, so M ≤ 7 there. The statement must be "for n ≥ 13" at k = 3 (and whatever the threshold is at k = 2, 4). If the manuscript says "every n", a judge who has read Krishnan will find it in thirty seconds. If it says n ≥ 13, fix the prompt and the abstract.
- "A published theorem is false; this replaces it" is Krishnan's result, not yours. What you add is what he says is missing: "a lower-bound proof valid for all large n." That is a good contribution. Describe it as proving his Conjecture 5 and nothing more.

**The scoop.** PR #10129 in `the-omega-institute/trureturing`, merged 26 September 2026, claims a complete proof of Conjecture 5 by an isoperimetric argument on forcing sets, with 40 Lean modules. Authored by a human account with an AI co-author line; no reviewer comments. It is not a paper, it has not been checked by anyone, and it may be wrong — but its date precedes anything of yours that is public. Your route (M = 8 via certificates, which also gives the matrix-theoretic statement) is independent and arguably stronger. Priority is settled by arXiv timestamps in practice. Post the k = 3 note this week.

**The k = 4 values** are probably the first exact ones and are the most defensible novel numbers in the project. Keep them central.

**The K_4 gap family — the serious problem.** The claim "equivariant maximum nullity is pinned at 6" rests on: nullity of an equivariant matrix = number of n-th roots of unity that are roots of det M(ζ), a Laurent polynomial of degree span 6. That counts roots only if det M(ζ) is not identically zero, and the span is 6 only if the extreme coefficients are nonzero. The extreme coefficient of det M(ζ) is a signed sum over permutations of V(K_4) achieving the maximum total voltage. For P(n,k) the maximizing permutation uses both loops and the coefficient is w_1·w_k ≠ 0. For K_4 with voltages (0,1,0,2,0,1), exponent 3 is achieved by a 3-cycle (which fixes a vertex and therefore multiplies by a *free diagonal*) and by a 4-cycle; the coefficient has the form w·w'·(M_aa·w_db − w_da·w_ab) and vanishes for a legal choice of M_aa. So "span 6 for every n" is a statement about generic matrices, not about the class. The ceiling for this base is not a theorem by the P(n,k) argument, and the pinned-at-6 claim is at best "generic equivariant nullity ≤ 6".

Conditional on configuration, it is worse. The three voltage-0 edges of K_4 form a triangle, a star, or a path. If a triangle (call its vertices a, b, d and the fourth c): layer i is a K_3 {a_i, b_i, d_i} with no edges to other layers except through c-vertices, and each c-vertex has its three neighbours in three different triangles. Take every triangle block to be rank one, T_i = u_i u_iᵀ with all entries of u_i nonzero (legal: off-diagonals nonzero, diagonals free). Then rank A ≤ rank(rows of triangle vertices) + rank(rows of c-vertices) ≤ (rank T + rank C) + n ≤ n + n + n = 3n, so null A ≥ 4n − 3n = n. Hence M ≥ n, Z = n+2, and the gap is at most 2 — the family is not a gap family at all. In the equivariant picture, det M(ζ) ≡ 0. If the zeros form a star or a path this particular construction does not apply, but the vanishing leading coefficient does, and the honest status becomes "generic equivariant nullity 6; true M unknown."

The general lesson, which also kills the "regularity blocks the obstruction" claim: for any S ⊆ V, M(G) ≥ |V| − mr(G[S]) − 2|V∖S|. The independent-set bound is the case mr(G[S]) = 0. Regular graphs block that case and nothing else; a regular cover whose layers contain triangles (mr = 1) is wide open. The right conjecture is not "regular bases" but: *the ceiling holds for a voltage base when the maximum-voltage term of det M(ζ) is a nonzero monomial in edge weights — no fixed points in the maximizing permutations, no cancellation.* That is a tropical-determinant / assignment condition on the base, it is exactly what the student's own P(n,k) argument uses, and it is probably provable in general. It is also the one ceiling-raising move in this project that the student can own.

**M(P(10,2)) = 6, numerical.** Either certify it with the same Krawczyk machinery or drop it from the claims.

### Part I — Ramanujan P(n,k)

"Ramanujan ⟺ Ihara zeta satisfies RH" is a textbook equivalence for regular graphs (Ihara, Bass; Murty's survey). Calling the project "the graph Riemann Hypothesis" adds no content and will be read by knowledgeable judges as inflation. Say "which P(n,k) are Ramanujan" and mention the zeta connection in one sentence.

The mathematics itself is tidy: the reduction to the k-independent forbidden set Q(x,y) ≥ 0 is a genuinely pretty observation; the Dirichlet bound making the family finite in both parameters is the kind of step a referee enjoys; the exact enumeration (460 pairs, 324 up to isomorphism, max n = 112) is solid. The "abelian covers do not expand" principle is correctly not claimed as new. I searched for a prior classification of Ramanujan generalized Petersen graphs and found none, but this is exactly the sort of thing that sits in a 2010s paper on I-graphs or circulant covers; a MathSciNet search is mandatory before posting. Appropriate venue: a short note (Involve, Discrete Mathematics Letters, Ars Mathematica Contemporanea at best). It is a nice second paper. It is not what wins ISEF, and the AI produced the parts (Dirichlet bound, the full census) that make it a paper rather than an observation.

### Verification

131 exact-arithmetic checks with a float control that fails on disagreement is better hygiene than most published papers in this area. It is the student's own, it caught AI errors, and it is the single most convincing thing to say in an interview about how the work was done. It is not a mathematical result.

## 3. Provenance

**Rules.** The Society for Science AI-use table (October 2025, in force for 2026) is explicit:

- Using AI "to initially write the research plan, abstract, paper or poster": never acceptable; guidance or refinement *after* the student has written the document is acceptable with explicit citation and a prompt log.
- Using AI "to produce your conclusions, future steps, etc.": never acceptable.
- Using AI to write initial code: acceptable only with explicit citation stating which portions are AI-generated and a prompt log.
- "All materials presented must be in the researcher's own words." Inappropriate use is grounds for failure to qualify. Affiliated fairs may be stricter.

Against that: "large parts of the current manuscript prose" are AI-written, which is squarely in the never-acceptable row unless the prose is rewritten from the student's own draft; roughly 1,900 lines of AI code must be labelled as such with a log; and several theorems were produced by the AI. The table has no row for "AI proved a theorem," but the nearest row — producing conclusions — is prohibited, and presenting AI-produced results as the student's own would be misrepresentation regardless of the table.

**What an honest disclosure contains.** Essentially §4 of the prompt, made result-by-result: a table with one row per theorem, lemma, construction, and code module, with columns *originated by / proved by / verified by / written up by*, and a pointer to the prompt log. It should state the errors the AI introduced and how they were caught, because that is the strongest evidence that the student was directing rather than transcribing. The disclosure goes in the research plan, the paper, and on the board.

**Is it still competitive once disclosed?** Yes, if the project is reorganized so that what is *presented as results* is what the student can derive at a whiteboard. The student's own core — the ceiling mechanism, the tiling construction, the Krawczyk certification, the k = 2,3,4 values, the verification suite — is the strongest material in the project. The AI-produced material is where the errors are (§2) and where a probing judge will expose a gap between what is on the board and what the student can defend. Degree-of-independence is interview-scored; a judge asks "how did you find the Dirichlet bound?" and listens for ownership, not for provenance.

**The honest-and-strong version:** Paper A (Part II, student's own + whatever the student re-derives), Paper B (Ramanujan note, co-attributed honestly), and the AI-explored material either re-derived by the student and then owned, or presented as "explored with AI assistance; not claimed."

One more thing to disclose, to yourself: this assessment was also written by an AI, from the same family that produced the disputed results. Get a human mathematician to read §2 before acting on it.

## 4. Plan to May

Ordered by expected value. **[C]** raises the ceiling; **[D]** raises defensibility. Defensibility matters more here: the ceiling is capped by the topic, and the realistic failure mode is a judge finding a claim the student cannot defend, not a judge finding the work too modest.

**Week 1 (by 10 October).**
1. **[C, low risk, highest EV]** Post a short arXiv note, written by the student from scratch, proving Krishnan's Conjecture 5 via M(P(n,3)) = 8 for n ≥ 13, citing Rashidi and Krishnan correctly. Four to six pages. Date stamp is the point.
2. **[D, low risk]** Test §2's K_4 argument: build the rank-one-triangle matrix (or, in a star/path configuration, the diagonal choice that kills the leading coefficient) for n = 5..10 and compute nullity exactly. One afternoon. Then rewrite the K_4 section to match whatever is true.
3. **[D]** Fix "every n" to the correct thresholds everywhere.

**October.**
4. **[D, essential for eligibility]** Write the disclosure table and prompt log; replace the board placeholder. Rewrite all AI-produced prose from the student's own outline.
5. **[C]** Send the two drafted emails, plus one to Krishnan (his conjecture; he is the natural first reader and a possible collaborator — decide in advance whether co-authorship is wanted) and one to the Hogben/Fallat circle for Part II. Ask for a read, not an endorsement.
6. Split the manuscript into Paper A and Paper B.

**November – mid-January.**
7. **[C, high risk, time-boxed to six weeks]** The general ceiling theorem: nullity ≤ degree span whenever the maximum-voltage term of det M(ζ) is a nonzero monomial in edge weights. If it lands, and a cubic family with a provable gap M < Z follows (which now requires a base that satisfies the criterion *and* has linear Z — not obviously available), that is the one result an expert would call interesting. If no proof by 15 January, stop and present it as a conjecture with the K_4 computation as evidence either way.
8. **[D]** Derivation drills and mock interviews with someone who will probe the AI-produced parts specifically.
9. If the student is a senior: Regeneron STS deadline is early November; the essays require own work and the disclosure above makes that answerable.

**February – March.** Affiliated fairs. Poster and presentation built from Paper A. Freeze claims.

**April.** Drills only. No new mathematics on the board.

**May.** ISEF. Target: Mathematics category award. A first requires item 7 plus an expert's read.

**Risks, marked:** scoop on Conjecture 5 (already partially realized; item 1 mitigates); K_4 collapse (likely; item 2 resolves it either way, and a collapse costs nothing if found now and everything if found by a judge); eligibility (moderate; item 4 resolves it, but check the affiliated fair's own AI policy, which may be stricter); item 7 failing (likely; it is time-boxed so it cannot sink the rest).

## 5. The strongest counterargument to this plan

"This plan cuts the project back to the safe part, posts a modest note early, and then drills. The student has been told 'more polish will not do it' seven times, and this is more polish with a disclosure form attached. The ambitious claim — a cubic family with unbounded Z − M — is the only thing here that could win, and the plan treats it as a liability. If it is false, prove it false and find the family that is true; if the regular-base conjecture is wrong, the leading-coefficient conjecture is right there, and a student who proves it and exhibits the gap family has a result that beats most of what wins. Spend the six months on that, not on rewriting prose."

The reply: the ambitious claim is the AI's, it is probably wrong, and a student who cannot reproduce it at a whiteboard is worse off presenting it than not. But the counterargument is half right, and the plan concedes it in item 7: the leading-coefficient theorem is the right ambition, because it is the student's own P(n,k) argument made general. The disagreement is only about sequencing — whether to secure the dated note and the disclosure first. Given a merged Lean PR dated five days ago, sequencing is not optional.

## Sources

- Krishnan, *A correction to the Zero Forcing Number of the Generalized Petersen Graphs P(n,3)*, arXiv:2607.19412 (13 July 2026): https://arxiv.org/abs/2607.19412 — Z(P(12,3)) = 7, table for 7 ≤ n ≤ 20, Conjecture 5.
- PR #10129, "Prove Krishnan's Conjecture 5", the-omega-institute/trureturing, merged 26 Sep 2026: https://github.com/the-omega-institute/trureturing/pull/10129 (and the failed earlier attempt, issue #8375).
- Society for Science, *Use of generative AI to support a research project* (Oct 2025): https://sspcdn.blob.core.windows.net/files/Documents/SEP/ISEF/2026/Rules/Generative-AI-Use-Table.pdf
- ISEF Rules for All Projects: https://www.societyforscience.org/isef/international-rules/rules-for-all-projects/
- Regeneron ISEF 2026 full awards: https://www.societyforscience.org/press-release/regeneron-isef-2026-full-awards/
- Regeneron ISEF 2025 full awards: https://www.societyforscience.org/press-release/regeneron-isef-2025-full-awards/
- Akbari, Vatandoost, Golkhandy Pour, *Maximum nullity and zero forcing number on cubic graphs*, arXiv:1705.09773: https://arxiv.org/abs/1705.09773
- Gera & Stănică, *The spectrum of generalized Petersen graphs*, Australas. J. Combin. 49: https://ajc.maths.uq.edu.au/pdf/49/ajc_v49_p039.pdf
- Murty, *Ramanujan Graphs*, J. Ramanujan Math. Soc. 18 (2003): https://mast.queensu.ca/~murty/ramanujan.pdf
