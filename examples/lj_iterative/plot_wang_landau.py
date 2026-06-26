#!/usr/bin/env python3
"""Plot grand potential Omega = kBT ln Q - mu N from Wang-Landau DOS."""

import glob
import sys
import pint
import numpy as np
import matplotlib.pyplot as plt

ureg = pint.UnitRegistry()
ureg.enable_contexts('chemistry')

# Physical constants
kB = 1.987e-3 * ureg.kcal / ureg.mole / ureg.kelvin  # R in kcal
T = 300 * ureg.kelvin
mu_vals = [-7.75, -8.0, -8.25, -8.5, -8.75] * ureg.kcal / ureg.mole

def read_qs_dat(path):
    n, lng = [], []
    for line in open(path):
        p = line.split()
        if len(p) >= 2:
            n.append(int(p[0]))
            lng.append(float(p[1]))
    return np.array(n), np.array(lng)

# Read final iteration
base = sys.argv[1] if len(sys.argv) > 1 else '.'
iters = sorted(glob.glob(f'{base}/iteration_*'))
final = iters[-1].split('_')[-1]
n, lng = read_qs_dat(f'{base}/iteration_{final}/qs.dat')

# Plot Omega for each mu
for mu in mu_vals:
    omega = -kB * T * lng - mu * n
    plt.plot(n, omega.magnitude, 'o-', label=f'mu={mu.magnitude}', markersize=3)

plt.xlabel('N')
plt.ylabel('Omega (kcal/mol)')
plt.title(f'Grand Potential at T={T.magnitude}K')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
