#!/bin/bash

#SBATCH -J fe16c1
#SBATCH -t 01:00:00
#SBATCH -o /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_sc17/fe16c1.output
#SBATCH -e /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_sc17/fe16c1.error

$HOME/EMTO5.8/bmdl/bmdl < /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_sc17/fe16c1.bmdl > /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_sc17/fe16c1_bmdl.output
$HOME/EMTO5.8/kstr/kstr < /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_sc17/fe16c1.kstr > /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_sc17/fe16c1_kstr.output
$HOME/EMTO5.8/kstr/kstr < /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_sc17/fe16c1M.kstr > /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_sc17/fe16c1M_kstr.output
$HOME/EMTO5.8/shape/shape < /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_sc17/fe16c1.shape > /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_sc17/fe16c1_shape.output
