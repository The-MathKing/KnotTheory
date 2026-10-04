"""Build the clean zero-forcing repository (COMPLETION_PLAN tasks E1, E2).

Why this exists. The current repository's `origin` is
`The-MathKing/KnotTheory`, its README is the knot project, its history contains
commits like "Abandon fabricated proofs", its `requirements.txt` asks for
torch/snappy/xlrd (none of which this project uses), and it carries a 1.4 GB
`venv/`. None of that is something to hand a judge or a referee. E1 asks for a
new repository with fresh history containing only this project.

This is a script rather than a sequence of `cp` commands so that what the clean
repository contains is auditable and reproducible: the manifest below is the
definition, and anyone can re-run it and diff the result.

What is deliberately EXCLUDED, and why:

  * `venv/`, `*.aux`, `*.out`, `*.log`, `*.bak`, `temp_united.pdf`, `__pycache__`
    -- build and environment junk (E2).
  * `src/experiments/`, `src/models/`, `src/math_engine/`, `src/octal_games/`,
    `src/data_ingestion/` -- the knot-theory and octal-games code (E2).
  * Nine files in `verification/` that belong to those other projects:
    the braid/Turaev group, the two octal-games scripts, and
    `audit_log_claims.py` (which reads the KnotInfo CSV). They are listed
    explicitly in DROP_VERIFICATION rather than matched by pattern, so that
    nothing is removed by accident.
  * The knot project's manuscripts (`paper.tex`, `log.tex`, `octal_log.tex`,
    `isef_paper.tex`, `poster.tex`, ...) and two leftover figures
    (`saliency_heatmap.png`, `seifert_defect.png`).
  * The compiled C solvers (`zf`, `zfp`, `zfboot`, `zfgen`). Their sources are
    kept and a Makefile is generated, because a committed binary is
    platform-specific and cannot be reviewed.

What is NOT decided here: the LICENSE. Choosing a licence has legal effect and
is the author's call, so this script writes no licence file and reports it as
the one thing left to add by hand.

Usage:
    python3 tools/make_clean_repo.py [--dest DIR] [--git]

`--git` initialises a fresh repository and makes no commit; committing is E5,
which the plan assigns to the author after reading the diff.
"""

import argparse
import os
import pathlib
import shutil
import subprocess
import sys

SRC = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_DEST = SRC.parent / "zero-forcing-covers"

#: verification/*.py that belong to the knot-theory or octal-games projects
DROP_VERIFICATION = {
    "audit_log_claims.py",            # reads the KnotInfo CSV
    "explore_n_strand_pattern.py",
    "extend_n_strand_mechanism.py",
    "investigate_octal_45.py",
    "prove_octal_45_periodicity.py",
    "prove_syllable_turaev_formula.py",
    "refute_3braid_claim.py",
    "refute_turaev_braid_bound.py",
    "test_3braid_signature_bound.py",
}

#: figures that are leftovers from the other projects
DROP_FIGURES = {"saliency_heatmap.png", "seifert_defect.png"}

#: compiled solvers -- sources are kept, binaries are not
DROP_BINARIES = {"zf", "zfp", "zfboot", "zfgen"}

JUNK_SUFFIX = {".aux", ".out", ".log", ".bak", ".pyc", ".DS_Store"}
JUNK_NAME = {"temp_united.pdf", ".DS_Store"}

REQUIREMENTS = """\
# Pinned to the versions the recorded verify_all.py output was produced with
# (COMPLETION_PLAN E4). numpy/scipy/sympy/mpmath carry the mathematics;
# ortools provides the CP-SAT zero-forcing solver; matplotlib draws the
# figures; networkx is used by one check; pymupdf assembles the binder.
numpy==2.5.2
scipy==1.18.1
sympy==1.14.0
mpmath==1.3.0
ortools==9.15.6755
matplotlib==3.11.1
networkx==3.6.1
pymupdf==1.28.2
"""

C_MAKEFILE = """\
# Build the exact zero-forcing solvers. `verify_all.py` invokes ./zf and ./zfp,
# so these must exist before the suite runs; `make` at the repository root
# builds them (COMPLETION_PLAN E3).
CC     ?= cc
CFLAGS ?= -O2 -march=native -pthread

BINS = zf zfp zfboot zfgen

all: $(BINS)

%: %.c
\t$(CC) $(CFLAGS) -o $@ $<

clean:
\trm -f $(BINS)

.PHONY: all clean
"""

ROOT_MAKEFILE = """\
# One-command reproduce (COMPLETION_PLAN E3).
#
#   make solvers   build the C zero-forcing solvers
#   make verify    run every check in the paper
#   make           both
#
# A clean clone needs:  pip install -r requirements.txt && make

PY ?= python3

all: solvers verify

solvers:
\t$(MAKE) -C src/zero_forcing/c

verify: solvers
\t$(PY) verification/verify_all.py

clean:
\t$(MAKE) -C src/zero_forcing/c clean

.PHONY: all solvers verify clean
"""


def is_junk(p: pathlib.Path) -> bool:
    return (p.suffix in JUNK_SUFFIX or p.name in JUNK_NAME
            or "__pycache__" in p.parts or p.name.endswith(".tex.bak"))


def copy_tree(src: pathlib.Path, dst: pathlib.Path, skip=lambda p: False):
    n = 0
    for s in sorted(src.rglob("*")):
        if s.is_dir():
            continue
        rel = s.relative_to(src)
        if is_junk(s) or skip(rel):
            continue
        d = dst / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, d)
        n += 1
    return n


def build(dest: pathlib.Path, do_git: bool):
    if dest.exists():
        print(f"refusing to overwrite existing {dest}")
        print("remove it first, or pass --dest elsewhere")
        return 1
    dest.mkdir(parents=True)
    report = []

    # verification/
    n = copy_tree(SRC / "verification", dest / "verification",
                  skip=lambda r: r.name in DROP_VERIFICATION)
    report.append(("verification/", n, f"{len(DROP_VERIFICATION)} other-project files dropped"))

    # src/zero_forcing/
    n = copy_tree(SRC / "src" / "zero_forcing", dest / "src" / "zero_forcing",
                  skip=lambda r: r.name in DROP_BINARIES)
    report.append(("src/zero_forcing/", n, "compiled solvers dropped, sources kept"))

    # results/zero_forcing/
    n = copy_tree(SRC / "results" / "zero_forcing",
                  dest / "results" / "zero_forcing")
    report.append(("results/zero_forcing/", n, "certificates"))

    # deliverables/
    n = copy_tree(SRC / "deliverables", dest / "deliverables")
    report.append(("deliverables/", n, ""))

    # manuscript/: zf_* plus the shared pieces, minus the other projects'
    man_src, man_dst = SRC / "manuscript", dest / "manuscript"
    man_dst.mkdir(parents=True, exist_ok=True)
    keep_extra = {"ram_table.tex", "fig_ramclass.pdf", "Makefile"}
    n = 0
    for s in sorted(man_src.iterdir()):
        if s.is_dir() or is_junk(s):
            continue
        if s.name.startswith("zf_") or s.name in keep_extra:
            shutil.copy2(s, man_dst / s.name)
            n += 1
    nf = copy_tree(man_src / "figures", man_dst / "figures",
                   skip=lambda r: r.name in DROP_FIGURES)
    report.append(("manuscript/", n, "zf_* plus ram_table/fig_ramclass/Makefile"))
    report.append(("manuscript/figures/", nf, f"{len(DROP_FIGURES)} leftover figures dropped"))

    # README, requirements, Makefiles
    readme = SRC / "README_zero_forcing.md"
    if readme.exists():
        shutil.copy2(readme, dest / "README.md")
        report.append(("README.md", 1, "from README_zero_forcing.md"))
    else:
        report.append(("README.md", 0, "MISSING: README_zero_forcing.md not found"))

    (dest / "requirements.txt").write_text(REQUIREMENTS, encoding="utf-8")
    report.append(("requirements.txt", 1, "pinned, 8 real dependencies"))

    (dest / "src" / "zero_forcing" / "c" / "Makefile").write_text(
        C_MAKEFILE, encoding="utf-8")
    (dest / "Makefile").write_text(ROOT_MAKEFILE, encoding="utf-8")
    report.append(("Makefile", 2, "root + C solvers (E3 build step)"))

    (dest / ".gitignore").write_text(
        "__pycache__/\n*.pyc\n*.aux\n*.out\n*.log\n*.bak\n"
        "venv/\n.DS_Store\n"
        "src/zero_forcing/c/zf\nsrc/zero_forcing/c/zfp\n"
        "src/zero_forcing/c/zfboot\nsrc/zero_forcing/c/zfgen\n",
        encoding="utf-8")
    report.append((".gitignore", 1, "ignores build output incl. the solvers"))

    print(f"\nclean repository written to {dest}\n")
    print(f"{'path':<26} {'files':>6}  note")
    for path, cnt, note in report:
        print(f"{path:<26} {cnt:>6}  {note}")

    total = sum(1 for p in dest.rglob("*") if p.is_file())
    size = sum(p.stat().st_size for p in dest.rglob("*") if p.is_file())
    print(f"\ntotal: {total} files, {size/1e6:.1f} MB"
          f"  (source tree is 1500 MB)")

    if do_git:
        subprocess.run(["git", "init", "-q"], cwd=dest, check=True)
        subprocess.run(["git", "add", "-A"], cwd=dest, check=True)
        print("\ngit: fresh repository initialised, files staged, NOT committed")
        print("     (committing is E5 -- read the diff first)")

    print("\nSTILL TO DO BY HAND:")
    print("  * LICENSE -- not written by this script. Choosing a licence has")
    print("    legal effect; pick one yourself (MIT and CC-BY-4.0 are the")
    print("    usual choices for code + manuscript respectively).")
    print("  * Verify the one-command reproduce on a clean clone (E3):")
    print("      pip install -r requirements.txt && make")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", default=str(DEFAULT_DEST))
    ap.add_argument("--git", action="store_true")
    a = ap.parse_args()
    return build(pathlib.Path(a.dest).resolve(), a.git)


if __name__ == "__main__":
    sys.exit(main())
