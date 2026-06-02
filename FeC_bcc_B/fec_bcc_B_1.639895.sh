#!/bin/bash

#SBATCH -J fec_bcc_B_1.639895
#SBATCH -t 02:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B_1.639895.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B_1.639895.error

/home/hpleva/EMTO5.8/kgrn/kgrn_cpa < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B_1.639895.kgrn > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B_1.639895_kgrn.output
/home/hpleva/EMTO5.8/kfcd/kfcd_cpa < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B_1.639895.kfcd > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B_1.639895_kfcd.output
