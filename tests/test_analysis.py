"""Minimal test suite for Wang-Landau analysis tools.

Run with: pytest tests/test_analysis.py -v
"""

import sys
import os
from pathlib import Path
import tempfile

import numpy as np
import pytest

# Add analysis/scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'analysis', 'scripts'))

from wang_landau import io, thermo, plotting


class TestIO:
    """Test input/output functions."""

    def test_read_qs_dat_basic(self):
        """Test basic reading of a qs.dat file."""
        # Create a temporary qs.dat file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write("# Test comment\n")
            f.write("# Another comment\n\n")
            f.write("0\t0.0\t100\n")
            f.write("1\t1.5\t200\n")
            f.write("2\t3.0\t300\n")
            f.write("3\t4.5\t400\n")
            temp_path = f.name

        try:
            result = io.read_qs_dat(temp_path)

            assert len(result.N) == 4
            assert np.array_equal(result.N, [0, 1, 2, 3])
            assert np.allclose(result.ln_g, [0.0, 1.5, 3.0, 4.5])
            assert np.allclose(result.histogram, [100, 200, 300, 400])
        finally:
            Path(temp_path).unlink()

    def test_read_qs_dat_no_histogram(self):
        """Test reading qs.dat without histogram column."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write("0\t0.0\n")
            f.write("1\t1.5\n")
            f.write("2\t3.0\n")
            temp_path = f.name

        try:
            result = io.read_qs_dat(temp_path)

            assert len(result.N) == 3
            assert np.array_equal(result.N, [0, 1, 2])
            assert np.allclose(result.ln_g, [0.0, 1.5, 3.0])
            assert np.all(result.histogram == 0.0)
        finally:
            Path(temp_path).unlink()

    def test_read_qs_dat_unordered(self):
        """Test that rows are sorted by N."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write("2\t3.0\t300\n")
            f.write("0\t0.0\t100\n")
            f.write("1\t1.5\t200\n")
            temp_path = f.name

        try:
            result = io.read_qs_dat(temp_path)

            assert np.array_equal(result.N, [0, 1, 2])
        finally:
            Path(temp_path).unlink()

    def test_wang_landau_result_validation(self):
        """Test that WangLandauResult validates array shapes."""
        with pytest.raises(ValueError, match="same shape"):
            io.WangLandauResult(
                N=[0, 1],
                ln_g=[0.0],
                histogram=[100, 200]
            )

    def test_read_empty_file(self):
        """Test reading an empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="No data parsed"):
                io.read_qs_dat(temp_path)
        finally:
            Path(temp_path).unlink()


class TestThermo:
    """Test thermodynamic functions."""

    def test_helmholtz_free_energy(self):
        """Test Helmholtz free energy calculation."""
        N = np.array([0, 1, 2, 3])
        ln_g = np.array([0.0, 1.5, 3.0, 4.5])
        T = 1.0

        F = thermo.helmholtz_free_energy(ln_g, T=T)

        # F(N) = -k_B * T * ln_g(N)
        expected = -thermo.kB_KCAL * T * ln_g
        assert np.allclose(F, expected)

    def test_grand_potential(self):
        """Test grand potential calculation."""
        N = np.array([0, 1, 2, 3])
        ln_g = np.array([0.0, 1.5, 3.0, 4.5])
        T = 1.0
        mu = -1.0

        Omega = thermo.grand_potential(N, ln_g, mu, T=T)

        # Omega(N, mu) = F(N) - mu * N = -k_B * T * ln_g(N) - mu * N
        F = -thermo.kB_KCAL * T * ln_g
        expected = F - mu * N
        assert np.allclose(Omega, expected)

    def test_equilibrium_particle_number(self):
        """Test equilibrium particle number from grand potential."""
        # Just test that the function runs and returns a float
        N = np.array([0, 1, 2, 3, 4])
        ln_g = np.array([0.0, 2.0, 8.0, 10.0, 8.0])
        T = 1.0
        mu = 0.0

        N_eq = thermo.equilibrium_particle_number(N, ln_g, T, mu, degree=5)

        # Should return a float
        assert isinstance(N_eq, (int, float))
        assert 0.0 <= N_eq <= 4.0


class TestConstants:
    """Test physical constants."""

    def test_kb_constant(self):
        """Test that Boltzmann constant is reasonable."""
        # kB in kcal/(mol·K) should be approximately 0.001987
        assert 0.001 < thermo.kB_KCAL < 0.003


if __name__ == "__main__":
    pytest.main([__file__, "-v"])