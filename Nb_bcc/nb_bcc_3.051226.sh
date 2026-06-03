#!/bin/bash

#SBATCH -J nb_bcc_3.051226
#SBATCH -t 02:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/Nb_bcc/nb_bcc_3.051226.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/Nb_bcc/nb_bcc_3.051226.error

/home/hpleva/EMTO5.8/kgrn/kgrn_cpa < /home/dm/workplace/FeC-BCC-EMTO/Nb_bcc/nb_bcc_3.051226.kgrn > /home/dm/workplace/FeC-BCC-EMTO/Nb_bcc/nb_bcc_3.051226_kgrn.output
/home/hpleva/EMTO5.8/kfcd/kfcd_cpa < /home/dm/workplace/FeC-BCC-EMTO/Nb_bcc/nb_bcc_3.051226.kfcd > /home/dm/workplace/FeC-BCC-EMTO/Nb_bcc/nb_bcc_3.051226_kfcd.output
