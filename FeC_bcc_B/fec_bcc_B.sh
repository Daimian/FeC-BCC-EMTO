#!/bin/bash

#SBATCH -J fec_bcc_B
#SBATCH -t 01:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B.error

$HOME/EMTO5.8/bmdl/bmdl < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B.bmdl > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B_bmdl.output
$HOME/EMTO5.8/kstr/kstr < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B.kstr > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B_kstr.output
$HOME/EMTO5.8/shape/shape < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B.shape > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc_B/fec_bcc_B_shape.output
