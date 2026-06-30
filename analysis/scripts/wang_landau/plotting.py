"""Plotting helpers for Wang-Landau results.

These import matplotlib lazily so that the rest of the package can be used
without a matplotlib installation (e.g. for scripted post-processing).
"""

from __future__ import annotations

import numpy as np

from .io import WangLandauResult
from .thermo import (
    _fitted_grand_potential,
    grand_potential,
    helmholtz_free_energy,
    kB_KCAL,
)


def plot_grand_potential(
    result: WangLandauResult,
    mus,
    T: float = 300.0,
    kB: float = kB_KCAL,
    degree: int = 4,
    show_fit: bool = True,
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
    degree : int, optional
        Degree of the polynomial fit used to locate and display the minimum
        of each curve (see :func:`~wang_landau.thermo.equilibrium_particle_number`).
    show_fit : bool, optional
        When true, overlay the polynomial fit and mark the fitted minimum
        ``N_eq`` of each curve with a vertical line and marker.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots()

    for mu in mus:
        omega = grand_potential(result.N, result.ln_g, mu, T=T, kB=kB)
        ax.plot(result.N, omega, "o", markersize=4, alpha=0.5)

        if show_fit:
            poly, n_eq = _fitted_grand_potential(result.N, omega, degree)
            label = f"μ = {mu:g}  ($N_{{eq}}$ = {n_eq:.2f})"
            if poly is not None:
                n_fine = np.linspace(result.N.min(), result.N.max(), 300)
                ax.plot(n_fine, poly(n_fine), "-", lw=1.5, label=label)
                ax.axvline(n_eq, ls=":", alpha=0.5)
                ax.plot(n_eq, poly(n_eq), "*", markersize=12)
            else:
                ax.plot([], "-", label=label)
        else:
            n_eq = result.N[int(np.argmin(omega))]
            ax.plot(result.N, omega, "-", lw=1.5,
                    label=f"μ = {mu:g}  ($N_{{eq}}$ = {n_eq:g})")

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
