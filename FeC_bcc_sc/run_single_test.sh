#!/bin/bash
#SBATCH --job-name=Fe16C1_test
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --mem-per-cpu=3800
#SBATCH -C avx512
#SBATCH -A p0020465
#SBATCH -t 02:00:00

ml openmpi/4.1.8-6xzv intel-oneapi-compilers/2025.3.1-pbro intel-oneapi-mkl/2025.3.1-iqtm

ulimit -s unlimited

export OMP_NUM_THREADS=4
export OMP_STACKSIZE=256M

BASE=fe16c1_swsc0.50_2.650000

echo "=== Fe16C1 single-point test: ${BASE} ==="
echo "Start: $(date)"
echo ""

echo "--- KGRN ---"
time kgrn_cpa < "${BASE}.kgrn" > "${BASE}_kgrn.output" 2>&1
KGRN_EXIT=$?
echo "KGRN exit code: ${KGRN_EXIT}"
echo ""

if [ ${KGRN_EXIT} -ne 0 ]; then
    echo "KGRN failed — skipping KFCD"
    exit 1
fi

echo "--- SCF convergence check ---"
grep -i 'EF' "${BASE}_kgrn.output" | tail -5
echo ""

echo "--- KFCD ---"
time kfcd_cpa < "${BASE}.kfcd" > "${BASE}_kfcd.output" 2>&1
KFCD_EXIT=$?
echo "KFCD exit code: ${KFCD_EXIT}"
echo ""

echo "--- Results ---"
echo "KGRN output size: $(wc -c < ${BASE}_kgrn.output) bytes"
echo "KFCD output size: $(wc -c < ${BASE}_kfcd.output) bytes"
echo "kgrn/ contents:"
ls -la kgrn/ 2>/dev/null | tail -5
echo "kfcd/ contents:"
ls -la kfcd/ 2>/dev/null | tail -5
echo ""
echo "End: $(date)"
