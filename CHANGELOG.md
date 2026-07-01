# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- **Graceful termination** - Histogram convergence now triggers `timer->force_timeout()` instead of hard `MPI_Finalize()/exit(0)`
- **Nonneutral flag support** - Added `nonneutral` option for systems with net charge using electrostatic interactions (kspace styles)
- **Enhanced histogram output** - Improved error handling and scientific notation in `write_histogram()`
- **Analysis test suite** - Added minimal test suite for Wang-Landau analysis tools (pytest-based)

### Changed
- **Sign bug fix** - Corrected Wang-Landau acceptance probability: `exp(-wl_factor+beta*)` (was `exp(+wl_factor-beta*)`)
- **Documentation** - Added comprehensive documentation for `nonneutral` option and graceful termination behavior

### Contributors
- Russell Kajouri (@russellkajouri) - Graceful termination implementation
- Philipp Stärk (@pstaerk) - Nonneutral flag support and documentation

## [0.1.0] - 2026-06-24

### Added
- Initial repository scaffold.
- Added a custom Wang-Landau `fix` to the LAMMPS `MC` package.
- Added examples, analysis skeleton, and documentation pages.
- Basic build CI workflow against LAMMPS patch_22Dec2022.
