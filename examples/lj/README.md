# Lennard-Jones Wang-Landau Example

A minimal example demonstrating the Wang-Landau Monte Carlo method for a neutral Lennard-Jones fluid.

## System

- **Particles**: Neutral Argon-like atoms (LJ σ=3.0 Å, ε=0.238 kcal/mol)
- **Ensemble**: NVT with Wang-Landau flat-histogram sampling
- **Box**: 25×25×25 Å³ with periodic boundaries
- **Temperature**: 300 K

## Files

- `in.lj_wang_landau` - LAMMPS input script

## Running

```bash
# Assuming LAMMPS is built with the MC package:
mpirun -np 4 lammps < in.lj_wang_landau
```

## Output

The simulation produces:

- `qs.dat` - Density of states file containing:
  - Column 1: Particle number N
  - Column 2: ln[g(N)] (logarithm of the density of states)
  - Column 3: Histogram counts

## Method

The `fix wang_landau` performs Grand Canonical Monte Carlo (GCMC) moves:
- **Translation**: Random displacement of existing particles
- **Insertion**: Add particles with acceptance based on chemical potential
- **Deletion**: Remove particles with acceptance based on chemical potential

The Wang-Landau algorithm adaptively builds the density of states g(N) by accepting/rejecting moves based on the ratio g(N_old)/g(N_new). The modification factor f is gradually reduced until the histogram is flat.

## Citation

If you use this example in academic work, please cite the [Wang-Landau extension paper](../README.md#citation).
