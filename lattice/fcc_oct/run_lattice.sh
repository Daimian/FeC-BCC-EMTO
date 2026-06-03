#!/bin/bash
#SBATCH --job-name=lat_fcc_oct
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH --mem-per-cpu=3800
#SBATCH -C avx512
#SBATCH -A p0020465
#SBATCH -t 00:10:00

ml openmpi/4.1.8-6xzv intel-oneapi-compilers/2025.3.1-pbro intel-oneapi-mkl/2025.3.1-iqtm

bmdl < fcc_oct.bmdl > bmdl_fcc_oct.output 2>&1
kstr < fcc_oct.kstr > kstr_fcc_oct.output 2>&1
kstr < fcc_octM.kstr > kstr_fcc_octM.output 2>&1
shape < fcc_oct.shape > shape_fcc_oct.output 2>&1

echo "FCC+oct lattice files done."
