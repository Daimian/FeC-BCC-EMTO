#!/bin/bash

#SBATCH -J bcc
#SBATCH -t 01:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc/bcc.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc/bcc.error

$HOME/EMTO5.8/bmdl/bmdl < /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc/bcc.bmdl > /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc/bcc_bmdl.output
$HOME/EMTO5.8/kstr/kstr < /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc/bcc.kstr > /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc/bcc_kstr.output
$HOME/EMTO5.8/kstr/kstr < /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc/bccM.kstr > /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc/bccM_kstr.output
$HOME/EMTO5.8/shape/shape < /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc/bcc.shape > /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc/bcc_shape.output
