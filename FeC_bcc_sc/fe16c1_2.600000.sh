#!/bin/bash

#SBATCH -J fe16c1_2.600000
#SBATCH -t 02:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_sc/fe16c1_2.600000.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_sc/fe16c1_2.600000.error

/home/hpleva/EMTO5.8/kgrn/kgrn_cpa < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_sc/fe16c1_2.600000.kgrn > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_sc/fe16c1_2.600000_kgrn.output
/home/hpleva/EMTO5.8/kfcd/kfcd_cpa < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_sc/fe16c1_2.600000.kfcd > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_sc/fe16c1_2.600000_kfcd.output
