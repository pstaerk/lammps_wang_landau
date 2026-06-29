---
title: LAMMPS Fixes
---

# LAMMPS Fix Overview

This project contains one Wang-Landau `fix` style implementation in:

- `src/lammps/MC/fix_wl.h`
- `src/lammps/MC/fix_wl.cpp`

## Basic Syntax

As described in the [theory section](theory.md), there are a few
"hyper-parameters" associated with the Wang-Landau method and the method is
an iterative procedure. The Wang-Landau extension to LAMMPS is implemented as
a single iteration of the method. This allows for detailed procedural control,
but requires external orchestration.
Here, we thus describe the syntax and the parameters for a single iteration and
refer to [the examples page](examples.md) for a description of the orchestration
needed to perform multiple iterations.

The fix scheme largely follows the
[standard LAMMPS GCMC fix scheme](https://docs.lammps.org/fix_gcmc.html).
For single particles, you can use the following template:
```lammps
fix <name> <group> wang_landau <nevery> <ninsert> <ndisplace> <type> <seed> \
    <temperature> <displace> <f_fac> min <nmin> max <nmax> accuracy <acc_fac>
```

Here, the parameters are:

 - `<name>` Internal name of the fix
 - `<group>` Particle group that the fix is acting on
 - `<nevery>` Number of integration loop steps until the fix is executed again
 - `<ninsert>` Number of insertion/deletion moves (every move is tracked by the
   method)
 - `<ndisplace>` Number of displacement moves to be made (this should be enough
   to get roughly decorrelated configurations between insertion/deletion moves,
   see [^1])
 - `<type>` Type of the particle that the method inserts
 - `<seed>` Seed for the random number generator
 - `<temperature>` Temperature of the particles
 - `<displace>` Displacement distance that particles are moved by
 - `<f_fac>` Modification factor $f_i$, see [theory](theory.md)
 - `<nmin>` Lower limit of the sampling "window" for the Wang-Landau run. The
   method will not go to particle numbers $N < n_{\mathrm{min}}$
 - `<nmax>` Upper limit of the sampling "window" for the Wang-Landau run. The
   method will not go to particle numbers $N > n_{\mathrm{max}}$
 - `<acc_fac>` Convergence criterion: the method will continue sampling until
   each particle number $N$ has been visited $h(N) > A / \sqrt{\ln{f}}$, with
   $A$ the accuracy factor `acc_fac`. Setting this parameter higher thus results
   in higher statistical accuracy within one iteration, trading longer
   simulation times for higher accuracy.

To give a good starting point for setting up simulations, we propose you use
```lammps
fix mywl <group> wang_landau 1 10 50 <type> <seed> \
    <temperature> 1.0 <f_fac> min <nmin> max <nmax> accuracy 500
```
which are good default values for using the method for a relatively dilute gas/
fluid.

## Advanced Syntax

To come soon.

[^1]: Wang, F. G. & Landau, D. P. [Efficient, Multiple-Range Random Walk Algorithm to Calculate the Density of States](https://doi.org/10.1103/PhysRevLett.86.2050). *Phys. Rev. Lett.* **86**, 2050–2053 (2001).