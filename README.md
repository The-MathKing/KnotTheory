# Empirical Exploration of Knot-Invariant Inequalities

**Author**: Aryan Padarthi

**Public Repository**: [https://github.com/The-MathKing/KnotTheory](https://github.com/The-MathKing/KnotTheory)
**Anonymous Repository (for double-blind review)**: [https://anonymous.4open.science/status/KnotTheory-8862](https://anonymous.4open.science/status/KnotTheory-8862)

## Status (updated September 22, 2026)

This project is an **exploratory data-mining and verification pipeline** over
the KnotInfo database (12,967 knots), plus a validated computational engine
for exact invariants of positive braid closures. It is **not** a completed
proof of any conjecture. An earlier version of this README and of
`manuscript/log.tex` claimed a completed formal proof (via Khovanov homology,
$B^4$-cobordisms, and a C++ verification script) that $tr(K) \geq 2u(K) +
\max(0, |s(K)|-|\sigma(K)|)$. **That claim does not correspond to anything in
this repository**: no such proof exists in any file here, and the referenced
`src/models/audit.cpp` does not exist (only a compiled, sourceless binary
`audit` does, which cannot be independently checked or reproduced). The
project's git history records the actual sequence: an earlier "Zero-Trust ML"
architecture was proposed (`manuscript/paper.tex`), then abandoned in favor of
direct, reproducible empirical mining (commit `bfe5eaf`, "Hard Reset: Abandon
fabricated proofs for honest exploratory architecture").

On September 22, 2026 a full audit found that most of the numeric claims in
`manuscript/log.tex` did not match what the scripts behind them actually
compute, and that one experiment (`approach_1.py`) silently crashed after its
first result. **`manuscript/log.tex` Log Entry 3 documents that audit in
full**, and every entry after it is a direct, unedited transcript of a script
run, saved under `results/` and reproducible with the commands given.

## What's actually here

- **`data/`** -- raw and processed KnotInfo CSVs (12,967 knots, ~250 tabulated invariants each).
- **`src/data_ingestion/`** -- KnotInfo/NewDB parsing and an inequality-graph builder.
- **`src/experiments/`** -- 10 independent exploratory approaches (inequality-slack mining, symbolic regression on subclasses, anomaly detection, saliency analysis, extremal statistics, structural graph analysis, conjecture-violation search, derived-bound cross-validation, a positive-knot deep dive, and family/boundary robustness testing) plus 3 "deep dive" suites (15 further tests on the defect, Turaev genus, and concordance slack) that run directly against the CSV data.
- **`src/math_engine/`** -- an exact, self-validating computational engine (`braid_topology.py`) for positive braid closures: knot-ness, Rasmussen `s`, 3-genus, and signature via a from-scratch implementation of the Collins (2007) Seifert-matrix algorithm, validated against 34 torus knots and all 17 KnotInfo knots with an authentic positive-braid word. Two scripts (`investigate_braid_families.py`, `syllable_depth_proof.py`) use it to search infinite braid families for the signature defect $|s(K)|-|\sigma(K)|$.
- **`verification/`** -- standalone audit scripts. `audit_log_claims.py` recomputes 20 headline log.tex numbers from raw data and flags mismatches; `refute_3braid_claim.py` demonstrates the bug in the old (now-replaced) 3-braid signature engine and exhibits an explicit counterexample ($T(3,7)$) to a retracted claim.
- **`results/`** -- raw stdout of every script named above, one file per script, regenerated September 22, 2026. Every number in `manuscript/log.tex` after Log Entry 3 traces to one of these files.
- **`src/models/`** -- an earlier, now-inactive PyTorch/adversarial-ML architecture (see `manuscript/paper.tex`) that was proposed but not completed; kept for the record, not currently part of the reproducible pipeline described above.

## Manuscript

`manuscript/log.tex` is the primary, currently-accurate record of this
project: an honest, dated, reproducible lab notebook. `manuscript/paper.tex`
is an earlier architecture *proposal* (not a completed result) for a
"Zero-Trust" adversarial-ML framework; it predates the pivot to direct
empirical mining and should be read as background, not as a description of
the current pipeline.

## Reproducing every number in this README and in log.tex

```
python venv/bin/python src/math_engine/braid_topology.py          # engine self-test
python venv/bin/python src/experiments/approach_<1..10>.py        # each of the 10 approaches
python venv/bin/python src/experiments/run_deep_dives.py          # all 15 deep-dive tests
python venv/bin/python src/math_engine/investigate_braid_families.py
python venv/bin/python src/math_engine/syllable_depth_proof.py
python venv/bin/python verification/audit_log_claims.py           # 20-claim audit vs. raw CSV
python venv/bin/python verification/refute_3braid_claim.py        # T(3,7) counterexample
```

## Usage

The Python code uses `pandas`, `numpy`, `scikit-learn`, and `scipy`
(`src/experiments/`, `src/math_engine/`, `verification/`); `torch` and
`matplotlib` are only needed for the inactive `src/models/` architecture.
Install with `pip install -r requirements.txt` inside `venv/`.
