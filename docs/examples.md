---
title: Examples
---

# Examples

Examples are organized by increasing complexity:

- `examples/lj/`: One single Wang-Landau iteration for a simple Lennard-Jones 
fluid
- `examples/lj_iterative/`: Multiple iterations of the WL-algorithm with
  sequential refinement, including `run_wang_landau.py` orchestrator and
  `plot_wang_landau.py` for grand potential analysis.
  
  ![Grand Potential](../assets/wang_landau_omega.png)

Each folder should contain:

- `in.*` LAMMPS input
- `qs.dat` Histogram output file.
- short `README.md` with description of inputs and outputs
