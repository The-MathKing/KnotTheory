# Adversarial Heuristics in Algebraic Topology
**Author**: Aryan Padarthi

**Public Repository**: [https://github.com/The-MathKing/KnotTheory](https://github.com/The-MathKing/KnotTheory)  
**Anonymous Repository (for double-blind review)**: [https://anonymous.4open.science/status/KnotTheory-8862](https://anonymous.4open.science/status/KnotTheory-8862)

This repository contains the full computational pipeline and manuscript for resolving the Trivializing Gap via Zero-Trust Machine Learning. The project utilizes a deep feedforward neural network as an adversarial heuristic to navigate the topological blind spots of classical database metrics.

## Abstract
The Trivializing Number Conjecture posits that the trivializing number $tr(K)$ is exactly twice the unknotting number $2u(K)$ for positive knots. Proving deviations where $tr(K) > 2u(K)$ requires identifying specific topological obstructions, a task often resistant to classical linear transitivity bounds. Utilizing a strictly partitioned "Zero-Trust" framework, we deployed deep neural networks explicitly as an adversarial heuristic over the Jabłonowski (2026) NewDB. By penalizing linear correlations, the network isolated non-linear defect interactions between the Rasmussen $s$-invariant and the knot signature $\sigma(K)$. We then abandoned the computational environment to formally prove via Khovanov homology, cobordisms in $B^4$, and the Euler characteristic that $tr(K) \geq 2u(K) + \max(0, |s(K)| - |\sigma(K)|)$. An optimized C++ script confirmed zero violations across all tested configurations.

## Code Architecture
- `src/data_ingestion/`: Contains SageMath bindings for evaluating topological matrices.
- `src/models/dataset.py`: PyTorch dataset class targeting specific defect structures.
- `src/models/objectives.py`: The adversarial loss function formulation masking linear correlations.
- `src/models/cross_compile.py`: Symbolic regression engine for synthesizing equations.
- `src/models/audit.cpp`: High-speed C++ script to cross-examine topological relations against the NewDB.
- `src/models/visualize.py`: Asset generation for topological models and gradient saliency heatmaps.

## Manuscript
The `manuscript/` directory contains the final `paper.tex` and compiled `paper.pdf` detailing the full formal proof and execution pipeline.

## Usage
The Python code utilizes `torch`, `numpy`, `pandas`, and `matplotlib`. Ensure these dependencies are installed in your environment before execution.
