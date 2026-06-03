#!/usr/bin/env python3
"""
Generate EMTO input files for pure BCC Fe (NQ=1).
FM (ferromagnetic), PBE, SWS scan for EOS fitting.
Uses shared lattice files from lattice/bcc/.
"""

import os
import numpy as np
import pyemto

# === Paths ===
folder = os.path.abspath("./Fe_bcc")
latpath = "../lattice/bcc"

# === Physical parameters ===
# alpha-Fe: a = 2.866 Å = 5.416 a.u.
a_bohr = 2.866 * 1.8897259886
sws_center = (3.0 * a_bohr**3 / 2.0 / (4.0 * np.pi))**(1.0/3.0)
print(f"Estimated SWS (NQ=1): {sws_center:.4f} a.u.")

# === KGRN atom block ===
atoms = np.array(['Fe'])
iqs   = np.array([1], dtype='int32')
its   = np.array([1], dtype='int32')
itas  = np.array([1], dtype='int32')
concs = np.array([100.0])
splts = np.array([2.0])

# === SWS scan range ===
n_sws = 7
sws_range = np.linspace(2.65, 2.70, n_sws)
print(f"SWS scan: {sws_range}")

# === Create symlinks to shared lattice output ===
os.makedirs(folder, exist_ok=True)
for d in ['bmdl', 'kstr', 'shape']:
    link = os.path.join(folder, d)
    target = os.path.join('..', 'lattice', 'bcc', d)
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
        lat='bcc',
        jobname='fe_bcc',
        latname='bcc',
        latpath=latpath,
        ibz=3,
        atoms=atoms,
        iqs=iqs,
        its=its,
        itas=itas,
        concs=concs,
        splts=splts,
        sws=sws_val,
        afm='F',
        xc='PBE',
        expan='S',
        sofc='Y',
        amix=0.02,
        efmix=1.0,
        niter=500,
        tole=1.0e-7,
        tolef=1.0e-7,
        mmom=2.2,
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
