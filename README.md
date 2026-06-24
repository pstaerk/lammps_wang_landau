# LAMMPS Wang-Landau Extension

This repository contains a Wang-Landau Monte Carlo extension for LAMMPS, runnable examples, and simple analysis tooling.

## Repository layout

```text
.
├── docs/                       # installation, theory, usage, analysis notes
├── src/lammps/MC/              # fix styles integrated with LAMMPS MC package
├── examples/                   # ready-to-run input decks
├── analysis/                   # post-processing scripts/notebooks
├── tests/                      # regression/smoke checks for examples
└── .github/workflows/          # CI and release workflows
```

## Quick start

1. Use LAMMPS `patch_22Dec2022` as the base release.
2. Copy the fix sources from `src/lammps/MC/` into `lammps/src/MC/`.
3. Build LAMMPS with the `MC` package enabled.
4. Run an input from `examples/minimal/`.
5. Use scripts in `analysis/scripts/` for post-processing.

See `docs/installation.md` and `docs/examples.md` for details.

## Build testing

GitHub Actions runs `.github/workflows/build.yml` to verify that
`fix_wang_landau.cpp/.h` compile against LAMMPS `patch_22Dec2022`.

## Citation

If you use this code in academic work, please cite:

```bibtex
@article{stark26d,
  title   = {Phase Diagram and Criticality of the Modified Primitive Electrolyte Model in Bulk and in Inert and Conducting Confinement},
  author  = {St{\"a}rk, Philipp and Schlaich, Alexander},
  year    = {2026},
  month   = {feb},
  journal = {The Journal of Chemical Physics},
  volume  = {164},
  number  = {6},
  pages   = {064507},
  issn    = {0021-9606},
  doi     = {10.1063/5.0314875},
  urldate = {2026-02-13}
}
```
