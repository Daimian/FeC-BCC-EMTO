#!/bin/bash

#SBATCH -J fe_bcc_2.576667
#SBATCH -t 02:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc_2.576667.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc_2.576667.error

/home/hpleva/EMTO5.8/kgrn/kgrn_cpa < /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc_2.576667.kgrn > /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc_2.576667_kgrn.output
/home/hpleva/EMTO5.8/kfcd/kfcd_cpa < /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc_2.576667.kfcd > /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc_2.576667_kfcd.output
