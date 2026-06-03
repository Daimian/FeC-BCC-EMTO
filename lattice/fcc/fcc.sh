#!/bin/bash

#SBATCH -J fcc
#SBATCH -t 01:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc/fcc.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc/fcc.error

$HOME/EMTO5.8/bmdl/bmdl < /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc/fcc.bmdl > /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc/fcc_bmdl.output
$HOME/EMTO5.8/kstr/kstr < /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc/fcc.kstr > /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc/fcc_kstr.output
$HOME/EMTO5.8/shape/shape < /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc/fcc.shape > /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc/fcc_shape.output
