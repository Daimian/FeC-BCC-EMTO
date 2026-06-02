#!/bin/bash

#SBATCH -J fec_bcc
#SBATCH -t 01:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc/fec_bcc.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc/fec_bcc.error

$HOME/EMTO5.8/bmdl/bmdl < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc/fec_bcc.bmdl > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc/fec_bcc_bmdl.output
$HOME/EMTO5.8/kstr/kstr < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc/fec_bcc.kstr > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc/fec_bcc_kstr.output
$HOME/EMTO5.8/shape/shape < /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc/fec_bcc.shape > /home/dm/workplace/FeC-BCC-EMTO/FeC_bcc/fec_bcc_shape.output
