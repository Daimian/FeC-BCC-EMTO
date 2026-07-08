#!/bin/bash
#SBATCH --job-name=Fe16C1_eta
#SBATCH -N 1
#SBATCH -n 5
#SBATCH -c 4
#SBATCH --mem-per-cpu=3800
#SBATCH -A p0020465
#SBATCH -t 02:00:00

ml openmpi/4.1.8-6xzv intel-oneapi-compilers/2025.3.1-pbro intel-oneapi-mkl/2025.3.1-iqtm

export OMP_NUM_THREADS=1
export OMP_STACKSIZE=256M

for kgrn_in in fe16c1_swsc*.kgrn; do
    base=${kgrn_in%.kgrn}
    (
        kgrn_cpa < "${base}.kgrn" > "${base}_kgrn.output" 2>&1
        kfcd_cpa < "${base}.kfcd" > "${base}_kfcd.output" 2>&1
    ) &
done

wait
echo "All S(ws)_C scan points finished."
