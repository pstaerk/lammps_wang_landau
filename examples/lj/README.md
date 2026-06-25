# Lennard-Jones Wang-Landau Example

A minimal example demonstrating the Wang-Landau Monte Carlo method for a neutral Lennard-Jones fluid.

## System

- **Particles**: Neutral Argon-like atoms (LJ σ=3.0 Å, ε=0.238 kcal/mol)
- **Ensemble**: NVT with Wang-Landau flat-histogram sampling
- **Box**: 25×25×25 Å³ with periodic boundaries
- **Temperature**: 300 K

## Files

While the majority of the theory is described in the docs, here we briefly state what you need to know to understand this simple Wang-Landau run.
The method, as implemented, updates the density of states estimates at every call to the Wang-Landau subroutine (every call to the LAMMPS "fix").
The run will stop when it hits the accuracy criterion.
As we keep track of the density of states via the logarithm (this is much easier to handle), we initialize the density of states to 1.
As such, before the run, we provide a file called `qs.dat` (hard-coded name), given in the following format:

- `qs.dat` - Density of states file containing:
  - Column 1: Particle number N
  - Column 2: ln[g(N)] (logarithm of the density of states, initialized to 1.0)
  - Column 3: Histogram counts
Thus, the example provided here takes in:

- `in.lj_simple` - LAMMPS input script
- `qs.dat` - Initial density of states file (will be overwritten with results)

Running the script via

```bash
# Assuming LAMMPS is built with the MC package:
lmp -in in.lj_simple
```

then starts a LAMMPS sampling run until the "flatness criterion" is met.

To start a new run to refine results, one would then re-set the histogram column to 0, keep the current estimate for the density of states.

The Wang-Landau algorithm adaptively builds the density of states g(N) by accepting/rejecting moves based on the ratio g(N_old)/g(N_new). The modification factor f is gradually reduced until the histogram is flat.

## Citation

If you use this example in academic work, please cite the [Wang-Landau extension paper](../README.md#citation).
