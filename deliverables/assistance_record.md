# Record of AI assistance — factual input for the provenance statement

> **RESTORED 4 October 2026 (afternoon).** This file was never committed and
> was found emptied to 0 bytes at 10:47 on 4 October. Sections 1–10b below are
> restored **verbatim** from the session transcripts: the original write of
> 1 October and every later append, replayed in order (the header line numbers
> of the result match a listing of the live file made on 3 October at 19:20,
> sections 5–9b at lines 167, 212, 290, 319, 346, 375). A partial rebuild made
> by another session earlier this afternoon has been superseded; its own new
> section is kept as §11. **Commit this file.**


**What this is.** You cannot write an accurate disclosure without knowing what
the assistance actually consisted of, and that is the one input I can supply
that you cannot reconstruct from the repository alone. This is my account of
what I produced in the Claude Code sessions of 29 September – 1 October 2026.

**What this is not.** It is not the disclosure itself, and it is not a judgement
about what the rules require. I have deliberately not drafted the statement for
you: what you conceived, directed, understood and verified is yours to state,
and me writing it would reintroduce exactly the problem it exists to solve.

**Verify this against your own records.** This is my recollection plus what the
repository shows. The baseline is commit `dc2a6cf` (28 September 2026);
everything described below postdates it. If anything here is wrong, your record
wins.

---

## 1. What was already yours, before these sessions

This is the larger part of the project, and it is worth stating first because
the list in §2 is long and would otherwise distort the picture.

**All of Part II.** The monodromy ceiling (`thm:red`) — eliminating the inner
coordinates of any matrix on the $P(n,k)$ pattern to get a recurrence of order
$2k+2$ — is yours, and it is the best theorem in the paper. So are the rotation
bootstrap, the identity-tile construction, the Krawczyk certification in exact
rational arithmetic, the 77 certified tiles, the exact values at $k=2,3,4$, the
correction to Rashidi et al., and the proof of Krishnan's Conjecture 5.

**The cover reductions.** `thm:cover`, `thm:red2` and `thm:theta`.

**The foundations of Part I.** The criterion $D_k\ge0$, the clearing of both
radicals by equivalences, the uniform finiteness bound
$n\le\pi(2+\sqrt2)\sqrt{k^2+1}$, the parity law, and the exact certification for
$k\le10$ giving 247 graphs.

**The corner theorem.** $Q(x,y)=4x^2+4y^2-8\sqrt2|xy|+3$ and the factorisation
behind it you brought to the first session already found and already persisted
in `ramanujan_exact.py`. My contribution there was verification only: I
re-derived the substitution independently, checked the identity numerically,
confirmed the area, and cross-checked the corner route against the spectral test.

**The verification discipline itself** — exact arithmetic where a decision is
made, a control with no authority, generated rather than typed numbers, and the
`verify_all.py` suite (99 checks at the start of these sessions). Also the prior
exploration of the cover-ceiling question: `cover_maxnull.py`,
`cover_ceiling.py`, `cover_ceiling_sharp.py`, `cover_ceiling_search.py`,
including the exp-parametrisation insight that a penalty cannot keep an
optimiser off the degenerate stratum — which I initially ignored, to my cost.

---

## 2. What I produced in these sessions

### Mathematics (statements and proofs I originated)

| Result | Where it is now |
|---|---|
| Absolute finiteness: $n\ge231$ fails for every $k$, by Dirichlet's approximation theorem | `thm:absolute` |
| Complete classification: 460 pairs, 324 isomorphism classes, nothing past $k=45$ | `thm:allk` |
| Corner criterion on every two-loop base; theta-base criterion; uniform bounds for both | `thm:covcorner`, `thm:thetarh`, `thm:covfinite` |
| No infinite Ramanujan family is a cyclic cover (quantitative form of a known principle) | `thm:noinfinite` |
| The deficit $\delta^*$ and its $3-2\sqrt2$ bound | `prop:deficit` |
| Locality at divisors; divisor closure; $\min\lVert jc/m\rVert=\gcd(c,m)/m$; gcd safety; the $k\le9$ closed form | `thm:local`, `cor:divclosed`, `lem:mingcd`, `thm:gcdsafe`, `prop:closedsmall` |
| Ceiling on path-with-loops bases of any size | `thm:redpath` |
| Ceiling on cycle bases | `thm:redcycle` |
| **Refutation** of the arbitrary-base ceiling, and the failure of the min-degree-2 repair | `thm:cexcover`, `rem:mindeg` |
| Independent-set obstruction and why regularity blocks it | `prop:indobs`, `cor:regblocks` |
| The cubic gap family: integer certificate at the span, $Z=n+2$, the conjecture — **the conjecture was refuted on 1 October, see §5** | `sec:gapfamily`, `prop:k4cert`, `prop:k4z` (formerly `conj:cubicgap`) |
| $M(P(10,2))=6$ — no strict gap there, contradicting your stated expectation | remark in §on the two exceptions |

I also found the float64 guard underflow in `sign_exact` (the guard
$10^{-(\mathrm{dps}-15)}$ underflowing to `0.0`, so the imaginary-part test
could never pass), which had been latent in the region $n>126$.

### Code

New modules, all written by me:

| File | Lines |
|---|---|
| `cubic_covers_rh.py` | 346 |
| `cover_ceiling_attack.py` | 286 |
| `ramanujan_closed_form.py` | 242 |
| `make_corner_figures.py` | 227 |
| `ramanujan_all_k.py` | 222 |
| `cover_ceiling_counterexample.py` | 160 |
| `cubic_gap_family.py` | 158 |
| `cover_ceiling_grad.py` | 138 |
| `make_graph_figures.py` | 96 |

Plus substantial edits to `verification/verify_all.py` (the suite went from 99
to 130 checks, sections 16–21 being mine), the `ramanujan_exact.py` guard fix,
and `manuscript/Makefile` (the overfull-box gate and the provenance gate).

### Writing

Large parts of the current `zf_ramanujan.tex` and `zf_paper.tex` — specifically
the statements, proofs and surrounding prose for everything in the table above,
plus §"What this contributes, and what it does not". Log entries 32 and 33.
Most of the current board text and its restructuring. Every file in
`deliverables/` except `abstract_250.md` and `interview_prep.md`, which I
revised rather than wrote: `derivation_drills.md`, `email_gera_stanica.md`,
`email_expert_review.md`, `arxiv_submission.md`, `research_programme.md`, and
this file.

### Figures

`fig_corner`, `fig_deficit`, `fig_cover`, `fig_icon`, and the regenerated
`fig_ramclass`.

### Literature search

The survey of the minimum-rank programme in `research_programme.md` — the delta
conjecture, the Graph Complement Conjecture, the $M$ versus $Z$ question, the
state of the cubic case (Akbari et al.), and the observation that documented
strict separations are tree-like — came from web searches I ran, not from you.

---

## 3. Things worth being precise about

**The corner theorem is yours.** It is the single prettiest idea in Part I and I
did not find it. If a disclosure reads as though the mathematics is uniformly
assisted, that would understate your contribution.

**The refutation is mine, and it refuted your conjecture.** `thm:cexcover` kills
a statement your paper had recorded as open. That is a genuine result and it is
not yours.

**I introduced errors that are now caught in the record.** I wrote a false
negative into the paper as evidence *for* the cover ceiling; I nearly reported a
strict gap at $P(10,2)$ that does not exist; I invented a theorem number for the
Rashidi citation (corrected to Thm 3.6); I announced a verification run that was
not running. Log Entry 33 records these. If you are asked how you checked the
assisted work, those are the honest examples — the suite and the exact
arithmetic caught them, which is the system you built working as intended.

**Volume is itself a disclosure-relevant fact.** The paper went from 47 to
roughly 60 pages and the suite from 99 to 130 checks across three days.

---

## 4. What you need to do with this

1. **Read the current ISEF/SRC rules on computational and AI assistance
   yourself.** They change year to year and I will not guess at them.
2. **Write the statement in your own words**, using §1 and §2 to be accurate in
   both directions — neither claiming what you did not do nor disowning what you
   did.
3. **Check it covers the forms as well as the board.** The abstract
   certification asks whether the work reflects your own independent research;
   whatever you write must be consistent across the board, the Research Plan,
   and that form.
4. **Then remove the placeholder.** `make zf_poster` prints `NOT PRINTABLE`
   until the string `AUTHOR: insert` is gone from `zf_poster.tex`.

If the honest statement turns out to be one you are not comfortable putting on a
board, that is important information and it is better to have it now than after
an SRC asks.


---

## 5. Session of 1 October 2026 (evening) — the refutation and the handoff

Everything in this section was produced by Claude in a single session, from
the external assessment onward.

**Mathematics I originated.**

| Result | Where |
|---|---|
| The $K_4$ family is the counterexample to the regular-base ceiling: rank-one triangle blocks give $\operatorname{null}A\ge n$ against $D=6$; $M(B^n)\ge n$, so $Z-M\le2$ | `thm:k4rankone` |
| The low-rank-subgraph obstruction $M(G)\ge|V|-\operatorname{mr}(G[S])-2|V\setminus S|$, generalising `prop:indobs` | `prop:lowrank` |
| The missing hypothesis $\det M(\zeta)\not\equiv0$ in `thm:cover`, and the observation that a rank-one fibre makes it vanish identically | `thm:cover`, the paragraph after it |
| The leading-coefficient criterion, and its symbolic check on every base in the paper | `conj:leading` |

I also refuted, in the process, two statements of mine from §2: the
conjecture $M(B^n)=6$ and the claim that the equivariant maximum nullity of the
$K_4$ family is $6$. Both had been presented as the strongest result in the
project.

**Code.** `verification/k4_rank_one.py` (new, ~150 lines); four new checks and
two reworded ones in `verify_all.py` (suite now 134 checks).

**Writing.** The external assessment (`external_assessment.md`), which found
the error from the prompt alone; the rewritten `sec:gapfamily`, the new
`prop:lowrank` and `conj:leading` with surrounding prose, the corrected
`rem:mindeg` and the two caveat paragraphs, and the new Status entries in
`zf_paper.tex`; log Entry 35 (drafted in your voice — rewrite it); the replaced
$K_4$ block on the board; the corrected abstract, arXiv draft, expert email,
interview answers and research-programme header; `HANDOFF.md`; and the
zero-forcing README draft.

**Corrections of fact.** The abstract, board, arXiv draft and interview script
said $Z=M=2k+2$ "for all $n$ at $k=2,3,4$"; the paper's theorems have $n\ge17$
and $n\ge29$, and $Z(P(11,3))=Z(P(12,3))=7$. The "refutation of Rashidi" is
Krishnan's (arXiv:2607.19412, July 2026), not this project's; the project
proves his Conjecture 5. Both were overclaims in material I had written.

**For the disclosure.** The strongest-sounding result of the 29 Sept – 1 Oct
sessions was wrong, it was mine, and the project's own standard — exact
arithmetic, adversarial checks, a status list — did not catch it: it was
caught by an outside read of a summary, i.e. by a different method. That is a
fair thing to say in an interview and a fair thing to say about AI assistance.

---

## 6. Session of 1 October 2026 (late) — executing COMPLETION_PLAN, *either* items only

This session worked only the tasks `COMPLETION_PLAN.md` §3 marks **either**.
I declined the **you** items and said so: B1, B3, B5, A5, A6, A7, A8, C1–C7,
D1–D5, E5, F1, F4, F6, F7, G1–G4. In particular I did not write any part of
the $k=3$ note, did not rewrite the AI-written prose (B3), did not re-derive
the theorems for you (A5), and did not draft the disclosure.

**Mathematics I originated.**

| Result | Where |
|---|---|
| $M(P(10,2))=6$ by an **exact integer** certificate: period-one is impossible there; period-two forces $6=2+1+1$ over the $\mathbb Z_5$ blocks; rational entries make the $j=1,2$ conditions Galois conjugate over $\mathbb Q(\sqrt5)$, giving $st+2sf+2et-ef=0$ and $a^2=-c^2d^2ef/((s+2e)(t+2f)(sf+et-ef))$. Nullity $6$ by rank over $\mathbb Z$. | `rem:twoexc`, `verification/p10_2_exact.py` |
| **The period-one ceiling.** Singular period-one Fourier blocks must have pairwise distinct $y_j=2\cos(2\pi jk/n)$, so $\operatorname{null}A$ is at most the sum over distinct $y$-values of the largest $\pm$class in each. Gives $8$ at $(24,4)$ against a ceiling of $10$, and at $k=2$ blocks exactly $n=8,10$ — the paper's two exceptions, derived rather than observed. | the $k=4$ discussion, `verification/period1_ceiling.py` |

The second of these generalises the $k=2$ antipodal/pigeonhole remark that was
already yours; the mechanism is different from the parity obstruction in
`antipodal_obstruction.py`, which is about roots of the symbol.

**Corrections of fact I made to the manuscript.** The paper contradicted
itself on $P(10,2)$: one remark said $M=Z=6$ while two other passages still
said "we expect $M(P(10,2))<Z(P(10,2))$, a strict gap". The two stale passages
were survivals of an expectation that had already been refuted, and one of them
was in the Status list. Corrected, and the claim moved from *numerical* to
*certified*. The $P(24,4)$ sentence "we simply have not found the matrix" was
replaced by the impossibility argument above.

**Notation (B7).** `$D$` carried **three** meanings, not the two the plan
names: a divisor set (`lcm(D)`), the degree span, and `$D_k$`. The set became
$\mathcal D$ in `zf_paper.tex` and `zf_guide.tex`. I deliberately did not
change `zf_log.tex`: retroactively editing dated log entries misrepresents the
record.

**Code.** New: `verification/p10_2_exact.py`, `verification/period1_ceiling.py`,
`verification/k4_max_nullity.py`, `verification/k4_nplus1.py`,
`tools/make_clean_repo.py`. Seven new checks in `verify_all.py` (suite 134 →
**141**), one of which is a control asserting the new bound contradicts none of
16 existing certificates; plus runtime reporting.

**Repository (E1–E4).** 49 files hardcoded the absolute path
`/Volumes/2TB/scifair` in 82 places, so no clone of this project could ever
have run. All now resolve the repository from `__file__`. Verified inert: the
suite's output after the change was byte-identical to the recorded transcript.
`requirements.txt` had been the knot project's (`torch`, `snappy`, `xlrd`,
`pandas`); replaced with the eight real dependencies, pinned to the versions
that produced the transcript. A clean tree was built at
`../zero-forcing-covers` (522 files, 10.3 MB, against 1.5 GB) from an auditable
manifest, with the knot/octal code and the compiled C binaries removed and a
Makefile added so the solvers build from source. `pip install -r
requirements.txt && make` passes 141/141 on it. Staged, **not committed** — E5
is yours.

**A mistake worth recording, because it is the same kind as before.** My first
path-rewriting pass used `tokenize` to find string literals and silently missed
21 of the 82 occurrences: Python 3.12+ emits f-strings as `FSTRING_START/
MIDDLE/END`, not `STRING`. Had I trusted the count it reported, the repository
would have been left half-converted and the breakage would have surfaced only
on someone else's machine. It was caught by comparing against a plain
`grep -c`, i.e. by a second method rather than by a more careful first one —
which is the same lesson as the refutation in §5.

**Not done, and why.** B2 (the Paper A/B split) is dated 15 Nov and would
collide directly with your B3 rewrite of the same passages, so starting it now
would create merge work rather than progress. F3 and F5 (quad chart, binder)
need LaTeX, which was not available in the environment I ran in — **every PDF
in `manuscript/` is now stale against its `.tex`** and needs a local rebuild.

**For the disclosure.** Two of this session's results are mine and both are
corrections to the project's own record rather than new mathematics: a
self-contradiction in the paper, and a claim of "not found" that was actually
"cannot exist". Neither was caught by the verification suite as it stood;
both were caught by reading the text against itself. That is worth saying,
because it is the honest answer to "how do you check the assisted work?" —
the suite catches arithmetic, not inconsistency.


---

## 7. Session of 2 October 2026 — the complete foundations guide

`manuscript/zf_guide.tex` was rebuilt as a complete reference spanning both
halves of the project (75 pages). Retained from the September version: the
primer, the zero-forcing and $M\le Z$ material, the families, the rotation
bootstrap, forts, the monodromy recurrence, period-one certificates and the
cyclotomic section, with their worked examples. **Written by Claude in this
session:** the new abstract; §9 (identity tiles, parameter count, Krawczyk's
test with a worked $\sqrt2$ example, exact arithmetic, the $k=3$ row and the
Krishnan/Rashidi attribution); §10 (cyclic covers, the cover reduction *with*
its hypothesis, both refutations, `prop:lowrank`, the $K_4$ family with the
exact rank table, the leading-coefficient table and conjecture); §11
(period-$d$ status relabelled to match the paper, the period-one ceiling with
the $(10,2)$ and $(24,4)$ class tables, the exact $P(10,2)$ certificate); §12
(all of Part I: Ihara zeta, $D_k$ with $D_2$ expanded by hand, the corner
criterion, finiteness three ways with a Dirichlet example at $n=231$, the
classification, locality, the cover criteria, the no-go, the deficit); §13
(verification standards, what the suite caught and what it did not); the
second symbol table; the status summary. Tone edits to the retained text
("miracle", "breakthrough", "demolishing", "published fallacy" → "a claim of
ours", 128 exclamation marks removed); the September version's "Theorem 10.2"
claiming $k\ge6$ values as theorems was replaced by the paper's numerical
label; the old cover-reduction box gained the missing hypothesis. Every number
in the new worked examples was computed by code in the session and
hand-checked. This is a pedagogical reference, not a fair-submitted document;
under the ISEF table it is AI-generated material to be cited as such if used.

---

## 8. Session of 2 October 2026 — the fifteen-episode explainer series

The one-hour explainer video made on 1 October (`video/`) assumed linear
algebra and was judged too compressed. It was replaced by a series of fifteen
episodes in `video/series/` (about 2 h 50 min) that assume only high-school
algebra and a little trigonometry and define every term before using it:
graphs → matrices and eigenvalues (worked on $C_4$, a $2\times2$ matrix, and
an explicit Petersen eigenvector) → random walks and the spectral gap →
the Ihara zeta and the two-line computation showing RH $\iff$ Ramanujan →
complex numbers, roots of unity, the $2\times2$ blocks (the Petersen spectrum
recomputed from five blocks) → $D_k$ with both squarings checked → the corner
criterion, AM–GM, Dirichlet by pigeonhole → exact arithmetic and the
classification → zero forcing and $M\le Z$ → recurrences and the ceiling →
rotation-invariant certificates (a nullity-6 matrix for $P(12,2)$ built by
hand, the antipodal obstruction, Galois orbits) → Newton, interval arithmetic
and Krawczyk on $\sqrt2$ → tiles → covers and the $K_4$ refutation → status
and verification. **Written by Claude in this session:** all narration
(`video/series/scripts/E01.md`–`E15.md`), all animation code
(`video/series/scenes/`), the build scripts, and this record. Every worked
number was computed by code in the session before being written into the
script (Petersen blocks, $D_2$ values, $Q$ values, the $n=12$ certificate
$a=1+\sqrt3$, $d=2+\sqrt3$, $c^2=3+\sqrt3$ verified to nullity 6, the Krawczyk
box, the $K_4$ rank-one nullity). Narration is synthesised speech (Kokoro).
The videos are study material, not a submission artifact.

---

## 9. Session of 3 October 2026 — making the mathematics the spine

Direction from the author: less reliance on computation, more pure
mathematics. What was done, all AI-drafted and to be rewritten by the author
where it is prose:

- **A proposition became a theorem.** `prop:closedsmall` (closed form of the
  Ramanujan classification for $k\le9$, $k\ne6,8$) was recorded in the paper as
  "verified case by case, not derived". It is now Theorem `prop:closedsmall`
  (label kept) with a proof: new Lemma `lem:bands` (the negative set of $D_k$ on
  $[-1,1]$ is the end band(s) alone exactly for $k\in\{1,2,3,4,5,7,9\}$, by
  exact root isolation over $\mathbb Q$ — Sturm's theorem, an integer
  computation — and the parity symmetry $D_k(-u)=D_k(u)$ for odd $k$), followed
  by the grid argument (only $j=1$, and for odd $n$ and odd $k$ only
  $j=(n-1)/2$, can enter a band). `verification/interior_bands.py` is new and
  the suite gained two checks (section 17).
- **Framing.** Paper §sec:contribution and the abstract now say which results
  are theorems and name tile existence as the one computer-assisted step
  (exact, in the Hales/Appel–Haken sense). The poster was rebuilt in the
  mathematics-category style (theorems with proof sketches, Introduction →
  Framework → Findings → Conclusions per the ISEF 2026 template), with the new
  Theorem 5 and with floating-point/bug/script vocabulary removed from the
  mathematical columns. Figures regenerated in one palette
  (`verification/make_*_figures.py` colour constants changed).
- **Not done, honestly:** a hand proof of tile existence. The paper's
  §sec:resist shows why forts, the fort LP and spectral bounds cannot give the
  all-$n$ lower bound; a pure route would be a new idea (a parametric tile
  family, or tiles built from two Galois certificates).

### 9b. Later the same day — a second theorem, and the consistency pass

- **Theorem `thm:ratclass` (classification of rational-symbol rotation-invariant
  certificates).** New, AI-derived and machine-verified: such a certificate of
  nullity $2k+2$ exists on $P(n,k)$ iff $n$ is divisible by one of $7,9,15,20$
  ($k=2$); $10,24,42$ ($k=3$); $60,70,90$ ($k=4$); $24,126$ ($k=5$); none
  ($k=6$, recovering `thm:k6imp`); $120$ ($k=7$). Proof: Galois-closed root
  sets of size $k+1$ are finitely many; the product of the $\Psi_d$ must match
  $(s+a)(t_k+d')-c_0$ in its forced middle coefficients, and $c_0\ne0$.
  `verification/period_one_classification.py` enumerates; suite section 23
  rebuilds the lists and checks every listed certificate's nullity on and off
  its class; macros `\RatClassTwo`…`\RatClassSeven` are generated. The classes
  $24,42$ ($k=3$) and $126$ ($k=5$) were not in the paper before.
- Consistency: abstract retitled to the poster's title; presentation frames
  "Findings 4" and "Conclusions" rewritten to the theorem/computation split;
  quad chart wording; guide gained Theorem 9.2 and Theorem 12.8a with worked
  examples; log Entry 36 drafted (marked AI-DRAFTED, to be rewritten by the
  author); paper introduction gained the paragraph identifying the symbol
  $M(\zeta)$ as the one object behind both parts; §sec:closed now states the
  classification as locality plus a finite table of bad levels.
- A full k=5 tile sweep (lengths 54–107) was started so that the $k=5$ threshold
  can drop from 162 to 54 if every length solves and certifies; results in
  `results/zero_forcing/tile_sweep_k5_full.txt`.
- Header band now dark; full-width section bars; trifold column gaps; Avenir for
  header and bars (Helvetica Neue body, CM math); columns fixed to one shared
  bottom margin; six key formulas displayed on their own lines; school filled in
  (Allen High School, Allen, Texas).
- 3 Oct, late: REVIEW_of_cut_proposal.md written by the poster/guide/video session, reviewing PROPOSAL_cut_the_ai_column.md (both AI-written; the student decides).

---

## 10. Session of 4 October 2026 — identity tiles for every large length (AI-derived)

The author asked the agent to attack the open problem it had identified:
whether identity tiles exist for every $k$ (controllability in $Sp(2k+2)$).
**Everything in this section was derived by the AI**; it is the largest
single AI-originated result in the project and is labelled as such in the
paper (`manuscript/zf_tiles_allk.tex`, `sec:tilesallk`).

What was found, in order:
1. The adjacency-weight dock is elliptic only for $k=1,2,5$ (eigenvalues of the
   step matrix off the unit circle otherwise), so the dock must be chosen;
   an explicit elliptic family $(0,1,c_0,0,\pm1)$ exists for every $k$
   (`lem:elliptic`, proved).
2. At the dock point the tile differential has rank $\dim Sp-(k-2)$ for every
   $k$ (the three-parameter obstruction, infinitesimally), so a submersion at
   that point is impossible for $k\ge3$; but full rank at a nearby generic point
   plus an elliptic product suffices (`thm:tilesallk`, proved: compact-subgroup
   argument, ineffective $L$).
3. The invariant skew form is the discrete Wronskian; proved invariant for all
   $k$; $\det B=e_0^{2k}/c_0^{4k}$ observed on 24 random rational docks and
   computed exactly for the docks used (`lem:wronskian`,
   `verification/tile_wronskian.py`).
4. The generic rank obeys $3\ell-5k-5$ (two diagonal gauge directions per
   position), which explains why tiles appear at 21 and 29 rather than at the
   5-count's 16 and 24 (`rem:threeperpos`, observed, not proved).
5. Exact certificates for $2\le k\le12$: Sturm ellipticity over $\mathbb Q$,
   exact $\det B$, and the Jacobian rank over $\mathbb F_p$ by forward-mode
   differentiation (`verification/tile_rank_exact.py`,
   `results/zero_forcing/tile_rank_exact_k7_12.txt`). Suite section 24 checks
   $k\le9$ and generates `manuscript/tiles_allk_table.tex`.

Result: $Z(P(n,k))=M(P(n,k))=2k+2$ for all sufficiently large $n$ at every
$2\le k\le12$ — new for $k\ge6$, where no tile has been found. Not done: the
rank hypothesis for all $k$ (conjectured). The author must decide whether to
present this at all (see `REVIEW_of_cut_proposal.md`); if presented, it must
be re-derived and rewritten, and attributed as AI-assisted.

### 10b. Later on 4 October — the rank hypothesis for every $k$ (AI-derived)

`manuscript/zf_tiles_rank.tex` (`sec:tilesrank`): Lemma `lem:firstorder`
(at the dock point the image of the tile differential is every root space plus
a 3-dimensional Cartan subspace: the $a$-weight direction has root-space
coefficient $-c_0/(a_0+s_j)\ne0$, and the Cartan motions span $\{1,u_j,1/u_j\}$);
Lemma `lem:secondorder` (one perturbation lifts the rank to $\dim Sp$, via
$\operatorname{rank}(A+\varepsilon B)\ge\operatorname{rank}A+\operatorname{rank}(\pi B|_{\ker A})$
and the brackets $[Y_{t_1},Y_t]$, whose Cartan parts are exponential sums in
the position difference and are independent under a nonresonance condition);
Theorem `thm:allkranks`: $Z(P(n,k))=M(P(n,k))=2k+2$ for all sufficiently large
$n$, for every $k\ge2$. Checked: dock-point deficit $k-2$ and single-perturbation
full rank at $k=3..8$ in floats and $k=3..6$ exactly mod $p$ (suite §24); the
predicted failure at the resonant symmetric dock for $k=5$ was observed.
Not written out in the draft: the Vandermonde surjectivity ("enough positions")
and the exponential-sum independence in `lem:secondorder` are cited as
standard facts. Treat it as a proof sketch until an expert has read it.

---

## 11. Session of 4 October — structural work by the assessing session

Not mathematics. For completeness:

- `deliverables/PROVENANCE_TABLE.md` — provenance of all 83 numbered results,
  by two independent methods.
- `deliverables/PROPOSAL_cut_the_ai_column.md` — proposal for review.
- A "Main results" summary added to `zf_paper.tex` after the abstract,
  assembled from existing theorem statements.
- Fixed an undefined reference `\ref{sec:tiles}` → `sec:tilesallk`
  (zf_paper.tex:1836).
- `deliverables/k3_note_SKELETON.md` — a scaffold, deliberately **not** a draft.
- This reconstruction.

---

## 12. Session of 4 October 2026 (afternoon) — the leading-coefficient criterion is a theorem (AI-derived)

The author asked for the open problem `conj:leading` to be attacked ("lets go
try problem 1"). Everything below was produced by Claude in that session and is
disclosed as such; the prose is a draft to be rewritten by the author.

**Mathematics I originated.**

| Result | Where |
|---|---|
| `conj:leading` is now **Theorem `thm:leading`**: if the top coefficient $c_{\max}$ of $\det M(\zeta)$ is a nonzero monomial in the edge weights alone, then $\operatorname{null}A\le D$ for every $A\in\mathcal S(B^n)$ and every $n$ | `manuscript/zf_leading.tex`, input into `zf_paper.tex` after the statement |
| Theorem `thm:stripdim`: under the same hypothesis the kernel of the lifted operator on the infinite strip has dimension **exactly** $D$ for every choice of nonzero weights and any diagonal | same file |
| Lemma `lem:potentials` (integer potentials from the assignment dual; $\det L=c_{\max}$ as a polynomial identity) and Lemma `lem:monomial` (monomial $c_{\max}$ $\iff$ unique maximising permutation using no diagonal; sub-blocks $L[S,\sigma^*(S)]$ nonsingular) | same file |
| The proof idea: grade the strip twice (rows at $t+p_i$ / unknowns at $s-q_j$ from the top, $t-q_i$ / $s+p_j$ from the bottom), take the window $\{\lambda\le b,\ \lambda'\ge\beta\}$, show its rows are independent and every window solution extends uniquely both ways, count $\lvert U\rvert-\lvert R\rvert=2\sum_i(p_i+q_i)=D$ | `thm:stripdim` |
| Remark `rem:monodromy`: $\operatorname{null}A=\dim\ker(T-I)$ on a $D$-dimensional space for every base satisfying the criterion (the $P(n,k)$ monodromy theorem for all such bases) | same file |
| Remark `rem:onegrading`: a single grading over-counts; the forward state $\sum_j m_j\ge D$ with equality iff $p$ is also, after a sign change, an optimal column potential; explicit base (loops $2,1,3$; edges $0{-}2,0{-}1,1{-}2$ of voltages $0,3,2$) with $\sum m_j=13$, $D=12$, $\dim K=12$; this is what `thm:order`'s $N>D$ measures; also $M(B^n)\le D\le Z(B^n)\le\min\sum_j m_j$ | same file |
| The remark after `thm:order` now says the question it left open is answered except for the tie $t_m=p+q$ | `zf_paper.tex` |

What was tried first and abandoned: the chained elimination suggested in the
paper (its order exceeds $D$ on the base above), and a single-grading state
count (gives $\sum_j m_j$, which is $D$ for $P(n,k)$ but not in general; the
condition for equality, $\Pi_{\mathrm{row}}\cap(-\Pi_{\mathrm{col}})\ne\emptyset$,
fails on about a quarter of random bases satisfying the criterion). The
two-grading count came from noticing that the bottom level of an unknown
exceeds its top level by exactly $p_j+q_j$.

**Code.** `verification/leading_coefficient.py` (new): symbolic $c_{\max}$;
maximising permutations; Bellman–Ford potentials; the window $U,R$ with exact
rank over $\mathbb F_p$; the forward-transfer monodromy and its zero-eigenvalue
count; random bases. `verify_all.py` section 25 (two checks: all paper bases,
25 random bases). Scratch scripts (not in the repo) tested the intersection
condition on 3000 random bases.

**Writing (all AI-drafted, to be rewritten).** `zf_leading.tex`; the theorem
statement replacing the conjecture; the paragraph before it; the remark after
`thm:order`; the Status entries (the "Added 4 October" paragraph and the
Conjectural item); one sentence in the abstract; a `schrijver` bibitem; guide
Theorem 10.9 and its paragraph, two status lines; poster (the refutation
sentence and one open-problem bullet); presentation (two lines); log Entry 38;
HANDOFF §13; this section.

**Precision.** The theorem is stated for every $n\ge1$; for small $n$ parallel
lifts are split into nonzero strip weights summing to the entry, and loops with
$n\mid v$ are absorbed into the strip diagonal. The hypothesis "monomial in the
edge weights alone" is used in exactly one place: it makes every tight
sub-block nonsingular for every choice of nonzero weights. When $c_{\max}$ has
two or more monomials the proof gives nothing, and whether the ceiling can fail
there (e.g. the tie $t_m=p+q$ on two vertices) is open.

**For the disclosure.** This is the third AI-originated theorem of 4 October
(after `thm:tilesallk` and `thm:allkranks`). Under the whiteboard test it is
the most elementary of the three — potentials, two gradings, a count — and the
one the author can most plausibly own; under the "cut the AI column" proposal
it is cut. The author decides.
