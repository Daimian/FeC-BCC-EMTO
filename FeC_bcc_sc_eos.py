#!/usr/bin/env python3
"""
Fe16C1 supercell: EOS at c/a=1.0, fixed S(ws)_C.
SWS scan: 2.60-2.70 Bohr, 7 points.
Update s_ws_C below after Step 1 (eta scan) completes.

17 atoms: 16 Fe (BCC 2x2x2) + 1 C (z-type octahedral interstitial).
No CPA - each site is 100% single element.
"""

import os
import numpy as np
import pyemto

# === Paths ===
folder = os.path.abspath("./FeC_bcc_sc")
latpath = "../lattice/bcc_sc17"

# === Optimal S(ws)_C from Step 1 (update after eta scan) ===
s_ws_C = 0.50

# === Volume conservation ===
s_ws_Fe = ((17.0 - s_ws_C**3) / 16.0) ** (1.0 / 3.0)
print(f"S(ws)_C = {s_ws_C:.4f}, S(ws)_Fe = {s_ws_Fe:.6f}")

# === SWS scan range ===
n_sws = 7
sws_range = np.linspace(2.60, 2.70, n_sws)
print(f"SWS scan: {sws_range}")

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
s_wss   = np.array([s_ws_Fe] * 16 + [s_ws_C])
ws_wsts = np.array([s_ws_Fe] * 16 + [s_ws_C])

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

# === Generate KGRN/KFCD for each SWS ===
sys = pyemto.System(folder=folder)

for sws_val in sws_range:
    # NOTE: pyemto.System.create_jobname() always appends "_{sws:8.6f}" to
    # the jobname we pass in. Keep jobname constant ('fe16c1') here so the
    # auto-appended sws value produces fe16c1_2.650000.kgrn etc. (not a
    # duplicated fe16c1_2.650000_2.650000.kgrn).
    jobname = 'fe16c1'

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
        sws=sws_val,
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

    print(f"  Generated SWS = {sws_val:.6f} a.u.")

print(f"\nAll input files written to: {folder}")
print("Run lattice/gen_lattice.py first (if not already done), then run_eos_sws.sh.")
