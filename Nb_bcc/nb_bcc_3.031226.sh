#!/bin/bash

#SBATCH -J nb_bcc_3.031226
#SBATCH -t 02:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/Nb_bcc/nb_bcc_3.031226.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/Nb_bcc/nb_bcc_3.031226.error

/home/hpleva/EMTO5.8/kgrn/kgrn_cpa < /home/dm/workplace/FeC-BCC-EMTO/Nb_bcc/nb_bcc_3.031226.kgrn > /home/dm/workplace/FeC-BCC-EMTO/Nb_bcc/nb_bcc_3.031226_kgrn.output
/home/hpleva/EMTO5.8/kfcd/kfcd_cpa < /home/dm/workplace/FeC-BCC-EMTO/Nb_bcc/nb_bcc_3.031226.kfcd > /home/dm/workplace/FeC-BCC-EMTO/Nb_bcc/nb_bcc_3.031226_kfcd.output
