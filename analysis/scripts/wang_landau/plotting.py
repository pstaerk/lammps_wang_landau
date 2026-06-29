"""Plotting helpers for Wang-Landau results.

These import matplotlib lazily so that the rest of the package can be used
without a matplotlib installation (e.g. for scripted post-processing).
"""

from __future__ import annotations

import numpy as np

from .io import WangLandauResult
from .thermo import grand_potential, helmholtz_free_energy, kB_KCAL


def plot_grand_potential(
    result: WangLandauResult,
    mus,
    T: float = 300.0,
    kB: float = kB_KCAL,
    ax=None,
    energy_unit: str = "kcal/mol",
):
    r"""Plot ``Omega(N, mu)`` for one chemical potential per curve.

    Parameters
    ----------
    result : WangLandauResult
        Output of :func:`~wang_landau.io.read_qs_dat`.
    mus : iterable of float
        Chemical potentials to plot, in the same energy units as ``kB * T``.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots()

    for mu in mus:
        omega = grand_potential(result.N, result.ln_g, mu, T=T, kB=kB)
        ax.plot(result.N, omega, "o-", label=f"μ = {mu:g}", markersize=3)

    ax.set_xlabel("particle number $N$")
    ax.set_ylabel(rf"$\Omega(N,\mu)$ / {energy_unit}")
    ax.set_title(f"Grand potential at $T$ = {T} K")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return ax


def plot_free_energy(
    result: WangLandauResult,
    T: float = 300.0,
    kB: float = kB_KCAL,
    ax=None,
    energy_unit: str = "kcal/mol",
):
    r"""Plot the Helmholtz free energy ``F(N) = -k_B T ln g(N)``."""
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots()

    f = helmholtz_free_energy(result.ln_g, T=T, kB=kB)
    ax.plot(result.N, f, "o-", markersize=3)
    ax.set_xlabel("particle number $N$")
    ax.set_ylabel(rf"$F(N)$ / {energy_unit}")
    ax.set_title(f"Helmholtz free energy at $T$ = {T} K")
    ax.grid(True, alpha=0.3)
    return ax
