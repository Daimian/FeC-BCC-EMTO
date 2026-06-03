#!/bin/bash

#SBATCH -J nbc_bcc_1.954751
#SBATCH -t 02:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/NbC_bcc/nbc_bcc_1.954751.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/NbC_bcc/nbc_bcc_1.954751.error

/home/hpleva/EMTO5.8/kgrn/kgrn_cpa < /home/dm/workplace/FeC-BCC-EMTO/NbC_bcc/nbc_bcc_1.954751.kgrn > /home/dm/workplace/FeC-BCC-EMTO/NbC_bcc/nbc_bcc_1.954751_kgrn.output
/home/hpleva/EMTO5.8/kfcd/kfcd_cpa < /home/dm/workplace/FeC-BCC-EMTO/NbC_bcc/nbc_bcc_1.954751.kfcd > /home/dm/workplace/FeC-BCC-EMTO/NbC_bcc/nbc_bcc_1.954751_kfcd.output
