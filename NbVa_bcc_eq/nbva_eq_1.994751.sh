#!/bin/bash

#SBATCH -J nbva_eq_1.994751
#SBATCH -t 02:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/NbVa_bcc_eq/nbva_eq_1.994751.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/NbVa_bcc_eq/nbva_eq_1.994751.error

/home/hpleva/EMTO5.8/kgrn/kgrn_cpa < /home/dm/workplace/FeC-BCC-EMTO/NbVa_bcc_eq/nbva_eq_1.994751.kgrn > /home/dm/workplace/FeC-BCC-EMTO/NbVa_bcc_eq/nbva_eq_1.994751_kgrn.output
/home/hpleva/EMTO5.8/kfcd/kfcd_cpa < /home/dm/workplace/FeC-BCC-EMTO/NbVa_bcc_eq/nbva_eq_1.994751.kfcd > /home/dm/workplace/FeC-BCC-EMTO/NbVa_bcc_eq/nbva_eq_1.994751_kfcd.output
