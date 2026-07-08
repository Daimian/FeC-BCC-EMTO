#!/bin/bash

#SBATCH -J fe16c1_2.683333
#SBATCH -t 02:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_sc/fe16c1_2.683333.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_sc/fe16c1_2.683333.error

/home/hpleva/EMTO5.8/kgrn/kgrn_cpa < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_sc/fe16c1_2.683333.kgrn > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_sc/fe16c1_2.683333_kgrn.output
/home/hpleva/EMTO5.8/kfcd/kfcd_cpa < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_sc/fe16c1_2.683333.kfcd > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_sc/fe16c1_2.683333_kfcd.output
