# Lennard-Jones Wang-Landau Iterative Example

This directory contains an automated workflow for running sequential Wang-Landau iterations on a Lennard-Jones fluid.

## Files

- `in.lj_template` - LAMMPS input template with placeholders for `f_0` and `seed`
- `run_wang_landau.py` - Python orchestration script
- `qs.dat` - Initial density of states file (template)

## How It Works

Each iteration:
1. Copies the density of states from the previous iteration
2. Resets the histogram to zero
3. Uses a modification factor `f_i = sqrt(f_{i-1})`
4. Uses seed `seed_i = seed_base + i * increment`
5. Runs LAMMPS until the flatness criterion is met
6. Proceeds to the next iteration

The modification factor sequence (starting with `f_0 = exp(4)`):
- f_0 = 54.6
- f_1 = 7.39
- f_2 = 2.72
- f_3 = 1.65
- f_4 = 1.28
- f_5 = 1.13
- ... and so on

## Usage

```bash
# Run with defaults (10 iterations, f_0=exp(4), seed=12345, increment=1)
python run_wang_landau.py

# Run with custom parameters
python run_wang_landau.py --iterations 15 --f0 100.0 --seed 42 --seed-increment 10

# Different LAMMPS executable
python run_wang_landau.py --lmp /path/to/lmp_serial
```

## Output Structure

```
lj_iterative/
├── in.lj_template      # Input template
├── run_wang_landau.py  # Orchestration script
├── qs.dat             # Initial density of states
├── iteration_0/       # First iteration
│   ├── in.lj          # Generated input file (seed = 12345)
│   ├── qs.dat         # Results
│   └── ...
├── iteration_1/       # Second iteration
│   ├── in.lj          # Generated input file (seed = 12346)
│   ├── qs.dat
│   └── ...
└── ...
```

## Command-Line Arguments

| Argument          | Short | Description                                           | Default          |
|-------------------|-------|-------------------------------------------------------|------------------|
| `--dir`           | `-d`  | Directory with template                               | `.`              |
| `--iterations`    | `-n`  | Number of WL iterations                               | `10`             |
| `--f0`            |       | Initial modification factor                           | `exp(4) ≈ 54.6`  |
| `--seed`          |       | Base random seed                                      | `12345`          |
| `--seed-increment`|       | Increment seeds by this amount each iteration         | `1`              |
| `--lmp`           |       | LAMMPS executable command                             | `lmp`            |

## Seed Strategy

The seed for each iteration is calculated as:
```
seed_i = seed_base + i * seed_increment
```

Example with `--seed 12345 --seed-increment 10`:
- iteration_0: seed = 12345
- iteration_1: seed = 12355
- iteration_2: seed = 12365
- ...

## Citation

If you use this example in academic work, please cite the [Wang-Landau extension paper](../README.md#citation).
