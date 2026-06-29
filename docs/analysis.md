---
title: Analysis
---

# Analyzing Wang-Landau Output

After a Wang-Landau run, the fix writes the estimated density of states to a file
called `qs.dat`. This page describes the file format, the thermodynamic
quantities you can derive from it, and the small Python package shipped in
`analysis/scripts/wang_landau/` that does the work for you.

## The `qs.dat` file

`qs.dat` is a whitespace-separated text file with three columns and optional `#`
comments:

| Column | Meaning                         |
|--------|---------------------------------|
| 1      | Particle number `N`             |
| 2      | Estimate of `ln g(N)`           |
| 3      | Visitation histogram `h(N)`     |

The histogram refers to the *last* iteration only (it is reset between
iterations, see [theory](theory.md)). The `ln g(N)` column carries over and is
refined across iterations, so the final iteration's `qs.dat` is the converged
result.

## From `ln g(N)` to thermodynamics

With `ln g(N)` in hand, the quantities of interest are direct (see
[theory](theory.md) for derivations):

- **Helmholtz free energy**

    $$F(N) = -k_B T \ln g(N) + c$$

- **Grand (Landau) potential** for a reservoir chemical potential $\mu$

    $$\Omega(N, \mu) = F(N) - \mu N$$

- **Equilibrium particle number**, obtained by minimizing the grand potential:

    $$N_{\mathrm{eq}}(\mu) = \arg\min_N \Omega(N, \mu)$$

!!! note "Units"
    With LAMMPS `units real`, energies are in kcal/mol and temperature in K, so
    $k_B = 1.987\times10^{-3}\ \mathrm{kcal\,mol^{-1}\,K^{-1}}$. The analysis
    helpers below default to these units but accept any consistent set.

## The `wang_landau` analysis package

The reusable routines live in `analysis/scripts/wang_landau/` and are used by
both the example plot script and a command-line tool. The public API:

| Function | Description |
|----------|-------------|
| `read_qs_dat(path)` | Load a `qs.dat` file into a `WangLandauResult` (`.N`, `.ln_g`, `.histogram`). |
| `helmholtz_free_energy(ln_g, T)` | `F(N) = -k_B T ln g(N)`. |
| `grand_potential(N, ln_g, mu, T)` | `Omega(N, mu) = F(N) - mu N`. |
| `equilibrium_particle_number(N, ln_g, mu, T)` | `argmin_N Omega(N, mu)`. |
| `plot_grand_potential(result, mus)` | Quick figure of `Omega(N, mu)` for several `mu`. |
| `plot_free_energy(result)` | Quick figure of `F(N)`. |

Example usage:

```python
import sys
sys.path.insert(0, "analysis/scripts")  # or install the package on your path

from wang_landau import read_qs_dat, grand_potential, equilibrium_particle_number

res = read_qs_dat("examples/lj_iterative/iteration_9/qs.dat")

mu = -8.25  # kcal/mol
omega = grand_potential(res.N, res.ln_g, mu, T=300.0)
n_eq = equilibrium_particle_number(res.N, res.ln_g, mu, T=300.0)
print(f"Equilibrium particle number at mu={mu}: N_eq = {n_eq}")
```

## Command-line tool

For a quick look without writing code, use the bundled front-end
`analysis/scripts/plot_dos.py`:

```bash
# Grand potential Omega(N, mu) for several chemical potentials
python analysis/scripts/plot_dos.py path/to/qs.dat \
    --mu -7.75 -8.0 -8.25 -8.5 -8.75

# Helmholtz free energy F(N) instead
python analysis/scripts/plot_dos.py path/to/qs.dat --free-energy

# Save to a file (no display needed)
python analysis/scripts/plot_dos.py path/to/qs.dat -o omega.png
```

The example script `examples/lj_iterative/plot_wang_landau.py` is itself just a
thin wrapper around this package: it picks the final `iteration_*/qs.dat` and
calls `plot_grand_potential`, reproducing the figure shown on the
[theory](theory.md) and [examples](examples.md) pages.
