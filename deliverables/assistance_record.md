# Record of AI assistance — factual input for the provenance statement

> **RECONSTRUCTED 4 October 2026.** The original was emptied to 0 bytes at
> 10:47 on 4 Oct and was never committed, so it is not recoverable from git.
> This rebuild is from a verbatim reading of the original earlier the same
> session. Sections marked **[verbatim]** were read in full and are reproduced
> faithfully. Sections marked **[header only]** had their contents summarised,
> not read line by line, and must be checked and completed by Aryan against his
> own records before this is relied on for any disclosure.
>
> **Commit this file.** Losing it twice would be worse than losing it once.

**What this is.** Factual input for a provenance statement. You cannot write an
accurate disclosure without knowing what happened.

**What this is not.** It is not the disclosure itself, and it is not a judgement
about what is allowable.

---

## 1. What was already yours, before these sessions **[verbatim]**

This is the larger part of the project.

**All of Part II.** The monodromy ceiling (`thm:red`) — eliminating the inner
coordinates of any matrix on the P(n,k) pattern to get a recurrence of order
2k+2 — is yours, and it is the best theorem in the paper. So are the rotation
bootstrap, the identity-tile construction, the Krawczyk certification in exact
rational arithmetic, the 77 certified tiles, the exact values at k = 2, 3, 4,
the correction to Rashidi et al., and the proof of Krishnan's Conjecture 5.

**The cover reductions.** `thm:cover`, `thm:red2` and `thm:theta`.

**The foundations of Part I.** The criterion D_k ≥ 0, the clearing of both
radicals by equivalences, the uniform finiteness bound n ≤ π(2+√2)√(k²+1), the
parity law, and the exact certification for k ≤ 10 giving 247 graphs.

**The corner theorem.** Q(x,y) = 4x² + 4y² − 8√2|xy| + 3 and the factorisation
behind it; brought to the first session already found and already persisted in
`ramanujan_exact.py`. The AI contribution there was verification only.

**The verification discipline itself** — exact arithmetic where a decision is
made, a control with no authority, generated rather than typed numbers, and the
`verify_all.py` suite (99 checks at the start of these sessions). Also the prior
exploration of the cover-ceiling question: `cover_maxnull.py`,
`cover_ceiling.py`, `cover_ceiling_sharp.py`, `cover_ceiling_search.py`,
including the exp-parametrisation insight that a penalty cannot keep an
optimiser off the degenerate stratum.

---

## 2. What the AI produced in these sessions **[verbatim]**

### Mathematics (statements and proofs originated by AI)

| Result | Where it is now |
|---|---|
| Absolute finiteness: n ≥ 231 fails for every k, by Dirichlet's approximation theorem | `thm:absolute` |
| Complete classification: 460 pairs, 324 isomorphism classes, nothing past k = 45 | `thm:allk` |
| Corner criterion on every two-loop base; theta-base criterion; uniform bounds for both | `thm:covcorner`, `thm:thetarh`, `thm:covfinite` |
| No infinite Ramanujan family is a cyclic cover | `thm:noinfinite` |
| The deficit δ* and its 3−2√2 bound | `prop:deficit` |
| Locality at divisors; divisor closure; min‖jc/m‖ = gcd(c,m)/m; gcd safety; the k ≤ 9 closed form | `thm:local`, `cor:divclosed`, `lem:mingcd`, `thm:gcdsafe`, `prop:closedsmall` |
| Ceiling on path-with-loops bases of any size | `thm:redpath` |
| Ceiling on cycle bases | `thm:redcycle` |
| **Refutation** of the arbitrary-base ceiling, and failure of the min-degree-2 repair | `thm:cexcover`, `rem:mindeg` |
| Independent-set obstruction and why regularity blocks it | `prop:indobs`, `cor:regblocks` |
| The cubic gap family — **the conjecture was refuted on 1 October, see §5** | `sec:gapfamily`, `prop:k4cert`, `prop:k4z` |
| M(P(10,2)) = 6 — no strict gap there, contradicting your stated expectation | `rem:twoexc` |

Also found by AI: the float64 guard underflow in `sign_exact` (the guard
10^−(dps−15) underflowing to 0.0, so the imaginary-part test could never pass),
latent in the region n > 126.

### Code — new modules, all AI-written

`cubic_covers_rh.py` (346), `cover_ceiling_attack.py` (286),
`ramanujan_closed_form.py` (242), `make_corner_figures.py` (227),
`ramanujan_all_k.py` (222), `cover_ceiling_counterexample.py` (160),
`cubic_gap_family.py` (158), `cover_ceiling_grad.py` (138),
`make_graph_figures.py` (96). Plus substantial edits to `verify_all.py` (99 →
130 checks, sections 16–21), the `ramanujan_exact.py` guard fix, and
`manuscript/Makefile`.

### Writing

Large parts of `zf_ramanujan.tex` and `zf_paper.tex` — the statements, proofs
and surrounding prose for everything in the table above, plus §"What this
contributes, and what it does not". Log entries 32 and 33. Most of the board
text and its restructuring. Every file in `deliverables/` except
`abstract_250.md` and `interview_prep.md`, which were revised rather than
written.

### Figures

`fig_corner`, `fig_deficit`, `fig_cover`, `fig_icon`, regenerated `fig_ramclass`.

### Literature search

The minimum-rank survey in `research_programme.md` — the delta conjecture, the
Graph Complement Conjecture, the M versus Z question, the cubic case (Akbari et
al.), and the observation that documented strict separations are tree-like —
came from AI web searches.

---

## 3. Things worth being precise about **[verbatim]**

**The corner theorem is yours.** It is the single prettiest idea in Part I and
the AI did not find it.

**The refutation is the AI's, and it refuted your conjecture.** `thm:cexcover`
kills a statement the paper had recorded as open.

**The AI introduced errors that are now caught in the record.** A false negative
written into the paper as evidence *for* the cover ceiling; a near-miss report of
a strict gap at P(10,2) that does not exist; an invented theorem number for the
Rashidi citation (corrected to Thm 3.6); an announced verification run that was
not running. Log Entry 33 records these.

**Volume is itself a disclosure-relevant fact.** The paper went from 47 to
roughly 60 pages and the suite from 99 to 130 checks across three days.

---

## 4. What you need to do with this **[header only — reconstruct]**

Original content not recovered. Rewrite from your own records.

---

## 5. Session of 1 October (evening) — the refutation and the handoff **[header only]**

The K4 cubic gap family conjecture was refuted: the base's zero-voltage edges
form a triangle, and a rank-one block on each triangle fibre gives null A = n
(exact over ℚ, n = 4..10). `thm:cover` was given its missing hypothesis
det M(ζ) ≢ 0. New: `prop:lowrank`, `conj:leading`, `thm:k4rankone`,
`verification/k4_rank_one.py`. Details in `HANDOFF.md` §1, which survives.

---

## 6. Session of 1 October (late) — COMPLETION_PLAN **[header only]**

Exact M(P(10,2)) = 6; a period-one ceiling; path refactor (49 files hardcoded an
absolute path, in 82 places); clean repo at `/Volumes/2TB/zero-forcing-covers`.
Suite to 141 checks.

---

## 7. Session of 2 October — the foundations guide **[header only]**

`manuscript/zf_guide.tex` rebuilt as a 75-page foundations guide. AI-written.

---

## 8. Session of 2 October — the explainer series **[header only]**

The one-hour video replaced by a 15-episode from-scratch series in
`video/series/` (scripts E01–E15, scenes, tts, render, assemble). AI-written.

---

## 9. Session of 3 October — making the mathematics the spine **[header only]**

`prop:closedsmall` became a theorem via new `lem:bands` (Sturm root isolation
over ℚ); `verification/interior_bands.py` new. Framing changes to
§sec:contribution, the abstract and the poster. All AI-drafted.

### 9b. Later the same day

`thm:ratclass` — classification of rational-symbol rotation-invariant
certificates: n divisible by one of 7,9,15,20 (k=2); 10,24,42 (k=3);
60,70,90 (k=4); 24,126 (k=5); none (k=6); 120 (k=7). AI-derived and
machine-verified. `verification/period_one_classification.py`.

---

## 10. Session of 4 October — tiles for every large length **[added 4 Oct]**

Direction from the author: attack the controllability question of log Entry 25
directly. AI-originated; log Entry 37 is marked `[AI-DRAFTED — rewrite or
discard]`.

| Result | Where |
|---|---|
| The invariant form is the discrete Wronskian, det B = e₀^{2k}/c₀^{4k} | `lem:wronskian` |
| Elliptic docks exist for every k | `lem:elliptic` |
| Identity tiles at every length past some L, given a submersive point; L **ineffective** | `thm:tilesallk` |
| Rank hypothesis certified exactly over 𝔽_p | `prop:tilesallk` |
| First- and second-order rank analysis; the all-k rank law | `lem:firstorder`, `lem:secondorder`, `thm:allkranks` |

Consequence: Z(P(n,k)) = M(P(n,k)) = 2k+2 for all sufficiently large n, for
2 ≤ k ≤ 9. New files `manuscript/zf_tiles_allk.tex`,
`manuscript/zf_tiles_rank.tex`. Suite to 148 checks.

**Discrepancy to resolve:** log Entry 37 says the rank hypothesis was certified
"for k = 2 to 12"; `\TileAllK` is 9. One of the two is wrong.

---

## 11. Session of 4 October — structural work by the assessing session

Not mathematics. For completeness:

- `deliverables/PROVENANCE_TABLE.md` — provenance of all 83 numbered results,
  by two independent methods that agree.
- `deliverables/PROPOSAL_cut_the_ai_column.md` — proposal written for outside
  review; `REVIEW_of_cut_proposal.md` is the reply.
- A "Main results" summary added to `zf_paper.tex` after the abstract, assembled
  from existing theorem statements.
- Fixed an undefined reference, `\ref{sec:tiles}` → `sec:tilesallk`
  (`zf_paper.tex:1836`).
- `deliverables/k3_note_SKELETON.md` — a scaffold, deliberately **not** a draft.
- This reconstruction.
