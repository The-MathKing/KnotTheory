# Second priority email — a referee-quality read of Part II

The Gera/Stănică email (`email_gera_stanica.md`) asks one narrow question about
Part I: has it been asked before. This one asks something harder and more
valuable — for someone in the field to tell you whether Part II is right, and
whether it matters.

**Why Part II and not Part I.** Part II is the stronger contribution: it
replaces a false published theorem, proves an attributed conjecture, and gives
the first exact values at $k=4$. It is also the half where an expert read can
change the outcome, because minimum rank / zero forcing is an active programme
with people who will immediately know whether the monodromy ceiling is new.

**Who.** The natural community is the AIM Minimum Rank — Special Graphs Work
Group, both of whose outputs you already cite (`\bibitem{AIM}`, and
Fallat–Hogben's survey `\bibitem{FH}`). Leslie Hogben co-authored the
Burgarth–D'Alessandro–Hogben–Severini–Young paper that supplies your quantum
control motivation *and* the minimum-rank survey, so she sits at the exact
intersection of both halves of your citation list.

**Two things I checked that change the approach.** She is now *Professor
Emerita* at Iowa State, and Associate Director at the American Institute of
Mathematics — which is where the Minimum Rank Special Graphs workshop came from
in the first place. So AIM is the better framing than a university department,
and "Professor Emerita Hogben" is the correct form of address. Her research page
is <https://www.aimath.org/~hogben/research.html>.

**Write to more than one person.** Because she is emerita, also consider
Shaun Fallat (co-author of the survey, University of Regina) and the Iowa State
REU group, which has produced a steady stream of zero-forcing papers and whose
members are actively publishing. Find each person's current page and preferred
contact yourself — do not reuse an address from an old paper, which is the most
common reason these mails bounce.

**What makes this email different from the first.** You are not asking whether
something is known. You are asking a professional to spend an hour. So lead with
the thing that would make it worth their hour — the ceiling theorem — and make
the ask small and bounded.

---

**Subject:** A nullity ceiling on cyclic covers, and $Z(P(n,k))$ for $k=2,3,4$

Dear Professor Hogben,

I am a high school student working on zero forcing and maximum nullity, and I
have a result I would value an expert opinion on. I have tried to make the ask
small: there is one theorem I would most like checked, and everything else can
be ignored.

Eliminating the inner coordinates of *any* matrix carrying the $P(n,k)$ pattern
— not one certificate, the whole class $\mathcal S(P(n,k))$ — leaves a single
scalar recurrence of order exactly $2k+2$. So

$$\operatorname{null} A = \dim\ker(T - I) \le 2k+2,$$

with $T$ the monodromy of one period, and equality exactly when $T = I$. The
point is that $2k+2$ is also the best known upper bound on $Z(P(n,k))$, so the
matrix-certificate method either settles $Z$ completely or cannot settle it at
all. It settles it: a tiling construction, with each tile certified by a
Krawczyk contraction in exact rational arithmetic, gives
$Z(P(n,k)) = M(P(n,k)) = 2k+2$ for every $n \ge 17$ at $k = 3$ and every
$n \ge 29$ at $k = 4$, and with exhaustive search below those thresholds
$Z(P(n,k))$ is determined for every $n$ at $k = 2, 3, 4$.

Two consequences I believe are new, and which are the reason I am writing rather
than simply posting it. Krishnan's July 2026 note (arXiv:2607.19412) corrects Rashidi, Shajareh
Poursalavati and Tavakkoli's $Z(P(n,3)) = 8$ for $n \ge 12$ to $Z(P(12,3)) = 7$
and conjectures $8$ for every $n \ge 13$; this proves that conjecture and fixes
the stabilization threshold at 13. The $k = 4$ values appear to be the
first exact ones at that parameter.

The reduction is not special to $P(n,k)$. For a general cyclic cover of a
voltage base $B$, the same bound holds for every equivariant matrix whose symbol
$\det M(\zeta)$ is not identically zero, and for *every* matrix on two-vertex,
path-with-loops and cycle bases. It fails for arbitrary bases (a pendant fibre
with zero diagonal gives nullity $n$), and — this is the part I most want
checked — it fails for regular bases too: on a cubic cover of $K_4$ whose
zero-voltage edges form a triangle, a rank-one block on each triangle fibre
gives $\operatorname{null} A \ge n$ against a degree span of $6$, by the
elementary bound $M(G) \ge |V| - \operatorname{mr}(G[S]) - 2|V \setminus S|$.
What the proofs actually use is that the top coefficient of $\det M(\zeta)$ is
a monomial in edge weights, so it cannot vanish; I conjecture that condition
is sufficient in general.

My questions are narrow. **Is the monodromy ceiling new, and is the argument
sound?** And **is the low-rank-subgraph bound
$M(G) \ge |V| - \operatorname{mr}(G[S]) - 2|V \setminus S|$ standard?** It
generalises the independent-set bound $M \ge |S| - |N(S)|$ and I have not found
it stated. I would rather learn now that either is folklore than claim it isn't.

If it is useful I can send the paper (it states, for every claim, whether it is
proved, proved by an exact certificate, proved by interval certification, or
numerical, and lists the claims of my own I have withdrawn). But I did not want
to send 50 pages unasked.

Thank you for your time.

Sincerely,
Aryan Padarthi

---

## Before you send

- **Have the paper ready as a clean PDF**, not a binder. Nobody reads a binder.
- **Expect no reply.** Researchers get a lot of unsolicited mail. One reply in
  three attempts is a good rate, so write to more than one person — but write to
  each individually, never as a visible group.
- **If they say it's folklore**, that is worth more than silence. The reduction
  being standard would narrow the contribution to the tiling and the exact
  values, which is still the part that closes Krishnan's conjecture.
- **Do not ask them to be your mentor, co-author, or to vouch for you to a
  fair.** Ask the mathematical question only. Anything else comes later, if at
  all, and offering it up front is what makes these emails easy to ignore.
