#!/bin/bash

#SBATCH -J fcc_oct
#SBATCH -t 01:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc_oct/fcc_oct.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc_oct/fcc_oct.error

$HOME/EMTO5.8/bmdl/bmdl < /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc_oct/fcc_oct.bmdl > /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc_oct/fcc_oct_bmdl.output
$HOME/EMTO5.8/kstr/kstr < /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc_oct/fcc_oct.kstr > /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc_oct/fcc_oct_kstr.output
$HOME/EMTO5.8/kstr/kstr < /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc_oct/fcc_octM.kstr > /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc_oct/fcc_octM_kstr.output
$HOME/EMTO5.8/shape/shape < /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc_oct/fcc_oct.shape > /home/dm/workplace/FeC-BCC-EMTO/lattice/fcc_oct/fcc_oct_shape.output
