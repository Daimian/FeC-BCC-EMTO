#!/bin/bash
#SBATCH --job-name=FeC_EOS
#SBATCH --partition=accel
#SBATCH --gres=gpu:1
#SBATCH -N 1
#SBATCH -n 7
#SBATCH -c 1
#SBATCH --mem-per-cpu=3800
#SBATCH -C avx512
#SBATCH -A p0024774
#SBATCH -t 02:00:00
#SBATCH --output=eos_%j.out
#SBATCH --error=eos_%j.err

EMTODIR=/home/hpleva/EMTO5.8
KGRN=$EMTODIR/kgrn/kgrn_cpa
KFCD=$EMTODIR/kfcd/kfcd_cpa
WDIR=$(dirname "$(readlink -f "$0")")
cd "$WDIR"

for kgrn_in in fec_bcc_1.*.kgrn; do
    base=${kgrn_in%.kgrn}
    (
        $KGRN < "${base}.kgrn" > "${base}_kgrn.output" 2>&1
        $KFCD < "${base}.kfcd" > "${base}_kfcd.output" 2>&1
    ) &
done

wait
echo "All 7 SWS points finished."
