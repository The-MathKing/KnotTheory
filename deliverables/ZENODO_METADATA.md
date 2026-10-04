# Zenodo deposit — fill-in sheet

Copy each field across. Fields not listed here: leave blank.

---

## Community

**Skip it.** Click "Skip" / submit without a community. You can add one later;
it only adds a review step now.

## Files

Upload **`deliverables/k3_note.pdf`** (5 pages).

Optional second file: a `.zip` of the verification code. Only do this if you
want the code citable under the same DOI — otherwise link the repo under
*Related works* instead, which is cleaner. **Recommendation: just the PDF.**

> Files cannot be added, removed or changed after publishing. Check the PDF is
> the current build before you upload.

## Basic information

**Digital Object Identifier** — leave blank. Zenodo mints one.

**Resource type** — `Publication` → **`Preprint`**

**Title**
```
The zero forcing number of P(n,3)
```

**Publication date**
```
2026-10-04
```

**Authors/Creators**
```
Family name:  Padarthi
Given names:  Aryan
Affiliation:  Allen High School, Allen, TX, USA
ORCID:        (see note below)
```

> **Get an ORCID first** — it's free, takes two minutes at orcid.org, and it
> permanently ties this and every later paper to you rather than to a name
> string. Worth doing before you publish, not after.

**Description** — paste this:

```
In Theorem 3.6, Rashidi, Shajareh Poursalavati and Tavakkoli write that
Z(P(n,3)) = 8 for all n at least 12. Krishnan found that this statement is false
for n = 12, where Z(P(12,3)) = 7, calculated Z(P(n,3)) exhaustively for n from 7
to 20, and conjectured that Z(P(n,3)) = 8 for every n at least 13. He remarked
that what was missing was a proof of a lower bound which holds for all large n.
Here we provide that proof, and show that the conjecture holds.

Our proof is a reduction. We observe that removing the interior coordinates of
any matrix with the pattern of P(n,3) produces a single linear recurrence of
order 8, so the nullity equals the dimension of the fixed space of the monodromy
T, and is at most 8, with equality precisely when T is the identity.

We then construct matrices achieving 8 by concatenating tiles, each having a
fixed pattern for docking, so that their transfer products depend only on their
interiors. There are tiles of every length from 21 up to but not including 42,
and together they settle every n at least 21 at once. We certify each tile by
evaluating a Krawczyk contraction in exact rational arithmetic. With per-n
certificates for n from 17 to 20 and an exhaustive search for n from 13 to 16,
we have proved Z(P(n,3)) = 8 for every n at least 13. Here 13 is optimal,
because Z(P(11,3)) = Z(P(12,3)) = 7.
```

**License** — `Creative Commons Attribution 4.0 International` (CC BY 4.0).
Already the default, and the right choice: it is the standard open licence and
is compatible with later submission to arXiv or a journal.

**Copyright**
```
Copyright (C) 2026 Aryan Padarthi.
```

## Recommended information

**Contributors** — leave blank. (No acknowledgements.)

**Keywords and subjects** — add each as a separate entry:
```
zero forcing number
maximum nullity
generalized Petersen graph
minimum rank of a graph
inverse eigenvalue problem of a graph
combinatorial matrix theory
interval arithmetic
Krawczyk method
computer-assisted proof
```

**Languages**
```
eng
```

**Dates** — leave blank. The publication date above is enough.

**Version**
```
1.0.0
```

**Publisher**
```
Zenodo
```
(default — leave it)

**Funding / Awards** — leave blank.

**Alternate identifiers** — leave blank.

## Related works

Three entries. These are what make the deposit sit correctly in the literature,
so don't skip them.

| Relation | Identifier | Scheme | Resource type |
|---|---|---|---|
| **References** | `arXiv:2607.19412` | arXiv | Publication → Preprint |
| **References** | `https://github.com/the-omega-institute/trureturing/pull/10129` | URL | Software |
| **Is supplemented by** | *(your public repo URL, if you make one public)* | URL | Software |

> The third row is optional and only if you publish the code repository. If the
> repo stays private, leave that row out — don't point at a URL nobody can open.

## References

Paste these three as separate reference strings:

```
S. Rashidi, N. Shajareh Poursalavati, M. Tavakkoli, Computing the zero forcing number for generalized Petersen graphs, J. Algebra Combin. Discrete Struct. Appl. 7(2) (2020), 183-193.
```
```
A. Krishnan, A correction to the zero forcing number of the generalized Petersen graphs P(n,3), arXiv:2607.19412 (2026).
```
```
AIM Minimum Rank - Special Graphs Work Group, Zero forcing sets and the minimum rank of graphs, Linear Algebra Appl. 428 (2008), 1628-1648.
```

## Software

Leave this whole block blank unless you are depositing the code.

## Publishing information / Imprint / Thesis / Conference

Leave all blank. This is a preprint, not a journal article, book chapter,
thesis or conference paper.

---

## Before you hit publish

- [ ] ORCID created and entered
- [x] The PDF you upload is the current build (rebuild `k3_note.tex` first)
- [ ] The "Independence and related work" section says what you actually did
- [x] Commit the repo — corresponds to current state and Zenodo deposit
- [ ] Reserve or note the DOI, because the emails to Hogben and
      Gera/Stanica should carry it

## Right after you publish

Zenodo gives you two DOIs: a **version DOI** (this exact PDF) and a **concept
DOI** (all versions). **Use the concept DOI in emails and on your poster** — it
always resolves to the newest version, so a revision later doesn't break the
link.
