#!/bin/bash

#SBATCH -J fec_fcc_2.164265
#SBATCH -t 02:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/FeC_fcc/fec_fcc_2.164265.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/FeC_fcc/fec_fcc_2.164265.error

/home/hpleva/EMTO5.8/kgrn/kgrn_cpa < /home/dm/workplace/FeC-BCC-EMTO/FeC_fcc/fec_fcc_2.164265.kgrn > /home/dm/workplace/FeC-BCC-EMTO/FeC_fcc/fec_fcc_2.164265_kgrn.output
/home/hpleva/EMTO5.8/kfcd/kfcd_cpa < /home/dm/workplace/FeC-BCC-EMTO/FeC_fcc/fec_fcc_2.164265.kfcd > /home/dm/workplace/FeC-BCC-EMTO/FeC_fcc/fec_fcc_2.164265_kfcd.output
