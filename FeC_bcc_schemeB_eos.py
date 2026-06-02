#!/usr/bin/env python3
"""
Generate EMTO-CPA input files for BCC Fe + C (octahedral interstitial).

Scheme B: SC conventional cell (LAT=1), NQ=8 (2 metal + 6 octahedral sites).
FM (ferromagnetic), PBE, SWS scan for EOS fitting.
"""

import os
import numpy as np
import pyemto

# === Paths ===
folder = os.path.abspath("./FeC_bcc_B")
latpath = "."

# === Physical parameters ===
# alpha-Fe: a = 2.866 Å = 5.416 a.u.
# NQ=8 (2 metal + 6 octahedral), conventional cell volume = a^3
# SWS = [3 * a^3 / (4*pi*NQ)]^(1/3)
a_bohr = 2.866 * 1.8897259886  # 5.416 a.u.
sws_center = (3.0 * a_bohr**3 / (4.0 * np.pi * 8))**(1.0/3.0)
print(f"Estimated SWS (NQ=8): {sws_center:.4f} a.u.")

# === Wigner-Seitz sphere radii ===
# Literature: C interstitial S(ws) = 0.77 (23% smaller)
# Metal atoms use default S(ws) = 1.0.
s_ws_C  = 0.77
s_ws_Fe = 1.0
print(f"S(ws): Fe = {s_ws_Fe:.4f}, C/Va = {s_ws_C:.4f}")

# === Carbon concentration ===
# 2 at% C on each octahedral sublattice
conc_C = 2.0   # percent on each sublattice
conc_Va = 100.0 - conc_C

# === SC conventional cell basis (fractional coordinates) ===
# IQ=1: Fe (0, 0, 0)        corner
# IQ=2: Fe (1/2, 1/2, 1/2)  body center
# IQ=3: Oct (1/2, 0, 0)     edge midpoint x
# IQ=4: Oct (0, 1/2, 0)     edge midpoint y
# IQ=5: Oct (0, 0, 1/2)     edge midpoint z
# IQ=6: Oct (0, 1/2, 1/2)   face center yz
# IQ=7: Oct (1/2, 0, 1/2)   face center xz
# IQ=8: Oct (1/2, 1/2, 0)   face center xy
basis = np.array([
    [0.0, 0.0, 0.0],
    [0.5, 0.5, 0.5],
    [0.5, 0.0, 0.0],
    [0.0, 0.5, 0.0],
    [0.0, 0.0, 0.5],
    [0.0, 0.5, 0.5],
    [0.5, 0.0, 0.5],
    [0.5, 0.5, 0.0],
])

# === KGRN atom block ===
# IQ=1,2: Fe (metal sites, IT=1)
# IQ=3-8: Va+C (octahedral, IT=2)
atoms = np.array([
    'Fe', 'Fe',
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
    2.0, 2.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
])
s_wss = np.array([
    s_ws_Fe, s_ws_Fe,
    s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C,
    s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C,
])
ws_wsts = np.array([
    s_ws_Fe, s_ws_Fe,
    s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C,
    s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C, s_ws_C,
])

# === SWS scan range ===
n_sws = 7
sws_range = np.linspace(sws_center - 0.06, sws_center + 0.06, n_sws)
print(f"SWS scan: {sws_range}")

# === Create System ===
fec = pyemto.System(folder=folder)

# Set lattice structure (BMDL/KSTR/SHAPE)
fec.lattice.set_values(
    jobname_lat='fec_bcc_B',
    latpath=latpath,
    lat='sc',
    basis=basis,
)
fec.lattice.write_structure_input_files(folder=folder, jobname_lat='fec_bcc_B')

# Set KGRN/KFCD parameters and generate SWS scan
for i, sws_val in enumerate(sws_range):
    fec.bulk_new(
        lat='sc',
        jobname='fec_bcc_B',
        latname='fec_bcc_B',
        latpath=latpath,
        ibz=1,             # IBZ=1 for SC
        atoms=atoms,
        iqs=iqs,
        its=its,
        itas=itas,
        concs=concs,
        splts=splts,
        sws=sws_val,
        s_wss=s_wss,
        ws_wsts=ws_wsts,
        afm='F',           # Ferromagnetic
        xc='PBE',
        expan='S',         # Single-Taylor expansion
        sofc='Y',          # Soft-core
        niter=100,
        ncpa=30,
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
        lmaxt=4,
        tfermi=500.0,
        depth=1.0,
        imagz=0.02,
        efgs=0.2,
        hx=0.2,
        nx=11,
        nz0=9,
        ncpu=8,
    )

    fec.emto.kgrn.write_input_file(folder=folder)
    fec.emto.kfcd.write_input_file(folder=folder)
    fec.emto.batch.write_input_file(folder=folder)

    print(f"  Generated SWS = {sws_val:.4f} a.u.")

print(f"\nAll input files written to: {folder}")
print(f"Run BMDL, KSTR, SHAPE first (structure files), then KGRN + KFCD for each SWS.")
