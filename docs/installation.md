---
title: Installation
---

# Installation

This repository tracks Wang-Landau fixes intended for the LAMMPS `MC` package.
Base version: `patch_22Dec2022` (commit hash `8b8c0ee72d7460fafdfdb4132e06a53`).
Newer versions might work too, but have not been tested. PRs are welcome.

## Integrate into LAMMPS MC package

1. Clone LAMMPS and check out `patch_22Dec2022`.
2. Copy `src/lammps/MC/fix_wang_landau.h` and `src/lammps/MC/fix_wang_landau.cpp`
   from this repository into `lammps/src/MC/`.
3. Build LAMMPS with the `MC` package enabled.
4. Run one of the provided `examples/*/in.*` files.
5. Use the method for your own use-cases
