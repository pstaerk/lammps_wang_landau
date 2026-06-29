---
title: Home
---

# LAMMPS Wang-Landau Extension

A **Wang-Landau Monte Carlo** extension for [LAMMPS](https://www.lammps.org/), enabling efficient sampling of density-of-states and free energy calculations for molecular systems.

![Build Status](https://github.com/pstaerk/lammps_wang_landau/actions/workflows/build.yml/badge.svg)

---

## Features

- **Seamless LAMMPS integration** — drop-in `fix` styles for Wang-Landau sampling, extending the GCMC suite
- **Free energy calculations** — compute Helmholtz/Landau free energies and phase diagrams
- **Parallel sampling** — leverages LAMMPS MPI parallelization
- **Versatile** — applicable to Lennard-Jones, electrolytes, and more


## Quick Start

```bash
# 1. Get LAMMPS patch_22Dec2022
git clone https://github.com/lammps/lammps.git -b patch_22Dec2022

# 2. Copy fix sources
cp src/lammps/MC/* lammps/src/MC/

# 3. Build with MC package
cd lammps
make yes-MC
make mpi

# 4. Run an example
cd ../lammps_wang_landau/examples/lj
mpirun -np 4 lammps -in in.wang_landau
```

---

## Citation

If you use this code in academic work, please cite:

> Stärk, P. & Schlaich, A. (2026). Phase Diagram and Criticality of the Modified Primitive Electrolyte Model in Bulk and in Inert and Conducting Confinement. *The Journal of Chemical Physics*, 164(6), 064507. [doi:10.1063/5.0314875](https://doi.org/10.1063/5.0314875)

```bibtex
@article{stark26a,
  title   = {Phase Diagram and Criticality of the Modified Primitive Electrolyte Model in Bulk and in Inert and Conducting Confinement},
  author  = {St{\"a}rk, Philipp and Schlaich, Alexander},
  year    = {2026},
  journal = {The Journal of Chemical Physics},
  volume  = {164},
  number  = {6},
  pages   = {064507},
  doi     = {10.1063/5.0314875}
}

@misc{stark26b,
  title   = {Replication Data for: Phase Diagram and Criticality of the Modified Primitive Electrolyte Model in Bulk and in Inert and Conducting Confinement},
  author  = {St{\"a}rk, Philipp and Schlaich, Alexander},
  year    = {2026},
  publisher = {DaRUS},
  doi     = {10.18419/DARUS-5037}
}
```

---

## Overview

| Topic | Description |
|-------|-------------|
| [Installation](installation.md) | How to install and build |
| [Theory](theory.md) | Wang-Landau algorithm background |
| [Examples](examples.md) | Runnable simulation examples |
| [Analysis](analysis.md) | Post-processing tools |
| [Usage within LAMMPS](lammps-fixes.md) | Detailed fix documentation |

---

*Built with [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).*
