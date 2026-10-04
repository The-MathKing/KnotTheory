# Explainer series — fifteen episodes, from scratch

`out/E01_….mp4` … `out/E15_….mp4` are fifteen narrated, animated episodes that
teach the whole project assuming only high-school algebra and a little
trigonometry. Every term is defined when it first appears and every definition
is followed by a worked example with real numbers that can be redone on paper
(the Petersen blocks, D₂ at n = 5, Q at n = 24, the 3-vertex kernel, the P(12,2)
certificate, Newton and Krawczyk on √2, the rank of the K4 matrix, …).

| ep | title | min |
|---|---|---|
| 1 | Graphs, and the Petersen family | 10 |
| 2 | Matrices, vectors, and eigenvalues from scratch | 13 |
| 3 | What eigenvalues tell you: random walks, the spectral gap, Ramanujan graphs | 10 |
| 4 | Why this is called a Riemann Hypothesis | 10 |
| 5 | Complex numbers, roots of unity, and how symmetry splits the matrix | 13 |
| 6 | From an eigenvalue test to a polynomial: D_k | 12 |
| 7 | The corner criterion, and why the family is finite | 18 |
| 8 | Deciding exactly, and the complete classification | 11 |
| 9 | Zero forcing: a colouring game, and why it bounds the nullity | 11 |
| 10 | Recurrences, and the exact ceiling on the matrix method | 10 |
| 11 | Rotation-invariant certificates: roots on the grid, and where they run out | 12 |
| 12 | Newton's method, interval arithmetic, and certified solutions | 11 |
| 13 | Tiles: from each n to every n | 10 |
| 14 | Covers, the K4 family, and a refutation | 10 |
| 15 | What is proved, what is open, and how the numbers are trusted | 8 |

Total 171 minutes (2 h 51 min), 375 MB.

The one-hour overview in the parent directory (`../Where_Optimal_Networks_Stop_Existing.mp4`)
assumed linear algebra; this series replaces it for a first viewing.

## How it is made

- `scripts/E01.md` … `E15.md` — narration, one `## E01S01 — title` heading per
  scene, numbered beats. Edit these to change what is said.
- `tts.py` — one WAV per beat with the Kokoro voice (runs in `../tts_venv`,
  Python 3.12; cached by text hash). Writes `audio/durations.json`, which the
  scenes read to time themselves.
- `scenes/lib.py` — palette, `BeatScene` (one beat = one narration clip +
  animations + hold), definition/example/idea cards, graph drawing, TeX setup
  (through `bin/pdflatex`, a retrying wrapper around tectonic; each render
  process gets its own TeX scratch directory so parallel renders do not race).
- `scenes/e01.py` … `e15.py` — the scenes, class names `E01S01` etc.
- `render.sh E01 [E02 …]` — renders every scene of those episodes at 1080p30,
  three at a time (`QUALITY=l` for 480p15 previews).
- `assemble.py E01 [E02 …]` — concatenates one episode's scenes with chapter
  markers into `out/`.

Rebuild from scratch:

    ../tts_venv/bin/python tts.py          # narration (≈25 min)
    ./render.sh E01 E02 … E15              # animation (≈3 h)
    python3 assemble.py E01 E02 … E15      # final files

Preview one scene: `source ../../venv/bin/activate && manim -ql scenes/e05.py E05S05`.

## Honesty note

Narration and animation code are AI-written (recorded in
`deliverables/assistance_record.md`). The videos are study material for the
author and explanation for mentors, not a submission artifact; every claim in
them is a claim of the paper, with the paper's status label, and the worked
numbers were computed and checked before being read aloud.
