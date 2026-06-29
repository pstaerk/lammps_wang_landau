#!/usr/bin/env python3
"""Plot the grand potential or Helmholtz free energy from a ``qs.dat`` file.

Thin command-line front-end over the reusable ``wang_landau`` analysis package
(see ``analysis/scripts/wang_landau`` and ``docs/analysis.md``).

Examples
--------
    # Grand potential for a few chemical potentials:
    python plot_dos.py path/to/qs.dat --mu -7.75 -8.0 -8.25 -8.5 -8.75

    # Helmholtz free energy instead:
    python plot_dos.py path/to/qs.dat --free-energy

    # Save to a file instead of showing a window:
    python plot_dos.py path/to/qs.dat -o omega.png
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Make the sibling `wang_landau` package importable when run from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib

from wang_landau import plot_free_energy, plot_grand_potential, read_qs_dat


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("qs_dat", help="path to a Wang-Landau qs.dat file")
    parser.add_argument(
        "--mu",
        nargs="+",
        type=float,
        default=[-7.75, -8.0, -8.25, -8.5, -8.75],
        help="chemical potentials (kcal/mol) for the grand-potential curves",
    )
    parser.add_argument(
        "-T", "--temperature", type=float, default=300.0, help="temperature (K)"
    )
    parser.add_argument(
        "--free-energy",
        action="store_true",
        help="plot the Helmholtz free energy F(N) instead of Omega(N, mu)",
    )
    parser.add_argument(
        "-o", "--output", help="save the figure to this path instead of showing it"
    )
    args = parser.parse_args(argv)

    if args.output:
        matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    result = read_qs_dat(args.qs_dat)
    if args.free_energy:
        plot_free_energy(result, T=args.temperature)
    else:
        plot_grand_potential(result, args.mu, T=args.temperature)

    if args.output:
        plt.savefig(args.output, dpi=150, bbox_inches="tight")
        print(f"Saved figure to {args.output}")
    else:
        plt.show()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
