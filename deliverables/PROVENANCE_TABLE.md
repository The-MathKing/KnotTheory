# Provenance of every numbered result

Purpose: so you know, per result, whether you may present it as your own work,
and what you must do before you can.

## How this was determined

Two independent methods, which agree exactly.

1. **Git boundary.** The last commit before the AI sessions is `dc2a6cf`
   (28 Sep 2026). Any `\label` in `manuscript/zf_paper.tex` that is absent there
   and present now was added in the 29 Sep – 3 Oct window. This method is
   **objective** and needs no one's recollection.
2. **The assistance record.** `assistance_record.md` §1 (yours), §2, §5, §6, §9,
   §9b (AI).

For `zf_paper.tex` the two methods produce **the same 13 labels**. That
agreement is the reason to trust the record elsewhere.

**Caveat.** `zf_ramanujan.tex` was untracked at `dc2a6cf`, so method 1 cannot be
applied to Part I; those rows rest on the record alone, plus the 28 Sep abstract,
which already contained `lem:signs`, `thm:uniform`, `thm:finite`, `thm:parity`
and the 247-graph classification.

## Key

| Mark | Meaning | What you must do |
|---|---|---|
| **Y** | Yours. Predates the AI sessions. | Nothing. Present freely. |
| **A** | AI-originated: statement and proof both. | Re-derive, rewrite in your words, and be able to prove it at a whiteboard — or cut it. |
| **A-fix** | Yours, but AI supplied a missing hypothesis or correction. | Present as yours; know and be able to state the correction. |
| **Ext** | Someone else's published result, cited. | Cite. Never present as yours. |

---

## Part II — `manuscript/zf_paper.tex`

### Yours (45 labels, all present on 28 Sep)

`conj:generaln`, `cor:ceiling`, `cor:excluded`, `cor:niven`, `lem:boot`,
`lem:close`, `lem:concat`, `lem:slice`, `lem:tile`, `obs:fulldim`, `obs:gcd`,
`obs:symp`, `prop:SU`, `prop:exh`, `prop:k2closed`, `prop:ratobs`, `prop:reach`,
`prop:symbol`, `rem:scope`, `rem:tilerank`, `thm:DP`, `thm:I`, `thm:adjclass`,
`thm:antipodal`, `thm:certvals`, `thm:complete`, `thm:congbound`,
`thm:coverattain`, `thm:cyclo`, `thm:k2all`, `thm:k3`, `thm:k3all`,
`thm:k3krishnan`, `thm:k5all`, `thm:k6`, `thm:k6imp`, `thm:k7`, `thm:order`,
`thm:p17`, `thm:realis`, `thm:red`, `thm:red2`, `thm:signedadj`, `thm:theta`,
`thm:tiling`

This includes everything that matters most: the monodromy ceiling (`thm:red`),
the rotation bootstrap, the tiling construction, the exact-arithmetic Krawczyk
certification, the complete determination at k = 2, 3, 4 (`thm:complete`), and
**the proof of Krishnan's Conjecture 5** (`thm:k3krishnan`).

### `thm:cover` — **A-fix**

Yours (record §1). AI added the missing hypothesis det M(ζ) ≢ 0, without which
the theorem is false. Present as yours; be ready to say why the hypothesis is
needed and what breaks without it.

### AI-originated (13 labels, added 29 Sep – 3 Oct)

| Label | What it is | Status |
|---|---|---|
| `thm:redpath` | Ceiling on path-with-loops bases | **A** |
| `thm:redcycle` | Ceiling on cycle bases | **A** |
| `thm:cexcover` | The arbitrary-base ceiling fails | **A** |
| `rem:mindeg` | Min-degree-2 repair also fails | **A** |
| `prop:indobs` | Independent-set obstruction | **A** |
| `cor:regblocks` | Why regularity blocks it | **A** |
| `prop:lowrank` | Low-rank-subgraph obstruction | **A** |
| `prop:k4cert` | Integer certificate at the span | **A** |
| `prop:k4z` | Z = n+2 grows | **A** |
| `thm:k4rankone` | **The refutation** of the cubic gap family | **A** |
| `conj:leading` | Leading-coefficient criterion (replacement conjecture) | **A** |
| `thm:ratclass` | Classification of rational-symbol certificates | **A** |
| `rem:twoexc` | M(P(10,2)) = 6 | **A** |

---

## Part I — `manuscript/zf_ramanujan.tex`

### Yours

| Label | What it is |
|---|---|
| `thm:crit`, `cor:crit` | The criterion D_k ≥ 0; clearing both radicals by equivalences |
| `lem:signs` | D_k(1) = −7, D_k(−1) = −7 or 9, D_k(0) ≥ 17 |
| `thm:uniform` | Uniform finiteness: n ≤ π(2+√2)√(k²+1) |
| `thm:finite` | Per-k finiteness: n ≤ 2π/arccos u_k |
| `thm:parity` | **The parity law** |
| `thm:ramclass` | Classification per k, k ≤ 10 — the 247 graphs |
| `thm:corner`, `cor:lens` | **The corner theorem.** Record §1: "the single prettiest idea in Part I"; AI contribution was verification only |

### External

| Label | Source |
|---|---|
| `thm:grh` | Ihara determinant formula — Terras |
| `lem:blocks` | P(n,k) spectrum — Gera & Stănică 2011, Thm 2.4 |

### AI-originated

| Label | What it is |
|---|---|
| `thm:absolute` | Absolute finiteness: n ≥ 231 fails for every k (Dirichlet) |
| `thm:allk` | Complete classification: 460 pairs, 324 classes, nothing past k = 45 |
| `thm:local` | Locality at divisors |
| `cor:divclosed` | Divisor closure |
| `lem:mingcd` | min‖jc/m‖ = gcd(c,m)/m |
| `thm:gcdsafe` | Gcd safety |
| `prop:closedsmall` | Closed form for k ≤ 9 |
| `lem:bands` | Band structure (Sturm root isolation) |
| `thm:covcorner` | Corner criterion on a two-loop base |
| `thm:thetarh` | Theta base |
| `thm:covfinite` | Uniform finiteness on both bases |
| `thm:noinfinite` | No infinite Ramanujan family is a cyclic cover |
| `prop:deficit` | The deficit δ* and its 3−2√2 bound |

---

## Totals

| | Yours | AI | External |
|---|---|---|---|
| Part II (`zf_paper.tex`) | 45 + 1 A-fix | 13 | — |
| Part I (`zf_ramanujan.tex`) | 9 | 13 | 2 |
| **Total** | **54** | **26** | **2** |

**Roughly two-thirds of the numbered results are yours, and they include every
headline claim**: the monodromy ceiling, the complete determination at
k = 2, 3, 4, the proof of Conjecture 5, the uniform finiteness bound, the parity
law, the 247-graph classification, and the corner theorem.

## What follows from this

1. **A nine-page paper of your own results is already available.** Take the Y
   rows only. Nothing in the AI column is needed for any headline claim.
2. **The AI column is severable.** No Y result depends on an A result. The one
   coupling is `thm:cover`, which needs its hypothesis — and that is a one-line
   addition you can state and defend yourself.
3. **Prose is a separate problem from authorship.** Many Y results are currently
   written up in AI-drafted sentences (record §2, "Writing"). A Y mark means the
   mathematics is yours, not that the paragraph is. The poster, abstract and
   research plan must be rewritten regardless of what the table says.
4. **If you keep any A row**, you must re-derive it, write it in your own words,
   and be able to prove it at a whiteboard under questioning. If you cannot do
   that for a given row, cut it. Keeping it is worse than not having it.
