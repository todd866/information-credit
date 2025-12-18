# State Credit and Protocol Efficiency: A Decomposition of Sub-Landauer Dissipation

**Target journal:** JSTAT
**Status:** In preparation

## Abstract

Landauer's bound is often stated as a fixed cost per bit erased. The correct bound depends on entropy removed, which can be significantly less than the bit-count when the system or its environment carries structure. We show that apparent sub-Landauer episodes decompose into two distinct mechanisms: (i) *state credit*—bias (negentropy) and correlations (mutual information) that reduce the reversible work bound and obey a conservation law; and (ii) *protocol efficiency*—geometric structure in control space (thermodynamic length) that reduces irreversible dissipation but is not itself conserved. This decomposition yields a combined finite-time bound unifying information-theoretic and geometric contributions.

## Key Results

- **State credit** is conserved: ΔC ≤ W_in/(kT ln 2)
- **Combined bound**: W ≥ kT ln 2 [H_max - C_state] + kT L²/(2τ)
- Worked example: 0.83 bits credit → 0.23 kT total work (vs 0.69 kT naive)

## Repository Structure

```
├── paper/
│   └── information_credit.pdf      # Current PDF
├── archive/latex/
│   ├── information_credit.tex      # LaTeX source
│   ├── references.bib              # Bibliography
│   ├── figures/                    # Figure PDFs
│   └── old_versions/               # Previous drafts
└── src/
    └── make_figures.py             # Figure generation script
```

## Building

Generate figures:
```bash
python3 src/make_figures.py
```

Build PDF (requires LaTeX):
```bash
cd archive/latex
pdflatex information_credit && bibtex information_credit && pdflatex information_credit && pdflatex information_credit
```

## Related Work

This paper continues the analysis from:
- Todd, I. (2025). "Timing Inaccessibility and the Projection Bound: Resolving Maxwell's Demon for Continuous Biological Substrates." *BioSystems* 258:105632.

## Interactive Demo

An interactive simulation of the credit ledger is available at:
https://coherencedynamics.com/simulations/credit-ledger

## License

MIT License. See LICENSE file.

## Citation

```bibtex
@article{todd2025credit,
  author = {Todd, Ian},
  title = {State Credit and Protocol Efficiency: A Decomposition of Sub-Landauer Dissipation},
  journal = {JSTAT},
  year = {2025},
  note = {In preparation}
}
```
