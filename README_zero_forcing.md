# Maximum nullity and zero forcing of cyclic covers; Ramanujan generalized Petersen graphs

Aryan Padarthi. Companion repository for the manuscript `manuscript/zf_paper.pdf`.

> This file is the README for the zero-forcing / Ramanujan project. The
> top-level `README.md` describes an earlier, unrelated knot-theory project that
> shares this working tree; see `deliverables/HANDOFF.md` for why the two should
> be separated before anything is made public.

## What is here

| Path | Contents |
|---|---|
| `manuscript/zf_paper.tex` | The paper (Part I: which P(n,k) are Ramanujan; Part II: maximum nullity and zero forcing of P(n,k) and of cyclic covers). |
| `manuscript/zf_log.tex` | Dated research log, including refuted claims with the wrong version left intact. |
| `manuscript/zf_numbers.tex`, `manuscript/ram_table.tex` | **Generated** by `verification/verify_all.py`. Never edited by hand. |
| `verification/verify_all.py` | One pass over every computational claim in the paper. Prints PASS/FAIL per check and regenerates the two files above. |
| `verification/*.py` | The individual constructions and certifiers the suite calls (tiles, Krawczyk certification in exact rational arithmetic, the Ramanujan census, cover reductions, the refutations). |
| `results/zero_forcing/` | Saved certificates (`cert_*.npy`, re-evaluated rather than trusted by the suite) and the last suite transcript `verify_all.txt`. |
| `src/zero_forcing/` | Zero forcing solvers: exhaustive C search (`c/`), CP-SAT model (`cpsat.py`), fort ILP. |
| `deliverables/` | Fair paperwork, interview preparation, the assistance record, and the handoff. |

## Reproduce every number in the paper

```
pip install -r requirements.txt
make                      # builds the C solvers, then runs every check
```

`make` is the whole of it. It builds the four exact zero-forcing solvers from
`src/zero_forcing/c/*.c` and then runs `verification/verify_all.py`, which
prints PASS/FAIL per check and regenerates `manuscript/zf_numbers.tex`. The two
steps separately, if you want them:

```
make solvers              # cc -O2, four binaries, no dependencies beyond libc
make verify               # the suite
cd manuscript && make     # typeset; fails on content pushed off the board
```

**Cost.** 141 checks, **about 5 minutes wall** (10 cores) on a 2023
Apple M2; the suite prints its own count and runtime on the last line, so a
slowdown is visible rather than discovered. Dependency versions in
`requirements.txt` are pinned to the ones that produced
`results/zero_forcing/verify_all.txt`.

Individual results, each runnable on its own:

```
python3 verification/certify_tiles.py       # Krawczyk certification of one identity tile
python3 verification/ramanujan_all_k.py     # the 460-pair Ramanujan census, exact arithmetic
python3 verification/cubic_gap_family.py    # the K4 family: span, certificate, Z by CP-SAT
python3 verification/k4_rank_one.py         # ...and the matrix that refutes the conjecture about it
python3 verification/p10_2_exact.py         # M(P(10,2))=6 by an exact integer certificate
python3 verification/cover_ceiling_counterexample.py   # star-with-a-loop and K_{2,3} refutations
```

No script contains an absolute path; every one of them locates the repository
from its own `__file__`, so a clone works wherever it is put.

Exact arithmetic (integers, rationals, cyclotomic fields) is used wherever a
decision is made; a floating-point control runs alongside with no authority and
fails the run on disagreement. Every number typeset in the paper is read off a
certificate on disk by `verify_all.py`.

## Status of claims

The paper's final section lists every claim by the standard it meets
(proved / exact certificate / interval certification / numerical / conjectural)
and every claim of ours that has been refuted or withdrawn, including the
regular-base ceiling and the $K_4$ "gap family" conjecture (refuted 1 October
2026 by `thm:k4rankone`).

## Assistance and Repository Maintenance

In accordance with fair ethics rules (ISEF Rule 8 / Form 2A), AI assistance was used for technical tooling and repository maintenance—including Git workflow, build scripting, verification harness maintenance, and documenting provenance in `deliverables/assistance_record.md`.


