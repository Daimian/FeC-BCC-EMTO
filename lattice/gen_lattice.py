#!/usr/bin/env python3
"""Generate shared BMDL/KSTR/SHAPE input files for all lattice types."""

import os
import numpy as np
import pyemto

# === Simple lattices (NQ=1) ===
# kappaw=[0.0, -0.2] generates both bcc.tfh and bccM.tfh (needed for FCD)
for lat in ['bcc', 'fcc']:
    folder = os.path.abspath(f"./{lat}")
    os.makedirs(folder, exist_ok=True)

    sys = pyemto.System(folder=folder)
    sys.lattice.set_values(
        jobname_lat=lat,
        latpath='.',
        lat=lat,
        kappaw=[0.0, -0.2],
    )
    sys.lattice.write_structure_input_files(folder=folder, jobname_lat=lat)
    print(f"Generated {lat} structure files in: {folder}")

# === BCC + octahedral interstitials (SC conventional cell, NQ=8) ===
folder = os.path.abspath("./bcc_oct")
os.makedirs(folder, exist_ok=True)

basis = np.array([
    [0.0, 0.0, 0.0],       # Fe corner
    [0.5, 0.5, 0.5],       # Fe body center
    [0.5, 0.0, 0.0],       # Oct edge-x
    [0.0, 0.5, 0.0],       # Oct edge-y
    [0.0, 0.0, 0.5],       # Oct edge-z
    [0.0, 0.5, 0.5],       # Oct face-yz
    [0.5, 0.0, 0.5],       # Oct face-xz
    [0.5, 0.5, 0.0],       # Oct face-xy
])

sys = pyemto.System(folder=folder)
sys.lattice.set_values(
    jobname_lat='bcc_oct',
    latpath='.',
    lat='sc',
    basis=basis,
    kappaw=[0.0, -0.2],
)
sys.lattice.write_structure_input_files(folder=folder, jobname_lat='bcc_oct')
print(f"Generated bcc_oct structure files in: {folder}")
