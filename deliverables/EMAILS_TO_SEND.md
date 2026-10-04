# Emails to send — addresses verified 4 October 2026

All three addresses were taken from current faculty pages today, not from the
2011 paper. Verify once more yourself before sending; addresses move.

| Who | Address | Title to use |
|---|---|---|
| Leslie Hogben | `hogben@aimath.org` | **Professor Emerita Hogben** — she is Director of Research Communities at AIM, Professor Emerita at Iowa State, and adjunct at Purdue |
| Ralucca Gera | `rgera@nps.edu` | **Professor Gera** — Professor of Mathematics, Naval Postgraduate School |
| Pantelimon Stănică | `pstanica@nps.edu` | **Professor Stănică** — Professor, Applied Mathematics, NPS |

Sources: aimath.org/~hogben · nps.edu/web/faculty-rgera · nps.edu faculty profile.

> **Note on the earlier draft.** It gave Hogben's AIM title as "Associate
> Director". Her page says **Director of Research Communities**. Corrected below.

> **One judgement call before you send.** These drafts are in my words, not
> yours. Emails are not ISEF "presented materials", so Rule 8 does not apply —
> but if someone replies and wants to talk, you need to sound like the person
> who wrote the email. Read each one aloud and change anything that isn't how
> you'd say it.

---

# 1. Hogben — send first

**To:** hogben@aimath.org
**Subject:** A nullity ceiling on cyclic covers, and Z(P(n,k)) for k = 2, 3, 4

Dear Professor Hogben,

I am a high school student working on zero forcing and maximum nullity, and I
have a result I would value an expert opinion on. There's one theorem I'd most
like checked; the rest can wait.

Eliminating the inner coordinates of any matrix carrying the P(n,k) pattern —
not one certificate, but the whole class S(P(n,k)) — leaves a single scalar
recurrence of order exactly 2k+2. So

    null A = dim ker(T − I) ≤ 2k+2,

where T is the monodromy of one period, with equality exactly when T = I. The
point is that 2k+2 is also the best known upper bound on Z(P(n,k)), so the
matrix-certificate method either settles Z completely or cannot settle it at
all.

The method settles it: I have a tiling construction, where each tile is
certified by a Krawczyk contraction evaluated in exact rational arithmetic, that
yields Z(P(n,k)) = M(P(n,k)) = 2k+2 for every n ≥ 17 at k = 3 and every n ≥ 29
at k = 4. By exhaustive search below those thresholds, I determine Z(P(n,k)) for
every n at k = 2, 3 and 4.

Krishnan's July 2026 note (arXiv:2607.19412) corrects Rashidi, Shajareh
Poursalavati and Tavakkoli's Z(P(n,3)) = 8 for n ≥ 12 to Z(P(12,3)) = 7, and
conjectures 8 for every n ≥ 13. I prove this conjecture, fixing the
stabilization threshold at 13. I have written it up as a five-page note, which
is the only thing I would ask you to look at:

    https://doi.org/10.5281/zenodo.23140891

My question is narrow: is the monodromy ceiling new, and is the argument sound?
If it's already known, I'd like to hear that before I take it further.

The reduction is not special to P(n,k); it applies to a general cyclic cover as
long as the top coefficient of det M(ζ), the symbol of the cover, is a monomial
in the edge weights, and without that condition it genuinely fails. I have more
on this if it interests you, but the note above is self-contained and does not
depend on it.

Thank you for your time.

Sincerely,
Aryan Padarthi

---

### What I cut from the earlier version, and why

The previous draft also asked whether the bound
**M(G) ≥ |V| − mr(G[S]) − 2|V∖S|** is standard, and described the K₄
counterexample in detail.

I removed both. Not because they are uninteresting — the low-rank bound is a
good question — but because **neither is work you originated.** Per your own
provenance table, `prop:lowrank` and `thm:k4rankone` came from an AI session. If
Hogben replies "that's standard, see Barioli–Fallat," or worse, "that's nice,
how did you find it?", you are in a conversation about mathematics you did not
derive, with the person best placed to notice.

Everything left in the email — the monodromy ceiling, the tiling, the
certification, the exact values, Conjecture 5 — is yours in tracked history
before 28 September. You can defend all of it.

If you re-derive the low-rank bound and want it back in, add this paragraph:

> A second question, if you have the patience: is the bound
> M(G) ≥ |V| − mr(G[S]) − 2|V∖S| standard? It generalises the independent-set
> bound M ≥ |S| − |N(S)| and I have not found it stated.

---

# 2. Gera — send second

**To:** rgera@nps.edu
**Subject:** Ramanujan generalized Petersen graphs — has this been asked?

Dear Professor Gera,

I am a high school student working on spectral graph theory. I have been using
Theorem 2.4 of your 2011 paper on the spectrum of generalized Petersen graphs,
and I have a question I have not been able to settle from the literature.

Using your spectral decomposition, I have classified which P(n,k) are Ramanujan
— equivalently, which satisfy the Riemann Hypothesis for their Ihara zeta
function. Clearing the radicals in the eigenvalue comparison reduces the
condition to the nonnegativity of a single integer polynomial on the cyclotomic
grid, and it turns out that only finitely many members qualify, in both
parameters.

My question is simply whether you are aware of this having been asked before.
Your paper determines the spectrum completely but does not mention Ramanujan
graphs or spectral gaps, and my searches have not turned up anyone who took the
next step for this family — though analogous classifications exist for unitary
Cayley graphs (Droll) and for integral circulant graphs of prime power order
(Le and Sander). I would rather learn that it is known than claim novelty I do
not have.

If it is new to you as well, I would be glad to send the writeup; if you know of
prior work, a pointer would be very helpful.

Thank you for your time, and for the paper — the block decomposition made the
whole thing tractable.

Sincerely,
Aryan Padarthi

---

# 3. Stănică — send third, separately

**To:** pstanica@nps.edu
**Subject:** Ramanujan generalized Petersen graphs — has this been asked?

Identical body to Gera's, with the salutation changed to **Dear Professor
Stănică**. It is joint work, so "your 2011 paper" needs no edit.

**Send as a separate email, not as a CC.** Two people who can each see the other
was asked will each assume the other will answer.

---

# Sending notes

**Order and timing.** Hogben first — she is the one whose reply could change the
outcome. Gera and Stănică the same day is fine; they are a different question.

**Do not ask for anything except the mathematical question.** No mentorship, no
endorsement, no letter, no vouching for a science fair. If a reply comes back
warm, asking about an arXiv endorsement in the *second* email is natural. Asking
in the first is what makes these easy to delete.

**Expect no reply.** One in three is a good rate. That is why you are writing to
three people.

**If Hogben says the ceiling is folklore:** that is worth more than silence. The
contribution narrows to the tiling, the certification and the exact values —
which is still what closes Krishnan's conjecture, and is still the whole of the
posted note.

**If Gera or Stănică say "not that we know of":** that is a citable personal
communication. Record the date and quote it. It is stronger evidence than any
search.

**If nobody replies:** say exactly that, on the board and in the paper. "I wrote
to the authors of the spectrum paper and did not hear back; the novelty claim
rests on search evidence." Knowing the weakness and having tried to close it is
a better answer than search evidence presented as certainty.

**Have the full paper ready as a clean PDF** before you send, in case someone
asks. Not the binder.
