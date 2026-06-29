---
title: Examples
---

# Examples
Examples are meant to showcase how to use the package and how to setup the 
multi-step simulation runs.

Examples are organized by increasing complexity:

- `examples/lj/`: One single Wang-Landau iteration for a simple Lennard-Jones 
fluid
- `examples/lj_iterative/`: Multiple iterations of the WL-algorithm with
  sequential refinement, including a simple python script, `run_wang_landau.py`
  for orchestrating and example outputs as well as a plotting script
  `plot_wang_landau.py` for grand potential analysis.
  
  ![Example of the results of the sequential Wang-Landau run for various
   .chemical potentials.](assets/wang_landau_omega.png)

Each folder should contain:

- `in.*` LAMMPS input
- `qs.dat` Histogram output file.
- short `README.md` with description of inputs and outputs
