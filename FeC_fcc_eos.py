#!/usr/bin/env python3
"""
Generate EMTO-CPA input files for FCC Fe + C (octahedral interstitial).
Equivalent to Fe24C1 supercell (4.0 at.% C).

FCC primitive cell (LAT=2), NQ=2 (1 metal + 1 octahedral site).
DLM paramagnetic, PBE, SWS scan for EOS fitting.
Uses shared lattice files from lattice/fcc_oct/.
"""

import os
import numpy as np
import pyemto

# === Paths ===
folder = os.path.abspath("./FeC_fcc")
latpath = "../lattice/fcc_oct"

# === Physical parameters ===
# gamma-Fe: a ~ 3.59 Å
# NQ=2 (1 metal + 1 octahedral), FCC primitive cell volume = a^3/4
# SWS = [3 * a^3/4 / (4*pi*NQ)]^(1/3)
a_bohr = 3.59 * 1.8897259886
sws_center = (3.0 * a_bohr**3 / 4.0 / (4.0 * np.pi * 2))**(1.0/3.0)
print(f"Estimated SWS (NQ=2, FCC+oct): {sws_center:.4f} a.u.")

# === Wigner-Seitz sphere radii ===
# Literature: C interstitial S(ws) = 0.77
s_ws_C  = 0.77
s_ws_Fe = 1.0

# === Carbon concentration ===
# Fe24C1: 4.0 at.% C -> on oct sublattice: 100/24 = 4.1667%
conc_C = 100.0 / 24.0
conc_Va = 100.0 - conc_C
print(f"C conc on oct site: {conc_C:.4f}%, Va: {conc_Va:.4f}%")
print(f"Overall: {conc_C/(100+conc_C)*100:.2f} at.% C (Fe24C1 equivalent)")

# === KGRN atom block ===
# NM: single Fe component, no spin splitting
# Oct: Va + C with CPA
atoms = np.array(['Fe', 'Va', 'C'])
iqs   = np.array([1, 2, 2], dtype='int32')
its   = np.array([1, 2, 2], dtype='int32')
itas  = np.array([1, 1, 2], dtype='int32')
concs = np.array([100.0, conc_Va, conc_C])
splts = np.array([0.0, 0.0, 0.0])
s_wss   = np.array([s_ws_Fe, s_ws_C, s_ws_C])
ws_wsts = np.array([s_ws_Fe, s_ws_C, s_ws_C])

# === SWS scan range ===
n_sws = 7
sws_range = np.linspace(sws_center - 0.06, sws_center + 0.06, n_sws)
print(f"SWS scan: {sws_range}")

# === Create symlinks to shared lattice output ===
os.makedirs(folder, exist_ok=True)
for d in ['bmdl', 'kstr', 'shape']:
    link = os.path.join(folder, d)
    target = os.path.join('..', 'lattice', 'fcc_oct', d)
    if os.path.islink(link):
        os.unlink(link)
    elif os.path.isdir(link):
        import shutil
        shutil.rmtree(link)
    os.symlink(target, link)

# === Create System and generate KGRN/KFCD ===
fec = pyemto.System(folder=folder)

for i, sws_val in enumerate(sws_range):
    fec.bulk_new(
        lat='fcc',
        jobname='fec_fcc',
        latname='fcc_oct',
        latpath=latpath,
        ibz=2,
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

    fec.emto.kgrn.write_input_file(folder=folder)
    fec.emto.kfcd.write_input_file(folder=folder)
    fec.emto.batch.write_input_file(folder=folder)

    print(f"  Generated SWS = {sws_val:.4f} a.u.")

print(f"\nAll input files written to: {folder}")
