#!/usr/bin/env python3
"""
Generate EMTO-CPA input files for BCC Nb + C (octahedral interstitial).

SC conventional cell (LAT=1), NQ=8 (2 metal + 6 octahedral sites).
Non-magnetic, PBE, SWS scan for EOS fitting.
Uses shared lattice files from lattice/bcc_oct/.
"""

import os
import numpy as np
import pyemto

# === Paths ===
folder = os.path.abspath("./NbC_bcc")
latpath = "../lattice/bcc_oct"

# === Physical parameters ===
# Nb BCC: a = 3.3008 Å
# NQ=8 (2 metal + 6 octahedral), conventional cell volume = a^3
# SWS = [3 * a^3 / (4*pi*NQ)]^(1/3)
a_bohr = 3.3008 * 1.8897259886
sws_center = (3.0 * a_bohr**3 / (4.0 * np.pi * 8))**(1.0/3.0)
print(f"Estimated SWS (NQ=8): {sws_center:.4f} a.u.")

# === Wigner-Seitz sphere radii ===
# Literature: C interstitial S(ws) = 0.77 (23% smaller)
# Metal atoms use default S(ws) = 1.0.
s_ws_C  = 0.77
s_ws_Nb = 1.0
print(f"S(ws): Nb = {s_ws_Nb:.4f}, C/Va = {s_ws_C:.4f}")

# === Carbon concentration ===
# 2 at% C on each octahedral sublattice
conc_C = 2.0
conc_Va = 100.0 - conc_C

# === KGRN atom block ===
# IQ=1,2: Nb (metal sites, IT=1)
# IQ=3-8: Va+C (octahedral, IT=2)
atoms = np.array([
    'Nb', 'Nb',
    'Va', 'C', 'Va', 'C', 'Va', 'C',
    'Va', 'C', 'Va', 'C', 'Va', 'C',
])
iqs = np.array([
    1, 2,
    3, 3, 4, 4, 5, 5,
    6, 6, 7, 7, 8, 8,
], dtype='int32')
its = np.array([
    1, 1,
    2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2,
], dtype='int32')
itas = np.array([
    1, 1,
    1, 2, 1, 2, 1, 2,
    1, 2, 1, 2, 1, 2,
], dtype='int32')
concs = np.array([
    100.0, 100.0,
    conc_Va, conc_C, conc_Va, conc_C, conc_Va, conc_C,
    conc_Va, conc_C, conc_Va, conc_C, conc_Va, conc_C,
])
splts = np.array([
    0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
])
s_wss = np.array([
    s_ws_Nb, s_ws_Nb,
    s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C,
    s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C,
])
ws_wsts = np.array([
    s_ws_Nb, s_ws_Nb,
    s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C,
    s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C,
])

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
nbc = pyemto.System(folder=folder)

for i, sws_val in enumerate(sws_range):
    nbc.bulk_new(
        lat='sc',
        jobname='nbc_bcc',
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
        ncpa=30,
        tolcpa=1.0e-6,
        alpcpa=0.602,
        amix=0.02,
        efmix=1.0,
        tole=1.0e-7,
        tolef=1.0e-7,
        mmom=0.0,
        nky=21,
        nkx=21,
        nkz=21,
        ncpu=8,
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

    nbc.emto.kgrn.write_input_file(folder=folder)
    nbc.emto.kfcd.write_input_file(folder=folder)
    nbc.emto.batch.write_input_file(folder=folder)

    print(f"  Generated SWS = {sws_val:.4f} a.u.")

print(f"\nAll input files written to: {folder}")
