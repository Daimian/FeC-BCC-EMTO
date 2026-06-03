#!/usr/bin/env python3
"""Fit EOS for pure BCC Fe using pyemto."""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pyemto
from pyemto.EOS.EOS import EOS

folder = os.path.abspath("./Fe_bcc")

fe = pyemto.System(folder=folder)
fe.bulk_new(
    lat='bcc',
    jobname='fe_bcc',
    latname='fe_bcc',
    latpath='.',
    ibz=3,
    atoms=np.array(['Fe']),
    iqs=np.array([1], dtype='int32'),
    its=np.array([1], dtype='int32'),
    itas=np.array([1], dtype='int32'),
    concs=np.array([100.0]),
    splts=np.array([2.0]),
    sws=2.687,
    xc='PBE',
)

sws_range = np.linspace(2.657, 2.717, 7)

# Read all energies
swses_all = []
energies_all = []
for s in sws_range:
    fe.sws = s
    job = fe.create_jobname('fe_bcc')
    en = fe.get_energy(job, folder=folder, func='PBE')
    if en is not None:
        swses_all.append(s)
        energies_all.append(en)

print("All data points:")
for s, e in zip(swses_all, energies_all):
    print(f"  SWS={s:.3f}  E={e:.6f}")

bohr2ang = 0.52917721092


def fit_and_plot(swses, energies, label, filename):
    eos = EOS(name='fe_bcc', xc='PBE', method='morse', units='bohr')
    eos.fit(swses, energies, show_plot=False, show_output=False)

    sws0 = eos.sws0
    B0 = eos.B0
    e0 = eos.e0
    R2 = eos.rsquared
    a0_bohr = sws0 * (8.0 * np.pi / 3.0) ** (1.0 / 3.0)
    a0_ang = a0_bohr * bohr2ang

    print(f"\n=== {label} ===")
    print(f"SWS_eq  = {sws0:.6f} Bohr")
    print(f"a_eq    = {a0_ang:.4f} Å  ({a0_bohr:.4f} Bohr)")
    print(f"B0      = {B0:.1f} GPa")
    print(f"E0      = {e0:.6f} Ry")
    print(f"R²      = {R2:.6f}")

    fig = plt.figure(figsize=(10, 7))
    plt.plot(swses, energies, 'bo', markersize=8, label='KFCD data')

    x_fit = np.linspace(min(swses) - 0.005, max(swses) + 0.005, 200)
    y_fit = eos.morse(x_fit, eos.eos_parameters[0], eos.eos_parameters[1],
                      eos.eos_parameters[2], eos.eos_parameters[3]) + eos.eMin
    plt.plot(x_fit, y_fit, 'r-', linewidth=2, label='Morse fit')
    plt.axvline(sws0, color='gray', linestyle='--', alpha=0.5, label=f'SWS$_0$ = {sws0:.4f}')

    plt.xlabel('SWS (Bohr)', fontsize=14)
    plt.ylabel('Energy (Ry)', fontsize=14)
    plt.title(f'{label}: a$_0$ = {a0_ang:.4f} Å, B$_0$ = {B0:.1f} GPa, R² = {R2:.4f}',
              fontsize=13)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    outpath = os.path.join(folder, filename)
    plt.savefig(outpath, dpi=150)
    plt.close()
    print(f"Plot saved to: {outpath}")


# --- Fit 1: All 7 points ---
fit_and_plot(swses_all, energies_all,
             "BCC Fe EOS (all 7 points)", "Fe_bcc_eos_all7.png")

# --- Fit 2: Without SWS=2.667 outlier ---
mask = [abs(s - 2.667) > 0.001 for s in swses_all]
swses_6 = [s for s, m in zip(swses_all, mask) if m]
energies_6 = [e for e, m in zip(energies_all, mask) if m]

fit_and_plot(swses_6, energies_6,
             "BCC Fe EOS (w/o 2.667)", "Fe_bcc_eos_no_outlier.png")
