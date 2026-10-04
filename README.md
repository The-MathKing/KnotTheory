# Maximum Nullity and Zero Forcing of Cyclic Covers; Ramanujan Generalized Petersen Graphs

**Author**: Aryan Padarthi  
**Repository**: [https://github.com/The-MathKing/KnotTheory](https://github.com/The-MathKing/KnotTheory)  
**Preprint ($k=3$ Zero Forcing)**: [DOI: 10.5281/zenodo.23140891](https://doi.org/10.5281/zenodo.23140891)  

---

## Overview

This repository contains the computational infrastructure, manuscripts, and exact verification suites for research on graph spectra, zero forcing, and topological invariants across generalized Petersen graphs $P(n,k)$ and cyclic covers.

The project consists of two core mathematical investigations (October 2026), built upon an empirical topology and knot-invariant foundation (May–September 2026):

1. **Part II: Zero Forcing and Maximum Nullity of Cyclic Covers** (`manuscript/zf_paper.tex`, `deliverables/k3_note.tex`)
   - **Proof of Krishnan's Conjecture 5**: Proves $Z(P(n,3)) = M(P(n,3)) = 8$ for all $n \ge 13$, resolving the open conjecture from arXiv:2607.19412 and settling the stabilization threshold.
   - **Monodromy Ceiling**: Eliminates the internal coordinates of any symmetric matrix on a cyclic cover to yield a closed recurrence of order $2k+2$.
   - **Certified Identity Tiles**: Exact rational Krawczyk contraction certificates proving tile existence and establishing large-$n$ stabilization for $k=2,3,4$.
   - **All-$k$ Controllability**: Submersion and discrete Wronskian analysis for identity tile families across large lengths.

2. **Part I: Ramanujan Generalized Petersen Graphs & Ihara Zeta Functions** (`manuscript/zf_ramanujan.tex`)
   - **Forbidden Corner Criterion**: Reduction of the algebraic Ihara condition $D_k \ge 0$ to a $k$-independent forbidden region $Q(x,y) = 4x^2 + 4y^2 - 8\sqrt{2}|xy| + 3 \ge 0$.
   - **Dirichlet Absolute Finiteness**: Dirichlet's approximation theorem forces failure once $n \ge 231$ for every $k$, establishing finiteness in both parameters.
   - **Exact Classification**: Complete census (460 pairs, 324 isomorphism classes, none with $k > 45$) certified in exact arithmetic.

3. **Historical Foundation: Knot Invariants & Braid Topology** (`src/math_engine/`, `src/experiments/`)
   - Data mining across 12,967 KnotInfo knots and an exact Seifert-matrix engine (Collins 2007) for positive braid closures.

---

## Directory Structure

| Directory / File | Contents |
|---|---|
| `deliverables/` | Science fair deliverables, research binder, interview preparation, Zenodo preprint metadata, and the assistance record. |
| `deliverables/k3_note.pdf` | Dedicated 5-page standalone preprint proving Krishnan's Conjecture 5. |
| `deliverables/assistance_record.md` | Comprehensive provenance log detailing student vs. assisted contributions. |
| `manuscript/` | LaTeX source and compiled PDFs for the comprehensive paper (`zf_paper.pdf`), research log (`zf_log.pdf`), foundations guide (`zf_guide.pdf`), poster (`zf_poster.pdf`), and presentation slides. |
| `verification/` | Exact rational arithmetic verification scripts, certificate checkers, and Krawczyk certifiers. |
| `verification/verify_all.py` | Standalone test suite executing 146 checks in exact arithmetic with zero external authority. |
| `src/zero_forcing/` | Zero forcing solvers: exhaustive C search (`c/`), CP-SAT constraint models, and fort ILP. |
| `video/series/` | 15-episode mathematical explainer animation series (Manim scene scripts and TTS generation pipelines). |
| `results/zero_forcing/` | Saved certificate arrays (`.npy`), verification logs, and census tables. |

---

## Reproducibility & Verification

To reproduce every computational claim and number in the manuscripts:

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Build C zero-forcing solvers
make solvers

# 3. Run the full verification test suite (146 checks, exact arithmetic)
python3 verification/verify_all.py
```

All decision-making scripts use exact arithmetic (integers, rationals, cyclotomic field operations) rather than floating-point approximations. Numbers typeset into the manuscripts (`manuscript/zf_numbers.tex`, `manuscript/ram_table.tex`) are generated automatically by `verification/verify_all.py`.

---

## AI Assistance & Repository Maintenance Disclosure

In compliance with science fair ethics rules (including **ISEF Rule 8** and **Student Support Disclosure Form 2A**):

- **Repository Maintenance & Tooling**: Generative AI assistance (Claude / DeepMind Antigravity) was used as technical tooling for Git repository maintenance, commit staging and organization, `.gitignore` configuration, build automation scripts, and formatting assistance.
- **Provenance Documentation**: A complete, itemized record of all computational and AI assistance—differentiating student-originated mathematical theorems from exploratory tooling and code—is documented in [deliverables/assistance_record.md](deliverables/assistance_record.md).
- **Core Research**: All scientific directions, mathematical proofs, paper revisions, and presentation materials reflect the researcher's independent work and understanding.
