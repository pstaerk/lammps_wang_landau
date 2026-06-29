"""Thermodynamic quantities derived from a Wang-Landau density of states.

The functions here are unit-agnostic: pass a temperature ``T`` and chemical
potential ``mu`` in whatever energy units you want the result in, together
with a matching Boltzmann constant ``kB``. The default :data:`kB_KCAL`
corresponds to LAMMPS ``units real`` (kcal mol^-1 K^-1), so energies come out
in kcal/mol. See ``docs/theory.md`` for the derivation.
"""

from __future__ import annotations

import numpy as np

#: Boltzmann constant in kcal mol^-1 K^-1 (LAMMPS ``units real``).
kB_KCAL: float = 1.9872041e-3


def helmholtz_free_energy(
    ln_g: np.ndarray, T: float = 300.0, kB: float = kB_KCAL
) -> np.ndarray:
    r"""Helmholtz free energy ``F(N) = -k_B T ln g(N)``.

    Only defined up to an additive constant (the arbitrary zero of the DOS),
    which is irrelevant for locating minima.
    """
    return -kB * T * np.asarray(ln_g, dtype=float)


def grand_potential(
    N: np.ndarray,
    ln_g: np.ndarray,
    mu: float,
    T: float = 300.0,
    kB: float = kB_KCAL,
) -> np.ndarray:
    r"""Grand (Landau) free energy ``Omega(N, mu) = F(N) - mu N``."""
    N = np.asarray(N, dtype=float)
    return helmholtz_free_energy(ln_g, T=T, kB=kB) - mu * N


def equilibrium_particle_number(
    N: np.ndarray,
    ln_g: np.ndarray,
    mu: float,
    T: float = 300.0,
    kB: float = kB_KCAL,
) -> int:
    r"""Equilibrium particle number ``N_eq(mu) = argmin_N Omega(N, mu)``."""
    N = np.asarray(N, dtype=float)
    omega = grand_potential(N, ln_g, mu, T=T, kB=kB)
    return int(N[int(np.argmin(omega))])
