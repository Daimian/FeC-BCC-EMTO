#!/usr/bin/env python3
"""
Test: NbVa with S(ws)=1.0 for ALL sites (equal spheres).
If this shows proper EOS minimum, the S(ws)=0.77 is the problem.
"""
import os, numpy as np, pyemto

folder = os.path.abspath("./NbVa_bcc_eq")
latpath = "../lattice/bcc_oct"

a_bohr = 3.3008 * 1.8897259886
sws_center = (3.0 * a_bohr**3 / (4.0 * np.pi * 8))**(1.0/3.0)

atoms = np.array(['Nb', 'Nb', 'Va', 'Va', 'Va', 'Va', 'Va', 'Va'])
iqs = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype='int32')
its = np.array([1, 1, 2, 2, 2, 2, 2, 2], dtype='int32')
itas = np.array([1, 1, 1, 1, 1, 1, 1, 1], dtype='int32')
concs = np.array([100.0]*8)
splts = np.array([0.0]*8)
# ALL S(ws) = 1.0 (equal spheres)
s_wss = np.array([1.0]*8)
ws_wsts = np.array([1.0]*8)

n_sws = 7
sws_range = np.linspace(sws_center - 0.06, sws_center + 0.06, n_sws)
print(f"SWS scan: {sws_range}")

os.makedirs(folder, exist_ok=True)
for d in ['bmdl', 'kstr', 'shape']:
    link = os.path.join(folder, d)
    target = os.path.join('..', 'lattice', 'bcc_oct', d)
    if os.path.islink(link): os.unlink(link)
    elif os.path.isdir(link): __import__('shutil').rmtree(link)
    os.symlink(target, link)

nb = pyemto.System(folder=folder)
for sws_val in sws_range:
    nb.bulk_new(lat='sc', jobname='nbva_eq', latname='bcc_oct', latpath=latpath,
        ibz=1, atoms=atoms, iqs=iqs, its=its, itas=itas, concs=concs, splts=splts,
        sws=sws_val, s_wss=s_wss, ws_wsts=ws_wsts,
        afm='P', xc='PBE', expan='S', sofc='Y', niter=500, amix=0.02, efmix=1.0,
        tole=1e-7, tolef=1e-7, mmom=0.0, nky=11, nkx=11, nkz=11, ncpu=1,
        lmaxh=8, lmaxt=4, tfermi=500.0, depth=1.0, imagz=0.02, efgs=0.2, hx=0.2, nx=11, nz0=9)
    nb.emto.kgrn.write_input_file(folder=folder)
    nb.emto.kfcd.write_input_file(folder=folder)
    nb.emto.batch.write_input_file(folder=folder)
    print(f"  Generated SWS = {sws_val:.4f}")

print(f"\nAll input files written to: {folder}")
