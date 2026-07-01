---
title: Using the Method in LAMMPS
---

# Usage within LAMMPS

This project contains one Wang-Landau `fix` style implementation in:

- `src/lammps/MC/fix_wang_landau.h`
- `src/lammps/MC/fix_wang_landau.cpp`

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

An example for a more complex system to sample is given by the following:

```
fix mywl <group> wang_landau <nevery> <ninsert> <ndisplace> 0 <seed> \
    <temperature> <displace> <f_fac> \
    min <nmin> max <nmax> region <region_name> \
    shake <shake_name> mol <molecule_name> tfac_insert <tfac_insert> \
    accuracy <accuracy> full_energy
```

Where we refer to the section above for an explanation of the basic structure.
Here, we show how to use rigid molecules via
[shake](https://docs.lammps.org/fix_shake.html) `shake`, using molecules via
[molecule](https://docs.lammps.org/molecule.html) `mol` and setting a 
temperature correction factor for the molecules degrees of freedom (see
[LAMMPS docs](https://docs.lammps.org/fix_gcmc.html#description)).
A insertion region can be set via
[LAMMPS regions](https://docs.lammps.org/region.html) and incorporated during
sampling via `region`.

It is also important to note that for extended molecules the acceptance
probability usually decreases drastically and thus requires a larger number of
visits per iteration, as controlled via the `accuracy` convergence criterion.
A good default value for a classical water model, for example, is
`accuracy 1000`.

## Special Options

### full_energy

When calculating the acceptance probability for insertion/deletion moves,
the fix can either use pairwise energies only or compute the full system energy.
The `full_energy` option enables full system energy calculation, which is
necessary when:

- Using long-range electrostatic interactions (kspace styles like PPPM, Ewald)
- Needing more accurate energy differences
- Working with systems where many-body effects are important

Note: `full_energy` is required when using the `nonneutral` option (see below).

### nonneutral (for non-neutral systems)

**This option is crucial for systems with net charge when using electrostatic
interactions.** When simulating non-neutral systems with kspace styles
(e.g., PPPM, Ewald), LAMMPS applies a neutralizing background charge to satisfy
periodic boundary conditions. This background interaction affects the energy
and should be properly accounted for.

To use this option:

```lammps
fix mywl <group> wang_landau <nevery> <ninsert> <ndisplace> <type> <seed> \
    <temperature> <displace> <f_fac> \
    min <nmin> max <nmax> \
    accuracy <accuracy> full_energy nonneutral
```

**Requirements:**
- A kspace style must be defined in your LAMMPS input (e.g., `kspace_style pppm 1.0e-4`)
- The `full_energy` option must be enabled
- The system must have charged particles

**What it does:**
The `nonneutral` option removes the interaction with the neutralizing background
charge from the energy calculations during Wang-Landau moves. This ensures
correct thermodynamics when the net charge of the system changes during
insertion/deletion events (e.g., inserting charged molecules).

**Physical intuition:**
When you insert a charged ion into a periodic system with Ewald/PPPM,
LAMMPS adds a compensating background charge to maintain overall neutrality.
This background interaction is an artifact of the periodic boundary conditions
and should not contribute to the free energy difference you're trying to
sample. The `nonneutral` option corrects for this.

**Example use case:**
Simulating electrolyte solutions where you're inserting/deleting ions and
want to correctly sample the ion density of states without artifacts from the
neutralizing background.

### Graceful Termination

When the Wang-Landau histogram converges (all bins meet the accuracy criterion),
the fix will trigger graceful termination:

- The histogram and density of states are written to `qs.dat`
- LAMMPS is notified to stop cleanly via `timer->force_timeout()`
- No hard exit is performed, allowing proper cleanup

This ensures that:
- Output files are properly flushed and closed
- Any LAMMPS post-processing runs correctly
- The simulation can be resumed or analyzed without corruption

The convergence criterion is controlled by the `accuracy` parameter:
higher values require more samples but give more accurate results.

[^1]: Wang, F. G. & Landau, D. P. [Efficient, Multiple-Range Random Walk Algorithm to Calculate the Density of States](https://doi.org/10.1103/PhysRevLett.86.2050). *Phys. Rev. Lett.* **86**, 2050–2053 (2001).