# Completion plan — where the paper ranks, and everything left before it is done

Written 1 October 2026, after the comparables research in `HANDOFF.md` §3.
This supersedes the plan in `external_assessment.md` §4 where they differ.

---

## 1. Ranking

### 1a. Against ISEF 2026 Mathematics (41 finalists, 10 awards)

What I actually know of each awarded project: full papers for the top three
(all on arXiv); titles only for the seven below them. The ranking is therefore
confident at the top and approximate in the middle.

| Rank | Project | Backing | Compared with this paper |
|---|---|---|---|
| 1 | Veselinov — *Solvability of meromorphic equations in elementary functions* (1st + $50k RYSA) | arXiv:2602.09253, 9 pp, co-authored with M. Marinov; topological Galois theory | **Above.** Resolves a question working analysts had posed; one theorem, one proof, a referee can read it in an hour. Nothing here is at that level. |
| 2 | Fan — *Detecting causality with conjugation quandles over dihedral groups* (2nd) | arXiv:2509.03544; mentored (Chernov, Dartmouth; Maguire, MIT) | **Comparable, this paper's substance slightly stronger.** Fan's result is a computation inside a mentor's programme (which quandle detects causality on one link family). $Z(P(n,k))$ for $k=2,3,4$ at every $n$, proving an attributed conjecture, with exact certification, is a more complete result. Fan has what this lacks: a preprint and a mentor. |
| 2 | Chand — *Universal matrices for Fibo-/C-multinomial coefficients* (2nd) | arXiv:2508.18461 | **Comparable.** A generalization of a prior paper's matrix-product formula. Similar size of contribution to Part II here. Has a preprint. |
| 3 | Ying — *Complexity functions are all you need*; Rangarajan — epidemic early warning; Mehrotra — repelling propellers (3rd ×3) | titles only | **Below on mathematical substance** (modelling / applied), judging by titles. Presentation likely stronger than this project's. |
| 4 | MATH008 projective foci/isogonal cubics; MATH011T virtual knots; MATH028 blood-flow numerics; MATH035 persistent homology on voting (4th ×4) | titles only | **Below or comparable.** |
| — | 31 unplaced | — | This project **as it stood yesterday** — leading with a false claim, no preprint, binder-shaped — would most likely have landed here or at 4th. |

**Placement estimate, honestly.**

- **As it stands today** (false claim removed, nothing posted, prose AI-written, no expert read): 4th award or unplaced. The mathematics is 2nd-award-level; the presentation and provenance are not, and judges score what they can probe.
- **After the plan below is executed** (posted preprint in your own words, split papers, one expert who has read it, disclosure on the board, interview-proof): **2nd–3rd award is the realistic target.** Part II's substance is at the 2nd-award level of 2026.
- **1st** requires one of: `conj:leading` proved (a theorem about a class, not a family), or an expert telling the judges the monodromy ceiling surprised them. *Update 4 Oct: `conj:leading` is proved (`thm:leading`), but by the AI (record §12); it counts toward the ceiling only if the student can own it at a whiteboard.* Plan for 2nd, leave the door open.

### 1b. Against DRSEF / TXSEF

Senior Mathematics at both is won by applied projects (2025 TXSEF: a CNN
optimizer, ECG wavelets, post-quantum crypto). A proved theorem on a named
open conjecture is unusual there and will stand out — **DRSEF 1st and a TXSEF
place are likely** — but the category judges may not be research
mathematicians, so the 30-second explanation and the board carry more weight
than at ISEF. Prepare for both audiences.

### 1c. As mathematics, independent of fairs

Part II (Paper A): publishable in *Linear Algebra Appl.* / *Electron. J.
Linear Algebra* / *Discrete Appl. Math.*; a referee will ask whether the
monodromy ceiling is standard (it is a transfer-matrix argument, applied well)
and will accept the tiling and certification as the contribution.
Part I (Paper B): a short note (*Involve*, *Discrete Math. Lett.*). Neither is
a surprise to experts; both are correct and complete, which most student work
is not.

---

## 2. What "done" means

Three finish lines, in order. Each has a hard date.

| Finish line | Date | Means |
|---|---|---|
| **D1 — Posted** | **10 Oct 2026** | $k=3$ note on arXiv, in your words. Priority established. |
| **D2 — DRSEF-ready** | **10 Feb 2027** (registration) · fair ~28 Feb | Disclosure written and on the board; forms filed; board printed; binder current; interview drills done; abstract SRC-stamped. |
| **D3 — ISEF-ready** | **1 May 2027** | Papers A and B posted and submitted; 12-page presentation, quad chart, 2-min video regenerated from the split papers; at least one expert has read Paper A; every open item either closed or labelled. |

A fourth, optional: **D4 — `conj:leading` proved** by 15 Jan 2027 or abandoned
as a conjecture. Time-boxed; it cannot be allowed to sink D2.

---

## 3. The full task list

Legend. **Owner:** *you* = must be your own work under the ISEF AI-use rules
(research plan, abstract, paper, poster prose, conclusions); *either* =
assistance is permitted with citation and a prompt log (code, figures,
formatting, checking). **Effort** in hours. **[C]** raises the ceiling,
**[D]** raises defensibility.

### A. Mathematics — correctness and closure

| # | Task | Owner | Effort | By | Notes |
|---|---|---|---|---|---|
| A1 | Reproduce `thm:k4rankone` and `prop:lowrank` by hand; confirm you can derive both at a whiteboard | you | 2 | 5 Oct | [D] It is in your paper now. |
| A2 | Determine $M(B^n)$ on the $K_4$ family exactly for $n=4,5,6$ (is it $n$, $n+1$ or $n+2$?): maximise nullity over the full pattern, then certify the winner exactly | either | 6 | 31 Oct | [D] Closes an "open" line in Status. $n=4$: 16 vertices, feasible by search. |
| A3 | Certify $M(P(10,2))=6$ exactly (Krawczyk on the nullity-6 matrix the search found), or delete the claim | either | 3 | 31 Oct | [D] Only "numerical" item left in Part II. |
| A4 | $M(P(24,4))$: one more certificate attempt with the Krawczyk pipeline at higher restart budget; if it fails, leave labelled open | either | 4 (compute) | 30 Nov | [D] |
| A5 | Re-derive, on paper, every AI-originated theorem you intend to claim (list: `assistance_record.md` §2, §5). Anything you cannot re-derive moves to "explored with assistance, not claimed" | you | 20 | 30 Nov | [D] The single most important item for the interview. |
| A6 | **`conj:leading`**: attempt the proof via chained elimination with the square subsystem whose determinant is $c_{\max}$; first on a base with one cycle and one loop, then general | you | 40 | **15 Jan** or stop | [C] The only ceiling-raising item. Time-boxed. |
| A7 | MathSciNet / Google Scholar search: "Ramanujan" + "generalized Petersen" / "I-graphs" / "circulant covers"; confirm Part I is not already in the literature | you | 2 | 15 Oct | [D] Before posting Paper B. |
| A8 | Verify the Lean PR (#10129) actually checks and states the full Conjecture 5; record the result in the log | you | 3 | 15 Oct | [D] Determines how you describe priority. |

### B. Writing

| # | Task | Owner | Effort | By | Notes |
|---|---|---|---|---|---|
| B1 | **$k=3$ note**, 4–6 pp, from your own outline: elimination → monodromy → identity tiles → Krawczyk → $Z(P(n,3))=8$, $n\ge13$; cites RST and Krishnan | you | 12 | **8 Oct** | D1. |
| B2 | Split `zf_paper.tex` into Paper A (Part II) and Paper B (Part I) per `arxiv_submission.md` §1; each self-contained | either (structure) / you (prose) | 10 | 15 Nov | |
| B3 | **Rewrite every AI-written passage in your own words** — from an outline, not by editing. Scope: `assistance_record.md` §2 "Writing" and §5. Includes the Status section, "What this contributes", `sec:gapfamily`, `conj:leading` prose, log entries 32–35 | you | 40 | 15 Dec | [D] ISEF rule: AI may not write the paper. |
| B4 | Drop the Status-of-claims section from the journal versions; keep a one-paragraph "what is certified at what standard" | you | 2 | 15 Dec | |
| B5 | Rewrite `research_plan.md` in your own words (it is AI-written; ISEF requires the plan to be yours) | you | 3 | 1 Nov | [D] Form-critical. |
| B6 | Abstract: already 250 words and correct; re-read after B3 so the two agree | you | 1 | 1 Feb | |
| B7 | Notation check across A and B (one symbol, one meaning; $D$ is used for both $D_k$ and the degree span — rename one) | either | 3 | 15 Dec | |
| B8 | Bibliography: every entry verified against the source; DOIs; Krishnan as arXiv:2607.19412; Rashidi Thm 3.6 | you | 2 | 15 Dec | |
| B9 | Fill dates for log entries 31–34 in `build_binder.py` | you | 0.5 | 15 Oct | |

### C. Posting and outreach

| # | Task | Owner | Effort | By | Notes |
|---|---|---|---|---|---|
| C1 | Post B1 to arXiv (`math.CO`), with code link | you | 2 | **10 Oct** | D1. arXiv endorsement may be needed — ask in C2/C3 if so. |
| C2 | Send `email_gera_stanica.md` (Part I: "is this known") | you | 1 | 12 Oct | |
| C3 | Send `email_expert_review.md` (corrected version) to Hogben, Fallat, and one Iowa State zero-forcing author — individually | you | 2 | 12 Oct | |
| C4 | Email Krishnan: his conjecture, your proof, the note's link; ask whether he has seen the Lean PR | you | 1 | 12 Oct | Possible collaborator; decide beforehand whether you want co-authorship on anything. |
| C5 | Post Papers A and B to arXiv, cross-referenced | you | 2 | 20 Dec | |
| C6 | Submit Paper A (LAA / ELA / DAM) and Paper B (Involve / DML) | you | 3 | 15 Jan | "Under review" by ISEF. |
| C7 | If you are a senior: Regeneron STS application (deadline early–mid Nov 2026) | you | 15 | Nov | Essays must be your own; the disclosure makes that answerable. |

### D. Provenance and compliance

| # | Task | Owner | Effort | By | Notes |
|---|---|---|---|---|---|
| D1 | Read the ISEF International Rules 2026–27 and the Generative-AI Use Table yourself; check DRSEF/TXSEF for stricter local policy | you | 2 | 10 Oct | |
| D2 | Assemble the **prompt log** (the rules require it for AI-generated code and ideas): session transcripts or summaries, dated, by file | you | 4 | 1 Nov | |
| D3 | Write the **disclosure statement**: result-by-result table (originated / proved / verified / written by), the errors the AI introduced and how they were caught, pointer to the log. Goes in the research plan, the paper, and the board | you | 6 | 1 Nov | Replaces `AUTHOR: insert` in `zf_poster.tex`; `make` stops saying NOT PRINTABLE. |
| D4 | Confirm the disclosure is consistent across Form 1A, the abstract certification, the research plan, and the board | you | 1 | 1 Feb | |
| D5 | Forms 1, 1A, 1B via STEM Wizard; abstract SRC approval and stamping | you + sponsor | 3 | **10 Feb** | DRSEF registration. |

### E. Repository

| # | Task | Owner | Effort | By | Notes |
|---|---|---|---|---|---|
| E1 | **New repository** containing only: `manuscript/zf_*`, `verification/`, `results/zero_forcing/`, `src/zero_forcing/`, `deliverables/`, `README_zero_forcing.md` as README, `requirements.txt`, a LICENSE. Fresh history. | either | 3 | 15 Oct | [D] The current public repo's README is the knot project and its history contains "Abandon fabricated proofs". |
| E2 | Remove from the new repo: sourceless binaries, `venv/`, build junk (`*.aux`, `temp_united.pdf`), the knot-theory `src/experiments`, `src/models`, `src/math_engine` | either | 1 | 15 Oct | |
| E3 | One-command reproduce verified on a clean clone (`pip install -r requirements.txt && python verification/verify_all.py`) — including the C solvers' build step | either | 3 | 31 Oct | |
| E4 | `verify_all.py` runtime printed and documented; pin dependency versions | either | 1 | 31 Oct | |
| E5 | Commit the current working tree (≈90 files) after reading the diff | you | 2 | 5 Oct | |

### F. Fair artifacts

| # | Task | Owner | Effort | By | Notes |
|---|---|---|---|---|---|
| F1 | Board: replace placeholder (D3); re-read every block after B3; confirm no URLs/QR/logos/"abstract" heading; print at 48×48 | you | 4 | 15 Feb | |
| F2 | 12-page ISEF Project Presentation regenerated from Paper A/B after the split (Math/CS template order; proofs or proof sketches in FINDINGS) | you (content) / either (layout) | 8 | 1 Apr | |
| F3 | Quad chart regenerated | either | 2 | 1 Apr | |
| F4 | 2-minute video (ISEF requirement) | you | 4 | 15 Apr | |
| F5 | Binder rebuilt (`build_binder.py`) after every document change; final rebuild 1 week before each fair | either | 0.5 each | per fair | |
| F6 | Virtual display board format confirmed with DRSEF | you | 0.5 | 1 Feb | |
| F7 | `DRSEF_CHECKLIST.md` walked top to bottom | you | 1 | 20 Feb | |

### G. Interview

| # | Task | Owner | Effort | By | Notes |
|---|---|---|---|---|---|
| G1 | `derivation_drills.md`: add "derive `thm:k4rankone`", "why `thm:cover` needs $\det M\not\equiv0$", "state `conj:leading` and say what it would prove", "what is yours and what was assisted" | you | 1 | 15 Oct | |
| G2 | Three mock interviews with someone who will probe the AI-assisted parts specifically; one with a non-mathematician (TXSEF-style) | you | 6 | Jan–Feb | |
| G3 | The 30-second, 2-minute, and 10-minute versions rehearsed cold; the 30-second one must work on a non-mathematician | you | 4 | Feb | |
| G4 | Re-read `interview_prep.md` after B3 so the answers match the rewritten text | you | 2 | Feb | |

---

## 4. Timeline

| When | Milestones |
|---|---|
| **1–10 Oct** | A1, A8, E5, D1, B1, C1 (**D1 — posted**), C2–C4, E1–E2, B9, G1 |
| **11–31 Oct** | A2, A3, A7, E3–E4, D2 |
| **Nov** | D3 (**disclosure**), B5, A4, A5 (re-derivations), B2 (split), C7 if senior |
| **Dec** | B3 (rewrite in own words), B4, B7, B8, C5 (post A and B) |
| **1–15 Jan** | A6 stops; C6 (submit) |
| **Feb** | D4, D5 (**10 Feb registration**), F1, F6, F7, G2–G4 — **D2 — DRSEF** (~28 Feb) |
| **Mar** | TXSEF (27–28 Mar); incorporate judge feedback into F2 |
| **Apr** | F2, F3, F4, F5 |
| **1 May** | **D3 — ISEF-ready.** Freeze. Drills only. |
| **May** | ISEF |

Total effort for "you" items: roughly 200 hours over seven months, front-loaded
in Oct–Dec. The rewrite (B3, 40 h) and the re-derivations (A5, 20 h) are the
two large blocks and both are non-negotiable under the rules.

---

## 5. Definition of done — the checklist

The project is done when every box is ticked or the item is explicitly
labelled open in the paper.

- [ ] $k=3$ note on arXiv, dated before anything else of yours is public
- [ ] Papers A and B on arXiv and submitted; every sentence yours
- [ ] At least one expert outside the project has read Paper A and replied
- [ ] Disclosure statement written by you, on the board, in the plan, in the paper, consistent with Form 1A
- [ ] Prompt log assembled
- [ ] `verify_all.py` passes on a clean clone of the new repository in one command
- [ ] Every claim in Status is proved / certified / labelled open; no "numerical" items remain in Part II
- [ ] `thm:k4rankone`, `prop:lowrank`, and every claimed AI-originated result re-derived by you on paper
- [x] `conj:leading` either proved or presented as a conjecture with the symbolic evidence — not as anything in between *(proved 4 Oct as `thm:leading`; AI-derived — rewrite the proof in your words or cut it)*
- [ ] Board printed, binder current, presentation and quad chart regenerated from the split papers, video recorded
- [ ] Three mock interviews done, including one with a non-mathematician
- [ ] Working tree committed; new repository public

---

## 6. What this plan does not include, deliberately

- A new headline result. The project does not need one; it needs the existing
  one posted, read, and owned.
- More polish on the board or presentation beyond what the rewrite forces.
- Any attempt to recover the "cubic gap family". It is gone; the refutation is
  a better interview story than the conjecture was.

---

## 7. Progress log — 1 October 2026 (late session)

Only **either**-owned tasks were worked. Every **you**-owned task is untouched,
including B1, B3, B5, A5, A6, A7, A8, C1–C7, D1–D5, E5, F1, F4, F6, F7, G1–G4.

| # | Status | Notes |
|---|---|---|
| A3 | **DONE, stronger than asked** | Not a Krawczyk interval certificate but an **exact integer** one: entries in $\{-375,\dots,25\}$, rank 14 over $\mathbb Z$, nullity 6. Also proved no period-one matrix can reach 6 there. `verification/p10_2_exact.py`. Found and fixed a **self-contradiction**: two passages still asserted the refuted strict gap while a third said $M=Z=6$. |
| A4 | **DONE, as an impossibility** | No search needed. The period-one ceiling gives 8 at $(24,4)$ against 10, so the absent certificate cannot exist for that method. Validated two ways: contradicts none of 16 existing certificates, and at $k=2$ blocks exactly $n=8,10$ — the paper's two exceptions, now derived. `verification/period1_ceiling.py`. |
| A2 | **PARTIAL** | $n=4$: nullity $n+1=5$ reached with a clean 8-order spectral gap; $n+2$ not reached. **Exact rationalisation failed, so it is labelled numerical, not claimed.** Recorded in the paper with that label and with the structural note that `prop:lowrank` does not explain it. $n=5,6$ not run — each takes hours at the restart budget needed. `verification/k4_nplus1.py`, `verification/k4_max_nullity.py`. |
| B7 | **DONE** | The collision was **three-way**, not two: divisor set, degree span, and $D_k$. Set → $\mathcal D$ in `zf_paper.tex` and `zf_guide.tex`. `zf_log.tex` deliberately unchanged — dated log entries should not be edited retroactively. |
| E1, E2 | **DONE** | `../zero-forcing-covers`: 524 files, 10.4 MB (from 1.5 GB). Fresh history, staged, **not committed**. Built from an auditable manifest: `tools/make_clean_repo.py`. Knot/octal code and compiled binaries removed; C sources kept with a Makefile. |
| E3 | **DONE** | **49 files hardcoded `/Volumes/2TB/scifair`** in 82 places — no clone could ever have run. Now resolved from `__file__`; verified inert (suite output byte-identical to the recorded transcript). `pip install -r requirements.txt && make` passes 141/141 on the clean tree, C solvers built from source. |
| E4 | **DONE** | `requirements.txt` was the knot project's (`torch`, `snappy`, `xlrd`); replaced with the 8 real deps, pinned. Suite now prints its own count and runtime. |
| B2 | **NOT STARTED, deliberately** | Dated 15 Nov. Doing the structural split now would collide with your B3 rewrite of the same passages; half-splitting a 3,500-line file creates merge work, not progress. |
| F3, F5 | **BLOCKED** | No LaTeX in the environment. **Every PDF in `manuscript/` is now stale against its `.tex`** — rebuild locally before anything is printed or sent. |

**Suite: 134 → 141 checks, all passing, 4.9 min.** Seven new checks, one of
them a control on the new bound.

**Two items for §5's checklist.** "No numerical items remain in Part II" is now
true of $P(10,2)$ but a new numerical item exists: the $n=4$ nullity-5 witness.
And the LICENSE (E1) was not written — choosing one has legal effect and is
yours to pick.
