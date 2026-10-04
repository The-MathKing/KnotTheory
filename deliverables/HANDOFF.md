# Handoff — state of the project on 1 October 2026, and what is yours to do

Written by Claude at the end of the 1 October session, for Aryan. Read this
first; everything else in `deliverables/` is referenced from here.

---

## 1. What changed today, in one screen

**A result the project was leading with is false, and is now correctly recorded as false.**

The "cubic gap family" — cubic covers of $K_4$ on which the maximum nullity was
conjectured to stay at $6$ while $Z=n+2$ grows — does not exist. The three
zero-voltage edges of that base form a triangle; a rank-one block on each
triangle fibre is a legal matrix with $\operatorname{null}A=n$ (exact over
$\mathbb Q$, $n=4,\dots,10$). So $M\ge n$, the gap to $Z$ is at most $2$, the
regular-base ceiling is false ($K_4$ is cubic), and the sentence "the
equivariant maximum nullity is $6$" was false too, because `thm:cover` needed
the hypothesis $\det M(\zeta)\not\equiv0$ and did not state it.

| Where | What was done |
|---|---|
| `manuscript/zf_paper.tex` | `thm:cover` given its missing hypothesis; new `prop:lowrank` ($M\ge\lvert V\rvert-\operatorname{mr}(G[S])-2\lvert V\setminus S\rvert$); `rem:mindeg` corrected; new `conj:leading` (the leading-coefficient criterion) with the symbolic evidence; `sec:gapfamily` rewritten around the new `thm:k4rankone`; Status-of-claims updated. Builds clean, 63 pp, no undefined references. |
| `manuscript/zf_log.tex` | Entry 35 drafted **in your voice — rewrite it in your own words**. Builds, 44 pp. |
| `manuscript/zf_poster.tex` | The $K_4$ block replaced by a "Refuted (my own conjecture)" block; the "for all $n$ at $k=2,3,4$" claim corrected. Passes the overfull-vbox gate. Still `NOT PRINTABLE` until the provenance placeholder is replaced. |
| `verification/k4_rank_one.py` | New. The refutation, the vanishing symbol, and the leading-coefficient classification on every base in the paper. |
| `verification/verify_all.py` | Four new checks (refutation; $\det M(\zeta)\equiv0$; criterion on proved bases; criterion on refuted bases); two reworded. Suite re-run in progress at time of writing — see `results/zero_forcing/verify_all.txt` for the current transcript and count. |
| `deliverables/abstract_250.md` | "for all $n$ at $k=2,3,4$" corrected (it was false at $(11,3)$, $(12,3)$, $(8,2)$); now exactly 250 words. |
| `deliverables/arxiv_submission.md` | Same correction; urgency note at top (see §3). |
| `deliverables/email_expert_review.md` | $K_4$ paragraph replaced; subject changed; Rashidi/Krishnan attribution fixed. **Do not send the old version.** |
| `deliverables/interview_prep.md` | "Strongest result" answer replaced; new answers for "why is it false" and "what replaces regularity". |
| `deliverables/research_programme.md` | Status note at top: the programme's target statement is false; kept as record. |
| `deliverables/assistance_record.md` | §5 added: everything above, attributed. |
| `deliverables/external_assessment.md` | The outside read that found the error, from the summary alone. |
| `README_zero_forcing.md` | Draft README for a clean repository (see §5). |

**Not updated, and stale until you rebuild them:** `deliverables/RESEARCH_BINDER.pdf`
(contains the old paper and log; rebuild with
`venv/bin/python verification/build_binder.py` after the suite finishes and
`make zf_paper zf_log` has been re-run), `deliverables/presentation_pages/*.png`
(no $K_4$ content, so not wrong, but regenerate if you change
`zf_presentation.tex`). Also: `verification/build_binder.py` has no dates for
log entries 31–34 (they print as "September 2026" in the binder TOC) — fill
them in from your own records; Entry 35 is dated 1 October.

**Nothing has been committed.** The working tree has ~90 modified/untracked
files from the 29 Sept – 1 Oct sessions. Commit when you have read the diff.

---

## 2. Two external facts that set the clock

1. **Krishnan, arXiv:2607.19412 (13 July 2026)** already contains the Rashidi
   correction ($Z(P(12,3))=7$), the exhaustive table for $7\le n\le20$, and
   states as Conjecture 5 that $Z(P(n,3))=8$ for $n\ge13$. The project's
   contribution is the lower bound for all large $n$ — i.e. the proof of his
   conjecture — not the correction. Every summary now says so.
2. **PR #10129 in `the-omega-institute/trureturing`, merged 26 September 2026**,
   claims a complete Lean-checked proof of Conjecture 5 by an isoperimetric
   argument (40 Lean modules, authored by a human account with an AI co-author
   line, no reviewer comments). It is not a paper, nobody has reviewed it, it
   may be wrong — but it is dated, and nothing of yours is public. **Read it
   yourself** (does the Lean actually check? is the statement the full
   conjecture?) and post your note regardless.

---

## 3. What the comparables actually look like

You asked for the level of rigor and completeness of last year's winners. Here
is what was findable.

**ISEF 2026, Mathematics.**

| Award | Project | What backs it |
|---|---|---|
| 1st + Regeneron Young Scientist Award ($50k) | Veselinov, *Solvability of Meromorphic Equations in Elementary Functions* | arXiv:2602.09253, 9 pages, co-authored with Miroslav Marinov; topological Galois theory; resolves a question experts had posed |
| 2nd | Chand, *Universal Matrices for Counting Fibo-Multinomial and C-Multinomial Coefficients* | arXiv:2508.18461 (Aug 2025) |
| 2nd | Fan, *Detecting Causality in (2+1)-Dimensional Globally Hyperbolic Spacetimes Using Conjugation Quandles over Dihedral Groups* | arXiv:2509.03544; Horizon Academic program, supervised by V. Chernov (Dartmouth) and R. Maguire (MIT) |
| 3rd | Ying, *Complexity Functions Are All You Need*; Rangarajan (epidemics); Mehrotra (repelling propellers) | — |
| 4th | MATH008 (projective foci / isogonal cubics), MATH011T (virtual knots), MATH028, MATH035 | — |

The pattern: **every top-three math award in 2026 had an arXiv preprint before
the fair, and two of three had a named university mentor or co-author.** The
winning paper is nine pages. Rigor at this level means a referee could read it;
completeness means the result is stated once, proved once, and the paper ends.
A 63-page document with a Status-of-claims section is a research binder, not
what they submitted.

**TXSEF.** The 2026 category winners are not published by name (TXSEF changed
its policy). 2025 Senior Mathematics: 1st *A Novel Optimizer Equation to Predict
KI67 Scores from Breast Cancer WSIs with CNN*; 2nd *Wavelet and Fourier
Transform ECG Analysis*; 3rd *Quantum-Resilient Polynomial Matrix …
Cryptographic Resilience*. In other words: at the state level the Mathematics
category is won by applied/ML projects, and a pure-mathematics project with a
proved theorem is unusual there. That cuts both ways — it stands out, and the
judges may not be mathematicians.

**DRSEF.** 2025 Senior Mathematics: 1st Jithesh Sarvin Jeganathan (charter),
2nd Annika Ghuman (Plano), 3rd Yorika Ohashi (Frisco). 2026: 2nd Goutham
Ronanki (Plano West), HM Annika Ghuman. Titles are not published in the public
lists; the 2026 results are in a Google Doc linked from
dallassciencefair.org/results (images, not text).

**Judgement.** Against ISEF 2026's bar the project is *not* at the level of
rigor and completeness of the winners — not because the mathematics is weaker
(the $k=2,3,4$ determination is a cleaner, more complete result than at least
one of the 2nd-award projects) but because (a) nothing is posted, (b) no expert
has read it, (c) the document is shaped like a binder, and (d) until today it
led with a false claim. (a)–(c) are fixable by you in weeks. (d) is fixed.

---

## 4. ISEF compliance, mapped onto this project

From the Society for Science AI-use table (Oct 2025, in force for 2026):

| Rule | Where this project stands |
|---|---|

---

## 5. What you do now, in order

Each item says what it is for: **[C]** raises the ceiling, **[D]** raises your
ability to defend the work. Defensibility matters more here.

1. **[D] Read the diff.** `git diff manuscript/zf_paper.tex` and the three
   new/changed verification files. Reproduce `thm:k4rankone` by hand on paper
   before you accept it — it is four lines. If you cannot reproduce it you
   cannot defend it, and it is now in your paper.
2. **[C, this week] Post the $k=3$ note.** 4–6 pages, your own prose: the
   elimination, the tiling, the certification, $Z(P(n,3))=8$ for $n\ge13$,
   citing Rashidi and Krishnan correctly. Nothing else. Date stamp first,
   split the rest later (`arxiv_submission.md`).
3. **[D] Rewrite log Entry 35, then the disclosure.** Use `assistance_record.md`
   §1, §2, §5 as the fact base. Replace the board placeholder. Decide, result
   by result, what you will claim and what you will label as assisted.
4. **[D] Separate the repositories.** The top-level `README.md` describes a
   knot-theory project whose git history includes a commit titled "Abandon
   fabricated proofs". A judge or referee who opens the public repo sees that
   first. Make a fresh repository with `manuscript/zf_*`, `verification/`,
   `results/zero_forcing/`, `src/zero_forcing/`, `deliverables/` and
   `README_zero_forcing.md` as its README.
5. **[C] Send the two emails** (`email_gera_stanica.md`, the corrected
   `email_expert_review.md`), and one to Krishnan — it is his conjecture.
6. **[D] Rebuild the stale artifacts** (binder, checklist count) after the
   suite finishes; regenerate `zf_numbers.tex` with `make numbers` before any
   final build.
7. **[C, time-boxed to mid-January] Attempt `conj:leading`.** It is your
   $P(n,k)$ argument made general; the route is written in the paper under the
   conjecture. If it lands it is the one result here an expert would call
   interesting. If it has not landed by 15 January, stop.
8. **[D] Drills.** `derivation_drills.md`; add "derive thm:k4rankone" and
   "why does thm:cover need $\det M\not\equiv0$" to the list.

---

## 6. Open mathematical items, honestly labelled

- $M(B^n)$ on the $K_4$ family: $\ge n$, $\le n+2$. Not determined.
- `conj:leading`: consistent with all 10 bases checked, proved on none beyond
  the two-vertex, path-with-loops and cycle cases.
- $M(P(10,2))=6$: numerical only. Certify or drop.
- $M(P(24,4))$: open (no nullity-10 certificate; $Z(P(24,4))=10$ by search).
- $k\ge5$ thresholds: $N(5)\le162$ proved; $k\ge6$ open.

---

## 7. What I would not do

Do not spend another session on polish, and do not spend one on a new "strongest
result". The project's weakness is not that it lacks a headline; it is that no
one outside it has read it and nothing is dated. Those are solved by posting
and emailing, which only you can do.

---

## 8. Addendum — review of the late-session changes (1 October, evening)

A second session (recorded in `COMPLETION_PLAN.md` §7 and
`assistance_record.md` §6) added the exact $M(P(10,2))=6$ certificate, the
period-one ceiling, the notation fix, the path refactor and the clean
repository. It had no LaTeX. I checked its work locally:

- **Mathematics.** The period-one bound is correct as stated: with $c\ne0$,
  two singular Fourier blocks sharing $y_j$ force $x_j=x_{j'}$, so singular
  classes have distinct $y$ values; the sums are $8$ at $(24,4)$ and $5$ at
  $(10,2)$ by hand. It bounds *equivariant* matrices only, and the paper says
  so. The $P(10,2)$ certificate is verified by exact rank in the suite. The
  $K_4$ nullity-$(n{+}1)$ witness is labelled numerical and nothing rests on it.
- **Suite.** Re-run locally in the main tree: **141 checks, 0 failures,
  6.8 min on 10 cores.** Re-run independently inside
  `/Volumes/2TB/zero-forcing-covers` with the same result — the path refactor
  holds.
- **Documents.** All four `manuscript/` PDFs, `zf_guide.pdf` (50 pp) and
  `RESEARCH_BINDER.pdf` (118 pp) rebuilt from the current sources; no
  undefined references.
- **Corrected.** `external_assessment_prompt.md` still described the refuted
  $K_4$ family as the newest result; it now describes the refutation, so a
  fresh outside read would see the true picture.
- **Still yours.** Everything in §5 marked *you*; the LICENSE for the clean
  repo; the commit in both trees (`zero-forcing-covers` has 524 files staged
  and no commits); the main repo's `requirements.txt` is still the knot
  project's and can stay that way if that repo is retired.


---

## 9. Addendum — 2 October: the complete foundations guide

`manuscript/zf_guide.pdf` (75 pp) now spans the whole project — Part I, Part
II, covers and refutations, tiles and Krawczyk, verification — in the
definition / intuition / worked-example format, with every claim labelled to
match the paper's Status section. It is built by `make zf_guide` (now in the
Makefile's DOCS). It is AI-written reference material (assistance record §7):
useful for drills and for explaining the project to a mentor or a judge, not
something to submit as your own prose.

## 10. The fifteen-episode explainer series (2 October, later)

`video/series/out/E01_….mp4` … `E15_….mp4` replace the one-hour overview for
a first viewing: every term defined, every definition followed by a worked
example you can redo on paper. Build: `video/series/README.md`. Episode 15
§6 says how to use it: as a drill, redo each worked example on a whiteboard.
AI-written throughout (assistance record §8); not something to submit.

## 11. The pure-mathematics pass (3 October)

The closed form for $k\le9$ is now a theorem with a proof (Lemma `lem:bands`,
Sturm root isolation; `verification/interior_bands.py`). The abstract, the
contributions section and the poster say plainly which results are theorems
and that tile existence is the single computer-assisted step. Two things
would finish the job and are yours: rewrite the new theorem's prose in your
words (assistance record §9), and decide whether to attempt an algebraic
construction of tiles (the open problem that would make Part II entirely
pure).

### 11b. Later on 3 October

Two theorems are new today: the closed form for $k\le9$ (now proved) and the
classification of rational-symbol certificates (`thm:ratclass`, with the new
classes $24,42\mid n$ at $k=3$ and $126\mid n$ at $k=5$). Both are in the paper,
poster, presentation and guide, and in the suite. Log Entry 36 is an AI draft:
rewrite it. If the $k=5$ tile sweep in `results/zero_forcing/tile_sweep_k5_full.txt`
finishes with every length 54–107 solved, run `certify_tiles.py 5` and the exact
re-certification, then change `SETTLE[5]` in `verify_all.py` and the theorem
threshold from 162 to 54.

## 12. 4 October: the all-$k$ tile theorem (AI-derived; decide before presenting)

`manuscript/zf_tiles_allk.tex` (input into the paper after `sec:symplectic`)
proves: elliptic dock + full-rank differential at one length ⇒ identity tiles
of every large length ⇒ $Z=M=2k+2$ for all large $n$. Hypotheses certified
exactly for $k=2..12$. This is the controllability question your 25 Sep
commit posed, answered modulo a per-$k$ rank check. It is AI-originated (record
§10): under the cut proposal it is cut; under the whiteboard test it is one
page of Lie-group argument you could own in a week. Your call. The open
problem that remains is the rank hypothesis for every $k$ (rem:threeperpos).
Update, same day: the rank hypothesis is proved for every $k$ in
`manuscript/zf_tiles_rank.tex` (record §10b), so the all-large-$n$ statement is
unconditional for every $k$. Two steps an expert must sign off on before you
claim it: the Vandermonde surjectivity and the exponential-sum independence in
`lem:secondorder`. The remaining open problem is an effective $L(k)$.
