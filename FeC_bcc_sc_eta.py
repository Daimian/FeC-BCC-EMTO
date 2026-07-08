#!/usr/bin/env python3
"""
Fe16C1 supercell: S(ws)_C scan at fixed w=2.65 Bohr, c/a=1.0.
Scan S(ws)_C = 0.40-0.60 to find optimal carbon sphere radius.

17 atoms: 16 Fe (BCC 2x2x2) + 1 C (z-type octahedral interstitial).
No CPA - each site is 100% single element.
"""

import os
import numpy as np
import pyemto

# === Paths ===
folder = os.path.abspath("./FeC_bcc_sc")
latpath = "../lattice/bcc_sc17"

# === Fixed parameters ===
sws_fixed = 2.65  # Bohr, near Al-Zoubi equilibrium w_eq=2.646

# === S(ws)_C scan ===
s_ws_C_values = [0.40, 0.45, 0.50, 0.55, 0.60]

# === 17-atom basis (fractional coords in SC supercell) ===
basis = np.array([
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
    # 1 C — z-type octahedral interstitial
    [0.00, 0.00, 0.25],
])

# === KGRN atom arrays (NQ=17, NT=2) ===
atoms = np.array(['Fe'] * 16 + ['C'])
iqs   = np.arange(1, 18, dtype='int32')
its   = np.array([1] * 16 + [2], dtype='int32')
itas  = np.array([1] * 17, dtype='int32')
concs = np.array([100.0] * 17)
splts = np.array([2.0] * 16 + [0.0])

# === Create output directory and symlinks ===
os.makedirs(folder, exist_ok=True)
for d in ['bmdl', 'kstr', 'shape']:
    link = os.path.join(folder, d)
    target = os.path.join('..', 'lattice', 'bcc_sc17', d)
    if os.path.islink(link):
        os.unlink(link)
    elif os.path.isdir(link):
        import shutil
        shutil.rmtree(link)
    os.symlink(target, link)

# === Generate KGRN/KFCD for each S(ws)_C ===
sys = pyemto.System(folder=folder)

for s_ws_C in s_ws_C_values:
    # Volume conservation: 16*S(ws)_Fe^3 + S(ws)_C^3 = 17
    s_ws_Fe = ((17.0 - s_ws_C**3) / 16.0) ** (1.0 / 3.0)

    s_wss   = np.array([s_ws_Fe] * 16 + [s_ws_C])
    ws_wsts = np.array([s_ws_Fe] * 16 + [s_ws_C])

    jobname = f'fe16c1_swsc{s_ws_C:.2f}'

    print(f"S(ws)_C = {s_ws_C:.2f}, S(ws)_Fe = {s_ws_Fe:.6f}")

    sys.bulk_new(
        lat='sc',
        jobname=jobname,
        latname='fe16c1',
        latpath=latpath,
        ibz=1,
        basis=basis,
        atoms=atoms,
        iqs=iqs,
        its=its,
        itas=itas,
        concs=concs,
        splts=splts,
        sws=sws_fixed,
        s_wss=s_wss,
        ws_wsts=ws_wsts,
        afm='F',
        xc='PBE',
        expan='S',
        sofc='Y',
        niter=500,
        ncpa=1,
        amix=0.02,
        efmix=1.0,
        tole=1.0e-7,
        tolef=1.0e-7,
        mmom=2.2,
        nkx=9,
        nky=9,
        nkz=9,
        lmaxh=8,
        lmaxt=4,
        depth=0.6,
        imagz=0.02,
        tfermi=500.0,
        ncpu=4,
    )

    sys.emto.kgrn.write_input_file(folder=folder)
    sys.emto.kfcd.write_input_file(folder=folder)
    sys.emto.batch.write_input_file(folder=folder)

    print(f"  Generated {jobname}")

print(f"\nAll input files written to: {folder}")
print("Run lattice/gen_lattice.py first (if not already done), then run_eos.sh.")
