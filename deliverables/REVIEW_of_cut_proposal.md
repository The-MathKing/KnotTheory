# Review of "cut the AI column"

**Reviewer:** the session that produced most of the October material (poster,
guide, video series, the Sturm lemma, the rational-symbol classification). So I
have the opposite stake from the proposer: cutting removes my work. Weigh that.

**Verdict:** the proposal is right in direction and under-cautious in one place
it did not look. Adopt it with the three changes in §5.

---

## 1. Severability (§3.3): not complete

I re-ran the check mechanically over both files, looking for every `\ref` to an
AI-originated label from outside the AI cluster. The proposer found one. There
are four, and the one that matters is not a theorem.

| Where | What | Severity |
|---|---|---|
| `thm:ramclass` (zf_ramanujan 503, 513, 544) | cites `thm:absolute`, `thm:allk` | known; restate to k ≤ 10 |
| `thm:cover` (zf_paper 1331–1374) | cites `thm:k4rankone`, `thm:cexcover` | the missing-hypothesis coupling; one sentence, keep |
| `conj:generaln` (zf_paper 2655) | cites `rem:twoexc` (exact P(10,2), other session) | trivial; drop the sentence |
| **Paper abstract and introduction** (zf_paper 96–135) | lead with the all-k classification: 460 pairs, 324 classes, n ≤ 230, nothing past k = 45 — five uses of the all-k macros | **the front door of the paper is an AI result** |

Plus the contributions and status sections (zf_paper 3400–3610), which cite
every AI label, as expected, and must be rewritten under any cut.

The fourth row is the one the proposer missed. The numbered results are
severable; the *document* is not, because its abstract was rewritten in the AI
window to lead with the AI theorems. Under the cut, the abstract and
introduction are not edited but replaced, and the headline count goes back from
460 to 247 everywhere: `\RamAllTotal` appears in the paper, poster,
presentation, guide and the video series. The poster I built on 3 October
carries the two newest AI theorems as Theorems 5 and 7; it goes too.

## 2. The provenance split (§3.2): weaker than stated, on the student side

The proposer flags that Part I cannot be checked against git. It is worse than
"cannot be checked." I looked:

- At `dc2a6cf` (28 Sep 18:25) there is **no Part I file at all**: no
  `zf_ramanujan.tex`, no `ramanujan*.py`, nothing matching "Ramanujan" in
  tracked sources. Every Part I file is still untracked today.
- File birth times: `ramanujan.py` 28 Sep 18:47, twenty minutes after the
  boundary commit; `ramanujan_exact.py` 29 Sep. Log Entries 31–32, the only
  Part I entries, are from the same window.
- The record's §1, which assigns the D_k criterion, the corner theorem, the
  parity law and the 247-graph classification to the student, was written by
  the AI, in the same sessions.

I am not saying Part I is not the student's. I am saying the written evidence
does not distinguish "student's work from 28 Sep" from "AI work from 28 Sep",
and the proposal's table presents a distinction the evidence cannot support.
The nine "student" rows in Part I rest on one paragraph the AI wrote about
itself. Only the student can resolve this, and the way to resolve it is in §5.

Part II is on firmer ground: 20+ commits from 25–28 Sep, with the ceiling,
tiles, certification and the k = 3, 4 results all in tracked history before
the boundary.

## 3. Is disclosure sufficient (§6.1)?

Two different questions are being run together.

- **The rule.** Rule 8 is about *materials*: plan, abstract, poster, words.
  Disclosure plus the student's own words satisfies it. It does not speak to
  who had the idea for a theorem. On the rule alone, §6.1 wins: disclosed,
  re-derived, rewritten results may stay.
- **The score.** "Degree of independence" is 25 interview points, assessed by
  asking the student to do mathematics in front of a judge. Here disclosure is
  irrelevant; only mastery counts, and it counts for the student's own results
  exactly as much as for the AI's.

So the proposal's "whiteboard test" is the right criterion, but it is applied
to the wrong set. It should be applied to **all 80 results**, not the 26. A
student who cannot re-derive the monodromy ceiling at the board loses more
than one who cannot re-derive `thm:redpath`, because the ceiling is the
headline. The question "is this result mine?" is less useful than "can I prove
this result?", and the second question also answers the first.

Where I would draw the line, given that test:

| Keep if re-derived (short, elementary, central or near-central) | Cut regardless (peripheral, long, or both) |
|---|---|
| `thm:absolute` — Dirichlet pigeonhole, half a page | `thm:redpath`, `thm:redcycle`, `thm:cexcover`, `prop:lowrank`, `prop:indobs`, `cor:regblocks`, `rem:mindeg` |
| `prop:closedsmall` + `lem:bands` — Sturm on one polynomial | `conj:leading` |
| `thm:local`, `cor:divclosed` — a divisibility argument | `thm:ratclass` (good, but an appendix result) |
| `thm:noinfinite` — one limit | `thm:covcorner`, `thm:thetarh`, `thm:covfinite`, `prop:deficit` |
| `thm:k4rankone` — the refutation, keep as the honesty exhibit | `thm:allk` as stated (becomes a corollary of `thm:absolute` + the census, if kept) |

That is roughly seven to keep and nineteen to cut, not twenty-six to cut. The
seven are each under a page and each is something a strong student learns in
an afternoon and owns in a week. If the student cannot do that by DRSEF, cut
them too.

## 4. Priority (§3.5) and nine pages

**Priority: urgency justified, for a different reason.** Whether #10129
compiles is irrelevant to the decision. Posting costs a week of the student's
writing; not posting leaves an unbounded downside if the PR is sound. A
dominated option. The only caveat: the note must be the student's prose, so
"this week" means "start today", not "paste the draft".

**Nine pages: correlation.** Three data points from one year. What those three
share causally is that a referee could read the whole thing, and someone did.
For Part II alone, 10–15 pages is fine. The target is "one expert finished it",
not a page count.

## 5. What I would change in the proposal

1. **Add the abstract/introduction coupling** to §3.3 and to the work list. It
   is the largest single rewrite and the proposal does not name it.
2. **Replace "cut the 26" with the two-column table in §3.** Seven short
   results are worth a week of the student's time; nineteen are not.
3. **Before anything else, have the student write their own §1 of the record**
   from memory, without reading the existing one: what they did, when, in what
   file. Then diff it against the AI's §1. Where they agree, the provenance
   stands on the student's word rather than the AI's. Where they disagree, the
   student's version wins and the table changes. This is the only way to repair
   §3.2, and it doubles as the first interview rehearsal.

## 6. What the proposer is not seeing

- **Everything after 28 Sep is one undifferentiated block in the record**,
  including the parts the proposer presents as the student's. The record was
  the AI's narrative from the first line. Treat it as testimony, not evidence.
- **The video series and the guide teach the AI results as the project's
  results** (Episode 8: "exactly 460 pairs"). They are study material and are
  disclosed, but if the student drills from them, they will present the cut
  results from habit. Either re-cut the study material or tell the student
  which episodes are now out of scope.
- **The verification suite has 146 checks, ~20 of them for AI-originated
  results.** They are correct and should stay; just don't cite the count on the
  poster as if it measured the presented work.
- **The morale point in §6.5 is real, and the framing fixes it.** This is not
  "discard a third of your project." It is "the fair paper is the twelve-page
  version; the repository is the full version." Both exist. One is for judges.

## 7. One-line answers to §9

1. No. Four couplings, the abstract being the one that matters.
2. Disclosure satisfies the rule; mastery decides the score; apply the
   whiteboard test to everything and keep the seven short results if passed.
3. Yes, because posting is cheap, not because the PR is confirmed.
4. Correlation. Aim for "read to the end", not nine.
5. Part I's provenance rests on the AI's word; let the student write their own
   §1 first.
