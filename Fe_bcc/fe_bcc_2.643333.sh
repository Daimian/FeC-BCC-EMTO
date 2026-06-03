#!/bin/bash

#SBATCH -J fe_bcc_2.643333
#SBATCH -t 02:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc_2.643333.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc_2.643333.error

/home/hpleva/EMTO5.8/kgrn/kgrn_cpa < /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc_2.643333.kgrn > /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc_2.643333_kgrn.output
/home/hpleva/EMTO5.8/kfcd/kfcd_cpa < /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc_2.643333.kfcd > /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc_2.643333_kfcd.output
