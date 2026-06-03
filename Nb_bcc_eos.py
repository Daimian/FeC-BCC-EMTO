#!/usr/bin/env python3
"""
Generate EMTO input files for pure BCC Nb (NQ=1).
Non-magnetic, PBE, SWS scan for EOS fitting.
"""

import os
import numpy as np
import pyemto

# === Paths ===
folder = os.path.abspath("./Nb_bcc")
latpath = "."

# === Physical parameters ===
# Nb BCC: a = 3.3008 Å
# NQ=1, BCC primitive cell volume = a^3/2
a_bohr = 3.3008 * 1.8897259886
sws_center = (3.0 * a_bohr**3 / 2.0 / (4.0 * np.pi))**(1.0/3.0)
print(f"Estimated SWS (NQ=1): {sws_center:.4f} a.u.")

# === KGRN atom block ===
atoms = np.array(['Nb'])
iqs   = np.array([1], dtype='int32')
its   = np.array([1], dtype='int32')
itas  = np.array([1], dtype='int32')
concs = np.array([100.0])
splts = np.array([0.0])

# === SWS scan range ===
n_sws = 7
sws_range = np.linspace(sws_center - 0.06, sws_center + 0.06, n_sws)
print(f"SWS scan: {sws_range}")

# === Create System ===
nb = pyemto.System(folder=folder)

# Set lattice structure (BMDL/KSTR/SHAPE)
nb.lattice.set_values(
    jobname_lat='nb_bcc',
    latpath=latpath,
    lat='bcc',
)
nb.lattice.write_structure_input_files(folder=folder, jobname_lat='nb_bcc')

# Set KGRN/KFCD parameters and generate SWS scan
for i, sws_val in enumerate(sws_range):
    nb.bulk_new(
        lat='bcc',
        jobname='nb_bcc',
        latname='nb_bcc',
        latpath=latpath,
        ibz=3,
        atoms=atoms,
        iqs=iqs,
        its=its,
        itas=itas,
        concs=concs,
        splts=splts,
        sws=sws_val,
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

    nb.emto.kgrn.write_input_file(folder=folder)
    nb.emto.kfcd.write_input_file(folder=folder)
    nb.emto.batch.write_input_file(folder=folder)

    print(f"  Generated SWS = {sws_val:.4f} a.u.")

print(f"\nAll input files written to: {folder}")
