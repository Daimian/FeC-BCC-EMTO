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

# === FCC + octahedral interstitial (FCC primitive cell, NQ=2) ===
folder = os.path.abspath("./fcc_oct")
os.makedirs(folder, exist_ok=True)

basis_fcc_oct = np.array([
    [0.0, 0.0, 0.0],       # Metal
    [0.5, 0.5, 0.5],       # Octahedral interstitial
])

sys = pyemto.System(folder=folder)
sys.lattice.set_values(
    jobname_lat='fcc_oct',
    latpath='.',
    lat='fcc',
    basis=basis_fcc_oct,
    kappaw=[0.0, -0.2],
)
sys.lattice.write_structure_input_files(folder=folder, jobname_lat='fcc_oct')
print(f"Generated fcc_oct structure files in: {folder}")

# === BCC 2x2x2 supercell: Fe16C1 (triclinic, NQ=17) ===
# Using LAT=14 (stric) for full flexibility over c/a ratio.
# c/a=1.0 → BCC; c/a≠1 → BCT (martensite).
ca = 1.0
folder = os.path.abspath("./bcc_sc17")
os.makedirs(folder, exist_ok=True)

basis_sc17 = np.array([
    # 8 Fe — corner sublattice
    [0.00, 0.00, 0.00], [0.50, 0.00, 0.00],
    [0.00, 0.50, 0.00], [0.00, 0.00, 0.50],
    [0.50, 0.50, 0.00], [0.50, 0.00, 0.50],
    [0.00, 0.50, 0.50], [0.50, 0.50, 0.50],
    # 8 Fe — body-center sublattice
    [0.25, 0.25, 0.25], [0.75, 0.25, 0.25],
    [0.25, 0.75, 0.25], [0.25, 0.25, 0.75],
    [0.75, 0.75, 0.25], [0.75, 0.25, 0.75],
    [0.25, 0.75, 0.75], [0.75, 0.75, 0.75],
    # 1 C — z-type octahedral interstitial (Zener ordered)
    [0.00, 0.00, 0.25],
])

# Site-specific a/w: 0.70 for Fe (IQ 1-16), 0.50 for C interstitial (IQ 17)
nq = 17
nl = 4
awIQ = np.ones((nq, nl)) * 0.70
awIQ[16, :] = 0.50

sys = pyemto.System(folder=folder)
sys.lattice.set_values(
    jobname_lat='fe16c1',
    latpath='.',
    lat='stric',
    latvectors=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, ca]],
    latparams=[1.0, 1.0, 1.0],
    basis=basis_sc17,
    kappaw=[0.0, -0.2],
    awIQ=awIQ,
)
sys.lattice.write_structure_input_files(folder=folder, jobname_lat='fe16c1')
print(f"Generated bcc_sc17 (Fe16C1) structure files in: {folder}")
