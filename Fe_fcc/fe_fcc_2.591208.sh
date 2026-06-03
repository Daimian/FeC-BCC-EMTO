#!/bin/bash

#SBATCH -J fe_fcc_2.591208
#SBATCH -t 02:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/Fe_fcc/fe_fcc_2.591208.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/Fe_fcc/fe_fcc_2.591208.error

/home/hpleva/EMTO5.8/kgrn/kgrn_cpa < /home/dm/workplace/FeC-BCC-EMTO/Fe_fcc/fe_fcc_2.591208.kgrn > /home/dm/workplace/FeC-BCC-EMTO/Fe_fcc/fe_fcc_2.591208_kgrn.output
/home/hpleva/EMTO5.8/kfcd/kfcd_cpa < /home/dm/workplace/FeC-BCC-EMTO/Fe_fcc/fe_fcc_2.591208.kfcd > /home/dm/workplace/FeC-BCC-EMTO/Fe_fcc/fe_fcc_2.591208_kfcd.output
