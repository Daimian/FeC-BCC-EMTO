#!/usr/bin/env python3
"""
Generate EMTO-CPA input files for BCC Nb + 100% Va (no Carbon).
SC conventional cell (LAT=1), NQ=8 (2 metal + 6 octahedral vacancy sites).
Test case to isolate interstitial structure issues from C chemistry.
Uses shared lattice files from lattice/bcc_oct/.
"""

import os
import numpy as np
import pyemto

# === Paths ===
folder = os.path.abspath("./NbVa_bcc")
latpath = "../lattice/bcc_oct"

# === Physical parameters ===
# Nb BCC: a = 3.3008 Å
a_bohr = 3.3008 * 1.8897259886
sws_center = (3.0 * a_bohr**3 / (4.0 * np.pi * 8))**(1.0/3.0)
print(f"Estimated SWS (NQ=8): {sws_center:.4f} a.u.")

# === Wigner-Seitz sphere radii ===
s_ws_Va = 0.77
s_ws_Nb = 1.0

# === KGRN atom block ===
# 100% Va on all interstitial sites (no C, no CPA needed for IT=2)
atoms = np.array([
    'Nb', 'Nb',
    'Va', 'Va', 'Va', 'Va', 'Va', 'Va',
])
iqs = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype='int32')
its = np.array([1, 1, 2, 2, 2, 2, 2, 2], dtype='int32')
itas = np.array([1, 1, 1, 1, 1, 1, 1, 1], dtype='int32')
concs = np.array([100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0])
splts = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
s_wss = np.array([s_ws_Nb, s_ws_Nb, s_ws_Va, s_ws_Va, s_ws_Va, s_ws_Va, s_ws_Va, s_ws_Va])
ws_wsts = np.array([s_ws_Nb, s_ws_Nb, s_ws_Va, s_ws_Va, s_ws_Va, s_ws_Va, s_ws_Va, s_ws_Va])

# === SWS scan range ===
n_sws = 7
sws_range = np.linspace(sws_center - 0.06, sws_center + 0.06, n_sws)
print(f"SWS scan: {sws_range}")

# === Create symlinks to shared lattice output ===
os.makedirs(folder, exist_ok=True)
for d in ['bmdl', 'kstr', 'shape']:
    link = os.path.join(folder, d)
    target = os.path.join('..', 'lattice', 'bcc_oct', d)
    if os.path.islink(link):
        os.unlink(link)
    elif os.path.isdir(link):
        import shutil
        shutil.rmtree(link)
    os.symlink(target, link)

# === Create System and generate KGRN/KFCD ===
nb = pyemto.System(folder=folder)

for i, sws_val in enumerate(sws_range):
    nb.bulk_new(
        lat='sc',
        jobname='nbva_bcc',
        latname='bcc_oct',
        latpath=latpath,
        ibz=1,
        atoms=atoms,
        iqs=iqs,
        its=its,
        itas=itas,
        concs=concs,
        splts=splts,
        sws=sws_val,
        s_wss=s_wss,
        ws_wsts=ws_wsts,
        afm='P',
        xc='PBE',
        expan='S',
        sofc='Y',
        niter=500,
        amix=0.02,
        efmix=1.0,
        tole=1.0e-7,
        tolef=1.0e-7,
        mmom=0.0,
        nky=11,
        nkx=11,
        nkz=11,
        ncpu=1,
        lmaxh=8,
        lmaxt=4,
        tfermi=500.0,
        depth=1.0,
        imagz=0.02,
        efgs=0.2,
        hx=0.2,
        nx=11,
        nz0=9,
    )

    nb.emto.kgrn.write_input_file(folder=folder)
    nb.emto.kfcd.write_input_file(folder=folder)
    nb.emto.batch.write_input_file(folder=folder)

    print(f"  Generated SWS = {sws_val:.4f} a.u.")

print(f"\nAll input files written to: {folder}")
