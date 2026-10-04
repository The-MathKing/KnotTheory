# Explainer videos

**Start with `series/`** — fifteen episodes (≈2 h 50 min) that assume only
high-school algebra and define every term with a worked example; see
`series/README.md`. The one-hour overview below assumes linear algebra.

## The one-hour overview (1 October)

`Where_Optimal_Networks_Stop_Existing.mp4` is a narrated, animated walk through
the whole project (both parts, the K4 refutation, status of claims).

How it is made:

- `SCRIPT.md` — the narration, one `## Sxx` heading per scene, numbered beats.
  Edit this to change what is said.
- `tts.py` — turns each beat into `audio/Sxx_nn.wav` with the Kokoro voice
  (runs in `tts_venv`, Python 3.12; cached by text hash, so only edited beats
  are regenerated). Writes `audio/durations.json`, which the scenes read to
  time themselves.
- `scenes/lib.py` — shared palette, the `BeatScene` base class (one beat =
  one narration clip + animations + hold), `petersen(n,k)` drawing, and the
  TeX setup. TeX goes through `bin/pdflatex`, a wrapper around tectonic.
- `scenes/partA.py` … `partD.py` — the 31 scenes, S01–S31.
- `render.sh` — renders every scene at 1080p30 into `media/videos/`.
- `assemble.py` — concatenates them with chapter markers into the final MP4.

Rebuild from scratch:

    tts_venv/bin/python tts.py        # narration (≈10 min)
    ./render.sh                       # animation (≈40 min)
    python3 assemble.py               # final file

To preview one scene quickly:

    source ../venv/bin/activate && manim -ql scenes/partB.py S12
