#!/usr/bin/env python3
"""Plot the grand potential Omega(N, mu) from the final Wang-Landau iteration.

This is a thin wrapper around the reusable analysis package in
``analysis/scripts/wang_landau`` (see ``docs/analysis.md``). The package is
located relative to this file, so the script can be run from anywhere.

Usage
-----
    python plot_wang_landau.py [base_dir]

``base_dir`` defaults to the directory containing this script and should hold
``iteration_*/qs.dat`` folders produced by ``run_wang_landau.py``.
"""

from __future__ import annotations

import glob
import sys
from pathlib import Path

# Locate the reusable analysis package relative to the repo root.
_here = Path(__file__).resolve()
for _parent in _here.parents:
    _candidate = _parent / "analysis" / "scripts"
    if _candidate.is_dir():
        sys.path.insert(0, str(_candidate))
        break
else:
    raise FileNotFoundError("Could not locate 'analysis/scripts/' in the repo")

from wang_landau import plot_grand_potential, read_qs_dat


def _iteration_index(path: str) -> int:
    return int(Path(path).name.split("_")[-1])


def main() -> None:
    base = sys.argv[1] if len(sys.argv) > 1 else str(_here.parent)
    iters = sorted(glob.glob(f"{base}/iteration_*"), key=_iteration_index)
    if not iters:
        raise SystemExit(f"No iteration_*/ directories found under {base!r}")

    final = iters[-1]
    print(f"Using final Wang-Landau iteration: {final}")

    result = read_qs_dat(Path(final) / "qs.dat")

    import matplotlib.pyplot as plt

    mus = [-7.75, -8.0, -8.25, -8.5, -8.75]
    plot_grand_potential(result, mus)
    plt.show()


if __name__ == "__main__":
    main()
