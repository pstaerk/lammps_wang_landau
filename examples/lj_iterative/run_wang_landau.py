#!/usr/bin/env python3
"""
Wang-Landau iteration orchestrator for Lennard-Jones fluid.

This script runs sequential Wang-Landau iterations, where each iteration:
1. Uses the current density of states (qs.dat) from the previous run
2. Resets the histogram to zero
3. Uses a refinement factor f_i that decreases as sqrt(f_{i-1})
4. Waits for each LAMMPS run to complete before starting the next

Usage:
    python run_wang_landau.py [--iterations N] [--f0 F0] [--seed SEED] [--seed-increment INC] [--lmp LMP]
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

import numpy as np


def read_template(template_path: str) -> str:
    """Read the LAMMPS input template."""
    with open(template_path, 'r') as f:
        return f.read()


def render_template(template: str, f0: float, seed: int) -> str:
    """Replace placeholders in the template with actual values."""
    return template.replace('${F0}', str(f0)).replace('${SEED}', str(seed))


def get_seeds(base_seed: int, num_iterations: int, increment: int) -> list[int]:
    """Generate seeds: seed_i = base_seed + i * increment"""
    return [base_seed + i * increment for i in range(num_iterations)]


def read_qs_dat(filepath: str) -> np.ndarray:
    """Read the density of states file."""
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split()
                if len(parts) >= 2:
                    data.append((int(parts[0]), float(parts[1]), 0.0))
    return np.array(data, dtype=[('N', int), ('ln_g', float), ('hist', float)])


def write_qs_dat(filepath: str, data: np.ndarray) -> None:
    """Write the density of states file."""
    with open(filepath, 'w') as f:
        for row in data:
            f.write(f"{row['N']}\t{row['ln_g']:.6f}\t{int(row['hist'])}\n")


def reset_histogram(qs_data: np.ndarray) -> np.ndarray:
    """Reset histogram counts to zero while preserving density of states."""
    qs_data['hist'] = 0
    return qs_data


def run_lammps(input_file: str, lammps_cmd: str, work_dir: str) -> tuple[bool, str]:
    """
    Run LAMMPS simulation.
    
    Returns:
        tuple: (success: bool, output: str)
    """
    print(f"  Running LAMMPS in {work_dir}...")
    print(f"  Command: {lammps_cmd} -in {input_file}")
    
    try:
        result = subprocess.run(
            f"{lammps_cmd} -in {input_file}",
            shell=True,
            cwd=work_dir,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout per iteration
        )
        
        if result.returncode == 0:
            print(f"  LAMMPS completed successfully")
            return True, result.stdout + result.stderr
        else:
            print(f"  LAMMPS failed with return code {result.returncode}")
            print(f"  STDERR: {result.stderr[:500]}")
            return False, result.stdout + result.stderr
            
    except subprocess.TimeoutExpired:
        print(f"  LAMMPS timed out after 1 hour")
        return False, "Timeout"
    except Exception as e:
        print(f"  Error running LAMMPS: {e}")
        return False, str(e)


def setup_iteration(iter_dir: Path, template: str, f0: float, seed: int, prev_qs_path: Optional[Path] = None) -> None:
    """Set up files for a single iteration."""
    iter_dir.mkdir(parents=True, exist_ok=True)
    
    # Write the input file
    input_content = render_template(template, f0, seed)
    with open(iter_dir / 'in.lj', 'w') as f:
        f.write(input_content)
    
    print(f"  Using seed: {seed}")
    
    # Copy or create qs.dat
    if prev_qs_path and prev_qs_path.exists():
        shutil.copy(prev_qs_path, iter_dir / 'qs.dat')
        # Reset histogram for new iteration
        qs_data = read_qs_dat(str(iter_dir / 'qs.dat'))
        qs_data = reset_histogram(qs_data)
        write_qs_dat(str(iter_dir / 'qs.dat'), qs_data)
        print(f"  Copied and reset qs.dat from {prev_qs_path}")
    else:
        # Create initial qs.dat with all 1s
        initial_data = np.array([
            (n, 0.0, 0) for n in range(10, 81)
        ], dtype=[('N', int), ('ln_g', float), ('hist', float)])
        write_qs_dat(str(iter_dir / 'qs.dat'), initial_data)
        print(f"  Created initial qs.dat")


def run_wang_landau_iterations(
    base_dir: str,
    num_iterations: int,
    f0: float,
    seed: int,
    seed_increment: int = 1,
    lammps_cmd: str = 'lmp'
) -> None:
    """
    Run Wang-Landau iterations sequentially.
    
    Args:
        base_dir: Base directory containing the template
        num_iterations: Number of iterations to run
        f0: Initial modification factor
        seed: Base seed (seed_i = base_seed + i * increment)
        seed_increment: Increment seeds by this amount each iteration
        lammps_cmd: LAMMPS executable command
    """
    seeds = get_seeds(seed, num_iterations, seed_increment)
    base_path = Path(base_dir)
    template_path = base_path / 'in.lj_template'
    
    if not template_path.exists():
        print(f"Error: Template not found at {template_path}")
        sys.exit(1)
    
    template = read_template(str(template_path))
    
    current_f = f0
    prev_qs_path = None
    
    print("=" * 60)
    print("Wang-Landau Iteration Orchestrator")
    print("=" * 60)
    print(f"  Base directory: {base_dir}")
    print(f"  Number of iterations: {num_iterations}")
    print(f"  Initial f_0: {f0}")
    print(f"  Base seed: {seed}")
    print(f"  Seed increment: {seed_increment}")
    print(f"  LAMMPS command: {lammps_cmd}")
    print("=" * 60)
    
    for i in range(num_iterations):
        iter_name = f"iteration_{i}"
        iter_dir = base_path / iter_name
        
        print(f"\n{'='*60}")
        print(f"Starting {iter_name}")
        print(f"  f_{i} = {current_f}")
        print(f"  Seed: {seeds[i]}")
        print(f"  Next f_{i+1} = sqrt({current_f}) = {np.sqrt(current_f)}")
        print("=" * 60)
        
        # Set up iteration files
        setup_iteration(iter_dir, template, current_f, seeds[i], prev_qs_path)
        
        # Run LAMMPS
        success, output = run_lammps('in.lj', lammps_cmd, str(iter_dir))
        
        if not success:
            print(f"\nIteration {i} failed! Stopping.")
            print("Last output:")
            print(output[-1000:])
            sys.exit(1)
        
        # Prepare for next iteration
        prev_qs_path = iter_dir / 'qs.dat'
        current_f = np.sqrt(current_f)
        
        print(f"\n{iter_name} complete!")
        print(f"  Final seed used: {seeds[i]}")
        print(f"  Next modification factor: {current_f}")
    
    print("\n" + "=" * 60)
    print("All iterations complete!")
    print("=" * 60)
    print(f"\nResults in: {base_path}")
    print(f"Final density of states: {prev_qs_path.parent}/qs.dat")


def main():
    parser = argparse.ArgumentParser(
        description='Run sequential Wang-Landau iterations for LAMMPS'
    )
    parser.add_argument(
        '--dir', '-d',
        default='.',
        help='Base directory containing in.lj_template (default: .)'
    )
    parser.add_argument(
        '--iterations', '-n',
        type=int,
        default=10,
        help='Number of iterations to run (default: 10)'
    )
    parser.add_argument(
        '--f0',
        type=float,
        default=np.exp(4.0),  # exp(4) ≈ 54.6
        help='Initial modification factor f_0 (default: exp(4) ≈ 54.6)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=12345,
        help='Base random seed (default: 12345)'
    )
    parser.add_argument(
        '--seed-increment',
        type=int,
        default=1,
        help='Increment seeds by this amount each iteration: seed_i = seed + i*increment (default: 1)'
    )
    parser.add_argument(
        '--lmp',
        default='lmp',
        help='LAMMPS executable command (default: lmp)'
    )
    
    args = parser.parse_args()
    
    run_wang_landau_iterations(
        base_dir=args.dir,
        num_iterations=args.iterations,
        f0=args.f0,
        seed=args.seed,
        seed_increment=args.seed_increment,
        lammps_cmd=args.lmp
    )


if __name__ == '__main__':
    main()
