#!/bin/bash

#SBATCH -J fec_bcc_1.739895
#SBATCH -t 02:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc/fec_bcc_1.739895.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc/fec_bcc_1.739895.error

/home/hpleva/EMTO5.8/kgrn/kgrn_cpa < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc/fec_bcc_1.739895.kgrn > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc/fec_bcc_1.739895_kgrn.output
/home/hpleva/EMTO5.8/kfcd/kfcd_cpa < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc/fec_bcc_1.739895.kfcd > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc/fec_bcc_1.739895_kfcd.output
