"""Reusable analysis routines for Wang-Landau density-of-states output.

The LAMMPS ``fix wang_landau`` writes a ``qs.dat`` file with the estimated
density of states ``ln g(N)`` as a function of particle number ``N``. This
package provides the small set of routines needed to turn that raw output into
thermodynamic quantities and plots:

* :func:`read_qs_dat`        - load a ``qs.dat`` file
* :func:`helmholtz_free_energy` - F(N) = -k_B T ln g(N)
* :func:`grand_potential`    - Omega(N, mu) = F(N) - mu N
* :func:`equilibrium_particle_number` - polynomial-fit minimum of Omega(N, mu)
* :func:`plot_grand_potential`, :func:`plot_free_energy` - quick figures

See ``docs/analysis.md`` for a walk-through.
"""

from .io import WangLandauResult, read_qs_dat
from .thermo import (
    kB_KCAL,
    equilibrium_particle_number,
    grand_potential,
    helmholtz_free_energy,
)
from .plotting import plot_free_energy, plot_grand_potential

__all__ = [
    "WangLandauResult",
    "read_qs_dat",
    "kB_KCAL",
    "helmholtz_free_energy",
    "grand_potential",
    "equilibrium_particle_number",
    "plot_grand_potential",
    "plot_free_energy",
]
