#!/bin/bash

#SBATCH -J bcc_oct
#SBATCH -t 01:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_oct/bcc_oct.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_oct/bcc_oct.error

$HOME/EMTO5.8/bmdl/bmdl < /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_oct/bcc_oct.bmdl > /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_oct/bcc_oct_bmdl.output
$HOME/EMTO5.8/kstr/kstr < /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_oct/bcc_oct.kstr > /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_oct/bcc_oct_kstr.output
$HOME/EMTO5.8/kstr/kstr < /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_oct/bcc_octM.kstr > /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_oct/bcc_octM_kstr.output
$HOME/EMTO5.8/shape/shape < /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_oct/bcc_oct.shape > /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_oct/bcc_oct_shape.output
