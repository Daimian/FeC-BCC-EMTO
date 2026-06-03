#!/bin/bash

#SBATCH -J fe_bcc
#SBATCH -t 01:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc.error

$HOME/EMTO5.8/bmdl/bmdl < /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc.bmdl > /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc_bmdl.output
$HOME/EMTO5.8/kstr/kstr < /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc.kstr > /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc_kstr.output
$HOME/EMTO5.8/shape/shape < /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc.shape > /home/dm/workplace/FeC-BCC-EMTO/Fe_bcc/fe_bcc_shape.output
