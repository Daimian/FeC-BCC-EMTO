#!/bin/bash

#SBATCH -J nbva_bcc_1.825000
#SBATCH -t 02:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/NbVa_bcc/nbva_bcc_1.825000.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/NbVa_bcc/nbva_bcc_1.825000.error

/home/hpleva/EMTO5.8/kgrn/kgrn_cpa < /home/dm/workplace/FeC-BCC-EMTO/NbVa_bcc/nbva_bcc_1.825000.kgrn > /home/dm/workplace/FeC-BCC-EMTO/NbVa_bcc/nbva_bcc_1.825000_kgrn.output
/home/hpleva/EMTO5.8/kfcd/kfcd_cpa < /home/dm/workplace/FeC-BCC-EMTO/NbVa_bcc/nbva_bcc_1.825000.kfcd > /home/dm/workplace/FeC-BCC-EMTO/NbVa_bcc/nbva_bcc_1.825000_kfcd.output
