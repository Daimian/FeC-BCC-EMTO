#!/bin/bash

#SBATCH -J fec_bcc_B_1.619895
#SBATCH -t 02:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B_1.619895.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B_1.619895.error

/home/hpleva/EMTO5.8/kgrn/kgrn_cpa < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B_1.619895.kgrn > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B_1.619895_kgrn.output
/home/hpleva/EMTO5.8/kfcd/kfcd_cpa < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B_1.619895.kfcd > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B_1.619895_kfcd.output
