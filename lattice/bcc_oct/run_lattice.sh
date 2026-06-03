#!/bin/bash
#SBATCH --job-name=lat_bcc_oct
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH --mem-per-cpu=3800
#SBATCH -C avx512
#SBATCH -A p0020465
#SBATCH -t 00:10:00

ml openmpi/4.1.8-6xzv intel-oneapi-compilers/2025.3.1-pbro intel-oneapi-mkl/2025.3.1-iqtm

bmdl < bcc_oct.bmdl > bmdl_bcc_oct.output 2>&1
kstr < bcc_oct.kstr > kstr_bcc_oct.output 2>&1
shape < bcc_oct.shape > shape_bcc_oct.output 2>&1

echo "BCC+oct lattice files done."
