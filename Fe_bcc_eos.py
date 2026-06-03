#!/usr/bin/env python3
"""
Generate EMTO input files for pure BCC Fe (NQ=1).
FM (ferromagnetic), PBE, SWS scan for EOS fitting.
Reference calculation for validating interstitial models.
"""

import os
import numpy as np
import pyemto

# === Paths ===
folder = os.path.abspath("./Fe_bcc")
latpath = "."

# === Physical parameters ===
# alpha-Fe: a = 2.866 Å = 5.416 a.u.
# NQ=1, BCC primitive cell volume = a^3/2
# SWS = [3 * a^3/2 / (4*pi)]^(1/3)
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
sws_range = np.linspace(2.607, 2.667, n_sws)
print(f"SWS scan: {sws_range}")

# === Create System ===
fe = pyemto.System(folder=folder)

# Set lattice structure (BMDL/KSTR/SHAPE)
fe.lattice.set_values(
    jobname_lat='fe_bcc',
    latpath=latpath,
    lat='bcc',
)
fe.lattice.write_structure_input_files(folder=folder, jobname_lat='fe_bcc')

# Set KGRN/KFCD parameters and generate SWS scan
for i, sws_val in enumerate(sws_range):
    fe.bulk_new(
        lat='bcc',
        jobname='fe_bcc',
        latname='fe_bcc',
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
