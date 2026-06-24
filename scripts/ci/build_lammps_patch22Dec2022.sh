#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WORK_DIR="${ROOT_DIR}/.ci-work"
LAMMPS_DIR="${WORK_DIR}/lammps"
LAMMPS_COMMIT="8b8c0ee72d7460fafdfdb4132e06a533f4f282ce"

rm -rf "${WORK_DIR}"
mkdir -p "${WORK_DIR}"

git init "${LAMMPS_DIR}"
git -C "${LAMMPS_DIR}" remote add origin https://github.com/lammps/lammps.git
git -C "${LAMMPS_DIR}" fetch --depth 1 origin "${LAMMPS_COMMIT}"
git -C "${LAMMPS_DIR}" checkout FETCH_HEAD

cp "${ROOT_DIR}/src/lammps/MC/fix_wang_landau.cpp" "${LAMMPS_DIR}/src/MC/"
cp "${ROOT_DIR}/src/lammps/MC/fix_wang_landau.h" "${LAMMPS_DIR}/src/MC/"

cmake -S "${LAMMPS_DIR}/cmake" -B "${LAMMPS_DIR}/build" \
  -D BUILD_MPI=off \
  -D BUILD_OMP=off \
  -D PKG_MC=on \
  -D CMAKE_BUILD_TYPE=Release

cmake --build "${LAMMPS_DIR}/build" --target lmp -j2
