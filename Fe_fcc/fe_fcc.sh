#!/bin/bash

#SBATCH -J fe_fcc
#SBATCH -t 01:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/Fe_fcc/fe_fcc.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/Fe_fcc/fe_fcc.error

$HOME/EMTO5.8/bmdl/bmdl < /home/dm/workplace/FeC-BCC-EMTO/Fe_fcc/fe_fcc.bmdl > /home/dm/workplace/FeC-BCC-EMTO/Fe_fcc/fe_fcc_bmdl.output
$HOME/EMTO5.8/kstr/kstr < /home/dm/workplace/FeC-BCC-EMTO/Fe_fcc/fe_fcc.kstr > /home/dm/workplace/FeC-BCC-EMTO/Fe_fcc/fe_fcc_kstr.output
$HOME/EMTO5.8/shape/shape < /home/dm/workplace/FeC-BCC-EMTO/Fe_fcc/fe_fcc.shape > /home/dm/workplace/FeC-BCC-EMTO/Fe_fcc/fe_fcc_shape.output
