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


def _fitted_grand_potential(N, omega, degree):
    r"""Fit ``omega(N)`` with a polynomial and locate its minimum.

    Returns ``(poly, n_min)`` where ``poly`` is the fitted
    :class:`numpy.poly1d` (or ``None`` when there are too few samples to fit)
    and ``n_min`` is the minimizing ``N``. When the fit is unavailable or its
    minimum lies outside the sampled range, ``n_min`` falls back to the
    discrete :func:`numpy.argmin` of ``omega``.
    """
    n_min = float(N[int(np.argmin(omega))])

    # Not enough points to fit the requested polynomial -> discrete argmin.
    if N.size <= degree:
        return None, n_min

    coeffs = np.polyfit(N, omega, degree)  # highest power first
    poly = np.poly1d(coeffs)

    # Stationary points = real roots of the derivative inside [N.min, N.max].
    n_lo, n_hi = float(N.min()), float(N.max())
    roots = np.roots(np.polyder(coeffs))
    real_roots = roots[np.isreal(roots)].real
    inside = real_roots[(real_roots >= n_lo) & (real_roots <= n_hi)]
    if inside.size == 0:
        return poly, n_min

    # Among the interior stationary points and the boundaries, pick the one
    # with the lowest grand potential according to the fit.
    candidates = np.concatenate(([n_lo, n_hi], inside))
    n_min = float(candidates[int(np.argmin(poly(candidates)))])
    return poly, n_min


def equilibrium_particle_number(
    N: np.ndarray,
    ln_g: np.ndarray,
    mu: float,
    T: float = 300.0,
    kB: float = kB_KCAL,
    degree: int = 4,
) -> float:
    r"""Equilibrium particle number ``N_eq(mu) = argmin_N Omega(N, mu)``.

    Rather than returning the discrete sample with the smallest grand
    potential, the grand potential ``Omega(N, mu)`` is fitted by a polynomial
    of the given ``degree`` in ``N`` and the minimum of that fit is returned.
    This yields a sub-integer estimate of the equilibrium particle number and
    smooths over statistical noise in the Wang-Landau density of states.

    Falls back to the discrete :func:`numpy.argmin` result when fewer than
    ``degree + 1`` samples are available or when the fitted minimum lies
    outside the sampled range of ``N``.
    """
    N = np.asarray(N, dtype=float)
    omega = grand_potential(N, ln_g, mu, T=T, kB=kB)
    _, n_min = _fitted_grand_potential(N, omega, degree)
    return n_min
