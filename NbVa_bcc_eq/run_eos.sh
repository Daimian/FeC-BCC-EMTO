#!/bin/bash
#SBATCH --job-name=NbVa_eq
#SBATCH -N 1
#SBATCH -n 7
#SBATCH -c 1
#SBATCH --mem-per-cpu=3800
#SBATCH -C avx512
#SBATCH -A p0020465
#SBATCH -t 00:30:00

ml openmpi/4.1.8-6xzv intel-oneapi-compilers/2025.3.1-pbro intel-oneapi-mkl/2025.3.1-iqtm

export OMP_NUM_THREADS=1
export OMP_STACKSIZE=256M
ulimit -s unlimited

for kgrn_in in *.kgrn; do
    base=${kgrn_in%.kgrn}
    (
        kgrn_cpa < "${base}.kgrn" > "${base}_kgrn.output" 2>&1
        kfcd_cpa < "${base}.kfcd" > "${base}_kfcd.output" 2>&1
    ) &
done

wait
echo "All SWS points finished."
