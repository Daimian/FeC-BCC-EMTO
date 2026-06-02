#!/usr/bin/env python3
"""
Generate EMTO-CPA input files for BCC Fe + C (octahedral interstitial).

Scheme A: BCC primitive cell (LAT=2), NQ=4 (1 metal + 3 octahedral sites).
FM (ferromagnetic), PBE, SWS scan for EOS fitting.
"""

import os
import numpy as np
import pyemto

# === Paths ===
folder = os.path.abspath("./FeC_bcc")
latpath = "."

# === Physical parameters ===
# alpha-Fe: a = 2.866 Å = 5.416 a.u.
# NQ=4 (1 metal + 3 octahedral), BCC primitive cell volume = a^3/2
# SWS = [3 * a^3/2 / (4*pi*NQ)]^(1/3)
a_bohr = 2.866 * 1.8897259886  # 5.416 a.u.
sws_center = (3.0 * a_bohr**3 / 2.0 / (4.0 * np.pi * 4))**(1.0/3.0)
print(f"Estimated SWS (NQ=4): {sws_center:.4f} a.u.")

# S(ws) and WS(wst) = 1.0 for all sites (EMTO standard).
# Volume partitioning is handled by SHAPE (Voronoi tessellation).

# === Carbon concentration ===
# 2 at% C on each octahedral sublattice
conc_C = 2.0   # percent on each sublattice
conc_Va = 100.0 - conc_C

# === KGRN atom block ===
# IQ=1: Fe (metal site, IT=1)
# IQ=2: Va+C (octahedral x, IT=2)
# IQ=3: Va+C (octahedral y, IT=2)
# IQ=4: Va+C (octahedral z, IT=2)
atoms = np.array(['Fe',  'Va', 'C',  'Va', 'C',  'Va', 'C'])
iqs   = np.array([1,      2,    2,    3,    3,    4,    4], dtype='int32')
its   = np.array([1,      2,    2,    2,    2,    2,    2], dtype='int32')
itas  = np.array([1,      1,    2,    1,    2,    1,    2], dtype='int32')
concs = np.array([100.0,  conc_Va, conc_C, conc_Va, conc_C, conc_Va, conc_C])
splts = np.array([2.0,    0.0,  0.0,  0.0,  0.0,  0.0,  0.0])

# === BCC primitive cell basis (fractional coordinates) ===
# Metal:         (0, 0, 0)
# Octahedral x:  (0, 1/2, 1/2)
# Octahedral y:  (1/2, 0, 1/2)
# Octahedral z:  (1/2, 1/2, 0)
basis = np.array([
    [0.0, 0.0, 0.0],
    [0.0, 0.5, 0.5],
    [0.5, 0.0, 0.5],
    [0.5, 0.5, 0.0],
])

# === SWS scan range ===
n_sws = 7
sws_range = np.linspace(sws_center - 0.06, sws_center + 0.06, n_sws)
print(f"SWS scan: {sws_range}")

# === Create System ===
fec = pyemto.System(folder=folder)

# Set lattice structure (BMDL/KSTR/SHAPE)
fec.lattice.set_values(
    jobname_lat='fec_bcc',
    latpath=latpath,
    lat='bcc',
    basis=basis,
)
fec.lattice.write_structure_input_files(folder=folder, jobname_lat='fec_bcc')

# Set KGRN/KFCD parameters and generate SWS scan
for i, sws_val in enumerate(sws_range):
    fec.bulk_new(
        lat='bcc',
        jobname='fec_bcc',
        latname='fec_bcc',
        latpath=latpath,
        ibz=3,             # IBZ=3 for BCC
        atoms=atoms,
        iqs=iqs,
        its=its,
        itas=itas,
        concs=concs,
        splts=splts,
        sws=sws_val,
        afm='F',           # Ferromagnetic
        xc='PBE',
        expan='S',         # Single-Taylor expansion
        sofc='Y',          # Soft-core
        niter=100,
        ncpa=30,           # More CPA iterations for empty spheres
        tolcpa=1.0e-6,
        alpcpa=0.602,
        amix=0.05,
        efmix=1.0,
        tole=1.0e-7,
        tolef=1.0e-7,
        mmom=2.2,
        nky=21,
        nkx=21,
        nkz=21,
        lmaxh=8,
        lmaxt=4,           # spdfg basis for interstitial spheres
        tfermi=500.0,
        depth=1.0,
        imagz=0.02,
        efgs=0.2,
        nx=9,
        ncpu=4,
    )

    fec.emto.kgrn.write_input_file(folder=folder)
    fec.emto.kfcd.write_input_file(folder=folder)
    fec.emto.batch.write_input_file(folder=folder)

    print(f"  Generated SWS = {sws_val:.4f} a.u.")

print(f"\nAll input files written to: {folder}")
print(f"Run BMDL, KSTR, SHAPE first (structure files), then KGRN + KFCD for each SWS.")
