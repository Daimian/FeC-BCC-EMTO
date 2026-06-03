#!/usr/bin/env python3
"""
Generate EMTO input files for pure FCC Fe (NQ=1).
DLM paramagnetic, PBE, SWS scan for EOS fitting.
Uses shared lattice files from lattice/fcc/.
"""

import os
import numpy as np
import pyemto

# === Paths ===
folder = os.path.abspath("./Fe_fcc")
latpath = "../lattice/fcc"

# === Physical parameters ===
# gamma-Fe: a ~ 3.59 Å (experimental high-T)
a_bohr = 3.59 * 1.8897259886
sws_center = (3.0 * a_bohr**3 / 4.0 / (4.0 * np.pi))**(1.0/3.0)
print(f"Estimated SWS (NQ=1, FCC): {sws_center:.4f} a.u.")

# === KGRN atom block ===
# DLM: Fe_up 50% + Fe_dn 50% on the same site
atoms = np.array(['Fe', 'Fe'])
iqs   = np.array([1, 1], dtype='int32')
its   = np.array([1, 1], dtype='int32')
itas  = np.array([1, 2], dtype='int32')
concs = np.array([50.0, 50.0])
splts = np.array([2.0, -2.0])

# === SWS scan range ===
n_sws = 7
sws_range = np.linspace(sws_center - 0.06, sws_center + 0.06, n_sws)
print(f"SWS scan: {sws_range}")

# === Create symlinks to shared lattice output ===
os.makedirs(folder, exist_ok=True)
for d in ['bmdl', 'kstr', 'shape']:
    link = os.path.join(folder, d)
    target = os.path.join('..', 'lattice', 'fcc', d)
    if os.path.islink(link):
        os.unlink(link)
    elif os.path.isdir(link):
        import shutil
        shutil.rmtree(link)
    os.symlink(target, link)

# === Create System and generate KGRN/KFCD ===
fe = pyemto.System(folder=folder)

for i, sws_val in enumerate(sws_range):
    fe.bulk_new(
        lat='fcc',
        jobname='fe_fcc',
        latname='fcc',
        latpath=latpath,
        ibz=2,
        atoms=atoms,
        iqs=iqs,
        its=its,
        itas=itas,
        concs=concs,
        splts=splts,
        sws=sws_val,
        afm='m',
        xc='PBE',
        expan='S',
        sofc='Y',
        niter=500,
        amix=0.02,
        efmix=1.0,
        tole=1.0e-7,
        tolef=1.0e-7,
        mmom=2.0,
        ncpa=30,
        tolcpa=1.0e-6,
        alpcpa=0.602,
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

    fe.emto.kgrn.write_input_file(folder=folder)
    fe.emto.kfcd.write_input_file(folder=folder)
    fe.emto.batch.write_input_file(folder=folder)

    print(f"  Generated SWS = {sws_val:.4f} a.u.")

print(f"\nAll input files written to: {folder}")
