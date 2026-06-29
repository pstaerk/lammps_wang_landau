"""I/O for Wang-Landau ``qs.dat`` density-of-states files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class WangLandauResult:
    """The columns of a ``qs.dat`` file as equal-length arrays.

    Attributes
    ----------
    N : np.ndarray
        Particle number (int).
    ln_g : np.ndarray
        Estimate of ``ln g(N)`` from the Wang-Landau run.
    histogram : np.ndarray
        Visitation histogram ``h(N)`` of the last iteration.
    """

    N: np.ndarray
    ln_g: np.ndarray
    histogram: np.ndarray

    def __post_init__(self) -> None:
        self.N = np.asarray(self.N, dtype=int)
        self.ln_g = np.asarray(self.ln_g, dtype=float)
        self.histogram = np.asarray(self.histogram, dtype=float)
        if not (self.N.shape == self.ln_g.shape == self.histogram.shape):
            raise ValueError("N, ln_g and histogram must have the same shape")


def read_qs_dat(path: str | Path) -> WangLandauResult:
    """Read a ``qs.dat`` file into a :class:`WangLandauResult`.

    The format is whitespace-separated columns::

        N   ln[g(N)]   h(N)

    with optional ``#`` comments and blank lines. The histogram column is
    optional; if absent it is returned as zeros. Rows are returned sorted by
    ``N``.
    """
    n: list[int] = []
    lng: list[float] = []
    hist: list[float] = []

    for raw in Path(path).read_text().splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        n.append(int(parts[0]))
        lng.append(float(parts[1]))
        hist.append(float(parts[2]) if len(parts) > 2 else 0.0)

    if not n:
        raise ValueError(f"No data parsed from {path!s}")

    order = np.argsort(n)
    return WangLandauResult(
        N=np.asarray(n)[order],
        ln_g=np.asarray(lng, dtype=float)[order],
        histogram=np.asarray(hist, dtype=float)[order],
    )
