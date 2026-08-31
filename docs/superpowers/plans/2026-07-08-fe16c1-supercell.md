# Fe₁₆C₁ Supercell EMTO Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate EMTO input files for Fe₁₆C₁ BCC supercell calculations — S(ws)_C sphere-radius scan (Step 1) and EOS at c/a=1 (Step 2).

**Architecture:** Three self-contained Python scripts following existing repo patterns (`Fe_bcc_eos.py`, `FeC_bcc_eos.py`). A shared lattice generator adds the 17-atom SC basis to `lattice/bcc_sc17/`. Each calculation script creates symlinks to the lattice output, then loops over parameter values generating KGRN/KFCD/batch files via pyemto. No shared library code — each script is independently runnable.

**Tech Stack:** Python 3, numpy, pyemto (KSTR/BMDL/SHAPE/KGRN/KFCD generation)

## Global Constraints

- All input files generated via `pyemto.System` / `sys.lattice.set_values()` / `sys.bulk_new()` — never hand-written
- `lat='sc'`, `ibz=1` for the 17-atom simple-cubic supercell
- Volume conservation: `16 * S(ws)_Fe**3 + S(ws)_C**3 = 17`
- No CPA: every site is 100% single element, no Va mixing
- FM: `afm='F'`, `mmom=2.2`, `splts=[2.0]*16 + [0.0]`
- Al-Zoubi parameters: `depth=0.6`, `lmaxh=8`, `lmaxt=4`, `sofc='Y'`, `expan='S'`
- k-mesh: `nkx=nky=nkz=9` (can increase to 13 if convergence is poor)
- Existing `run_eos.sh` pattern used for batch execution

---

## File Structure

| File | Responsibility |
|------|---------------|
| `lattice/gen_lattice.py` (modify) | Add 17-atom `bcc_sc17` lattice generation |
| `FeC_bcc_sc_eta.py` (create) | Step 1: S(ws)_C scan at fixed w=2.65, c/a=1.0 |
| `FeC_bcc_sc_eos.py` (create) | Step 2: EOS (SWS scan) at fixed S(ws)_C, c/a=1.0 |

Output directories created by scripts:
- `lattice/bcc_sc17/` — KSTR/BMDL/SHAPE for 17-atom basis
- `FeC_bcc_sc/` — KGRN/KFCD outputs, symlinks to lattice, `run_eos.sh`

---

### Task 1: Add 17-atom lattice to lattice generator

**Files:**
- Modify: `lattice/gen_lattice.py:47-48` (append new section after existing `fcc_oct` block)

**Interfaces:**
- Consumes: nothing (standalone lattice generator)
- Produces: `lattice/bcc_sc17/{bmdl,kstr,shape}/` directories with structure files for the 17-atom SC basis. Task 2 and Task 3 symlink to these.

- [ ] **Step 1: Add the bcc_sc17 lattice block to gen_lattice.py**

Append this block after the existing `fcc_oct` section (after line 68):

```python
# === BCC 2x2x2 supercell: Fe16C1 (SC conventional cell, NQ=17) ===
folder = os.path.abspath("./bcc_sc17")
os.makedirs(folder, exist_ok=True)

basis_sc17 = np.array([
    # 8 Fe — corner sublattice
    [0.00, 0.00, 0.00], [0.50, 0.00, 0.00],
    [0.00, 0.50, 0.00], [0.00, 0.00, 0.50],
    [0.50, 0.50, 0.00], [0.50, 0.00, 0.50],
    [0.00, 0.50, 0.50], [0.50, 0.50, 0.50],
    # 8 Fe — body-center sublattice
    [0.25, 0.25, 0.25], [0.75, 0.25, 0.25],
    [0.25, 0.75, 0.25], [0.25, 0.25, 0.75],
    [0.75, 0.75, 0.25], [0.75, 0.25, 0.75],
    [0.25, 0.75, 0.75], [0.75, 0.75, 0.75],
    # 1 C — z-type octahedral interstitial (Zener ordered)
    [0.00, 0.00, 0.25],
])

sys = pyemto.System(folder=folder)
sys.lattice.set_values(
    jobname_lat='fe16c1',
    latpath='.',
    lat='sc',
    basis=basis_sc17,
    kappaw=[0.0, -0.2],
)
sys.lattice.write_structure_input_files(folder=folder, jobname_lat='fe16c1')
print(f"Generated bcc_sc17 (Fe16C1) structure files in: {folder}")
```

- [ ] **Step 2: Run the lattice generator to verify**

```bash
cd /home/dm/workplace/FeC-BCC-EMTO/lattice
python gen_lattice.py
```

Expected output includes:
```
Generated bcc_sc17 (Fe16C1) structure files in: /home/dm/workplace/FeC-BCC-EMTO/lattice/bcc_sc17
```

Verify the output directories exist:

```bash
ls lattice/bcc_sc17/bmdl/ lattice/bcc_sc17/kstr/ lattice/bcc_sc17/shape/
```

Expected: each directory contains files (`fe16c1.mdl`, `fe16c1.tfh`, `fe16c1M.tfh`, etc.)

- [ ] **Step 3: Commit**

```bash
git add lattice/gen_lattice.py
git commit -m "lattice: add bcc_sc17 (Fe16C1 17-atom supercell) basis"
```

---

### Task 2: Create S(ws)_C scan script (Step 1)

**Files:**
- Create: `FeC_bcc_sc_eta.py`

**Interfaces:**
- Consumes: `lattice/bcc_sc17/{bmdl,kstr,shape}/` (from Task 1)
- Produces: `FeC_bcc_sc/fe16c1_swsc0.{40,45,50,55,60}.{kgrn,kfcd,sh}` — 5 EMTO jobs at fixed w=2.65, varying S(ws)_C. Also `FeC_bcc_sc/run_eos.sh` for batch execution.

- [ ] **Step 1: Create FeC_bcc_sc_eta.py**

```python
#!/usr/bin/env python3
"""
Fe16C1 supercell: S(ws)_C scan at fixed w=2.65 Bohr, c/a=1.0.
Scan S(ws)_C = 0.40–0.60 to find optimal carbon sphere radius.

17 atoms: 16 Fe (BCC 2x2x2) + 1 C (z-type octahedral interstitial).
No CPA — each site is 100% single element.
"""

import os
import numpy as np
import pyemto

# === Paths ===
folder = os.path.abspath("./FeC_bcc_sc")
latpath = "../lattice/bcc_sc17"

# === Fixed parameters ===
sws_fixed = 2.65  # Bohr, near Al-Zoubi equilibrium w_eq=2.646

# === S(ws)_C scan ===
s_ws_C_values = [0.40, 0.45, 0.50, 0.55, 0.60]

# === 17-atom basis (fractional coords in SC supercell) ===
basis = np.array([
    # 8 Fe — corner sublattice
    [0.00, 0.00, 0.00], [0.50, 0.00, 0.00],
    [0.00, 0.50, 0.00], [0.00, 0.00, 0.50],
    [0.50, 0.50, 0.00], [0.50, 0.00, 0.50],
    [0.00, 0.50, 0.50], [0.50, 0.50, 0.50],
    # 8 Fe — body-center sublattice
    [0.25, 0.25, 0.25], [0.75, 0.25, 0.25],
    [0.25, 0.75, 0.25], [0.25, 0.25, 0.75],
    [0.75, 0.75, 0.25], [0.75, 0.25, 0.75],
    [0.25, 0.75, 0.75], [0.75, 0.75, 0.75],
    # 1 C — z-type octahedral interstitial
    [0.00, 0.00, 0.25],
])

# === KGRN atom arrays (NQ=17, NT=2) ===
atoms = np.array(['Fe'] * 16 + ['C'])
iqs   = np.arange(1, 18, dtype='int32')
its   = np.array([1] * 16 + [2], dtype='int32')
itas  = np.array([1] * 17, dtype='int32')
concs = np.array([100.0] * 17)
splts = np.array([2.0] * 16 + [0.0])

# === Create output directory and symlinks ===
os.makedirs(folder, exist_ok=True)
for d in ['bmdl', 'kstr', 'shape']:
    link = os.path.join(folder, d)
    target = os.path.join('..', 'lattice', 'bcc_sc17', d)
    if os.path.islink(link):
        os.unlink(link)
    elif os.path.isdir(link):
        import shutil
        shutil.rmtree(link)
    os.symlink(target, link)

# === Generate KGRN/KFCD for each S(ws)_C ===
sys = pyemto.System(folder=folder)

for s_ws_C in s_ws_C_values:
    # Volume conservation: 16*S(ws)_Fe^3 + S(ws)_C^3 = 17
    s_ws_Fe = ((17.0 - s_ws_C**3) / 16.0) ** (1.0 / 3.0)

    s_wss   = np.array([s_ws_Fe] * 16 + [s_ws_C])
    ws_wsts = np.array([s_ws_Fe] * 16 + [s_ws_C])

    jobname = f'fe16c1_swsc{s_ws_C:.2f}'

    print(f"S(ws)_C = {s_ws_C:.2f}, S(ws)_Fe = {s_ws_Fe:.6f}")

    sys.bulk_new(
        lat='sc',
        jobname=jobname,
        latname='fe16c1',
        latpath=latpath,
        ibz=1,
        basis=basis,
        atoms=atoms,
        iqs=iqs,
        its=its,
        itas=itas,
        concs=concs,
        splts=splts,
        sws=sws_fixed,
        s_wss=s_wss,
        ws_wsts=ws_wsts,
        afm='F',
        xc='PBE',
        expan='S',
        sofc='Y',
        niter=500,
        amix=0.02,
        efmix=1.0,
        tole=1.0e-7,
        tolef=1.0e-7,
        mmom=2.2,
        nkx=9,
        nky=9,
        nkz=9,
        lmaxh=8,
        lmaxt=4,
        depth=0.6,
        imagz=0.02,
        tfermi=500.0,
        ncpu=4,
    )

    sys.emto.kgrn.write_input_file(folder=folder)
    sys.emto.kfcd.write_input_file(folder=folder)
    sys.emto.batch.write_input_file(folder=folder)

    print(f"  Generated {jobname}")

print(f"\nAll input files written to: {folder}")
print("Run lattice/gen_lattice.py first (if not already done), then run_eos.sh.")
```

- [ ] **Step 2: Run the script to generate input files**

```bash
cd /home/dm/workplace/FeC-BCC-EMTO
python FeC_bcc_sc_eta.py
```

Expected output:
```
S(ws)_C = 0.40, S(ws)_Fe = 1.019...
  Generated fe16c1_swsc0.40
S(ws)_C = 0.45, S(ws)_Fe = 1.019...
  Generated fe16c1_swsc0.45
...
All input files written to: .../FeC_bcc_sc
```

- [ ] **Step 3: Verify generated files**

```bash
ls FeC_bcc_sc/fe16c1_swsc*.kgrn
```

Expected: 5 files — `fe16c1_swsc0.40.kgrn` through `fe16c1_swsc0.60.kgrn`.

Check the KGRN atom block has 17 lines (no Va, no CPA):

```bash
grep -c '^Fe\|^C ' FeC_bcc_sc/fe16c1_swsc0.50.kgrn
```

Expected: `17` (16 Fe + 1 C lines).

Check key parameters in a generated `.kgrn`:

```bash
grep 'IBZ\.\.' FeC_bcc_sc/fe16c1_swsc0.50.kgrn
```

Expected: contains `IBZ..=  1` (not 3).

```bash
grep 'DEPTH' FeC_bcc_sc/fe16c1_swsc0.50.kgrn
```

Expected: contains `DEPTH..=  0.600`.

```bash
grep 'NCPA' FeC_bcc_sc/fe16c1_swsc0.50.kgrn
```

Expected: `NCPA.=  1` (no CPA iterations needed — single-element sites).

- [ ] **Step 4: Create run_eos.sh in FeC_bcc_sc/**

```bash
cat > FeC_bcc_sc/run_eos.sh << 'RUNEOF'
#!/bin/bash
#SBATCH --job-name=Fe16C1_eta
#SBATCH -N 1
#SBATCH -n 5
#SBATCH -c 4
#SBATCH --mem-per-cpu=3800
#SBATCH -A p0020465
#SBATCH -t 02:00:00

ml openmpi/4.1.8-6xzv intel-oneapi-compilers/2025.3.1-pbro intel-oneapi-mkl/2025.3.1-iqtm

export OMP_NUM_THREADS=1
export OMP_STACKSIZE=256M

for kgrn_in in fe16c1_swsc*.kgrn; do
    base=${kgrn_in%.kgrn}
    (
        kgrn_cpa < "${base}.kgrn" > "${base}_kgrn.output" 2>&1
        kfcd_cpa < "${base}.kfcd" > "${base}_kfcd.output" 2>&1
    ) &
done

wait
echo "All S(ws)_C scan points finished."
RUNEOF
chmod +x FeC_bcc_sc/run_eos.sh
```

Note: `-c 4` matches `ncpu=4` in the KGRN input. `-n 5` runs all 5 jobs in parallel. Walltime 2h is conservative for the first NQ=17 run — adjust after seeing single-point timing.

- [ ] **Step 5: Commit**

```bash
git add FeC_bcc_sc_eta.py FeC_bcc_sc/run_eos.sh
git commit -m "feat: add Fe16C1 supercell S(ws)_C scan script (Step 1)"
```

---

### Task 3: Create EOS script (Step 2)

**Files:**
- Create: `FeC_bcc_sc_eos.py`

**Interfaces:**
- Consumes: `lattice/bcc_sc17/{bmdl,kstr,shape}/` (from Task 1). The optimal S(ws)_C from Step 1 results — hardcoded as `s_ws_C = 0.50` initially, updated after Step 1 runs.
- Produces: `FeC_bcc_sc/fe16c1_{sws}.{kgrn,kfcd,sh}` — 7 EMTO jobs scanning SWS=2.60–2.70 at fixed S(ws)_C and c/a=1.0.

- [ ] **Step 1: Create FeC_bcc_sc_eos.py**

```python
#!/usr/bin/env python3
"""
Fe16C1 supercell: EOS at c/a=1.0, fixed S(ws)_C.
SWS scan: 2.60–2.70 Bohr, 7 points.
Update s_ws_C below after Step 1 (eta scan) completes.

17 atoms: 16 Fe (BCC 2x2x2) + 1 C (z-type octahedral interstitial).
No CPA — each site is 100% single element.
"""

import os
import numpy as np
import pyemto

# === Paths ===
folder = os.path.abspath("./FeC_bcc_sc")
latpath = "../lattice/bcc_sc17"

# === Optimal S(ws)_C from Step 1 (update after eta scan) ===
s_ws_C = 0.50

# === Volume conservation ===
s_ws_Fe = ((17.0 - s_ws_C**3) / 16.0) ** (1.0 / 3.0)
print(f"S(ws)_C = {s_ws_C:.4f}, S(ws)_Fe = {s_ws_Fe:.6f}")

# === SWS scan range ===
n_sws = 7
sws_range = np.linspace(2.60, 2.70, n_sws)
print(f"SWS scan: {sws_range}")

# === 17-atom basis (fractional coords in SC supercell) ===
basis = np.array([
    # 8 Fe — corner sublattice
    [0.00, 0.00, 0.00], [0.50, 0.00, 0.00],
    [0.00, 0.50, 0.00], [0.00, 0.00, 0.50],
    [0.50, 0.50, 0.00], [0.50, 0.00, 0.50],
    [0.00, 0.50, 0.50], [0.50, 0.50, 0.50],
    # 8 Fe — body-center sublattice
    [0.25, 0.25, 0.25], [0.75, 0.25, 0.25],
    [0.25, 0.75, 0.25], [0.25, 0.25, 0.75],
    [0.75, 0.75, 0.25], [0.75, 0.25, 0.75],
    [0.25, 0.75, 0.75], [0.75, 0.75, 0.75],
    # 1 C — z-type octahedral interstitial
    [0.00, 0.00, 0.25],
])

# === KGRN atom arrays (NQ=17, NT=2) ===
atoms = np.array(['Fe'] * 16 + ['C'])
iqs   = np.arange(1, 18, dtype='int32')
its   = np.array([1] * 16 + [2], dtype='int32')
itas  = np.array([1] * 17, dtype='int32')
concs = np.array([100.0] * 17)
splts = np.array([2.0] * 16 + [0.0])
s_wss   = np.array([s_ws_Fe] * 16 + [s_ws_C])
ws_wsts = np.array([s_ws_Fe] * 16 + [s_ws_C])

# === Create output directory and symlinks ===
os.makedirs(folder, exist_ok=True)
for d in ['bmdl', 'kstr', 'shape']:
    link = os.path.join(folder, d)
    target = os.path.join('..', 'lattice', 'bcc_sc17', d)
    if os.path.islink(link):
        os.unlink(link)
    elif os.path.isdir(link):
        import shutil
        shutil.rmtree(link)
    os.symlink(target, link)

# === Generate KGRN/KFCD for each SWS ===
sys = pyemto.System(folder=folder)

for sws_val in sws_range:
    jobname = f'fe16c1_{sws_val:.6f}'

    sys.bulk_new(
        lat='sc',
        jobname=jobname,
        latname='fe16c1',
        latpath=latpath,
        ibz=1,
        basis=basis,
        atoms=atoms,
        iqs=iqs,
        its=its,
        itas=itas,
        concs=concs,
        splts=splts,
        sws=sws_val,
        s_wss=s_wss,
        ws_wsts=ws_wsts,
        afm='F',
        xc='PBE',
        expan='S',
        sofc='Y',
        niter=500,
        amix=0.02,
        efmix=1.0,
        tole=1.0e-7,
        tolef=1.0e-7,
        mmom=2.2,
        nkx=9,
        nky=9,
        nkz=9,
        lmaxh=8,
        lmaxt=4,
        depth=0.6,
        imagz=0.02,
        tfermi=500.0,
        ncpu=4,
    )

    sys.emto.kgrn.write_input_file(folder=folder)
    sys.emto.kfcd.write_input_file(folder=folder)
    sys.emto.batch.write_input_file(folder=folder)

    print(f"  Generated SWS = {sws_val:.6f} a.u.")

print(f"\nAll input files written to: {folder}")
print("Run lattice/gen_lattice.py first (if not already done), then run_eos.sh.")
```

- [ ] **Step 2: Run the script to generate input files**

```bash
cd /home/dm/workplace/FeC-BCC-EMTO
python FeC_bcc_sc_eos.py
```

Expected output:
```
S(ws)_C = 0.5000, S(ws)_Fe = 1.018...
SWS scan: [2.6  2.61666... 2.63333... 2.65 2.66666... 2.68333... 2.7]
  Generated SWS = 2.600000 a.u.
  ...
  Generated SWS = 2.700000 a.u.
All input files written to: .../FeC_bcc_sc
```

- [ ] **Step 3: Verify generated files**

```bash
ls FeC_bcc_sc/fe16c1_2.*.kgrn | wc -l
```

Expected: `7`.

Check the SWS value is correctly embedded:

```bash
grep 'SWS' FeC_bcc_sc/fe16c1_2.650000.kgrn
```

Expected: contains `SWS......= 2.6500000`.

Check S(ws) values in atom block:

```bash
grep '^Fe\|^C ' FeC_bcc_sc/fe16c1_2.650000.kgrn | head -3
```

Expected: Fe lines show S(ws)≈1.018, C line shows S(ws)=0.500.

- [ ] **Step 4: Update run_eos.sh for EOS jobs**

The existing `run_eos.sh` from Task 2 uses `fe16c1_swsc*.kgrn`. For the EOS run, either:
- (a) Run after removing/moving Step 1 outputs, OR
- (b) Create a separate `run_eos_sws.sh`

Create the separate script:

```bash
cat > FeC_bcc_sc/run_eos_sws.sh << 'RUNEOF'
#!/bin/bash
#SBATCH --job-name=Fe16C1_eos
#SBATCH -N 1
#SBATCH -n 7
#SBATCH -c 4
#SBATCH --mem-per-cpu=3800
#SBATCH -A p0020465
#SBATCH -t 04:00:00

ml openmpi/4.1.8-6xzv intel-oneapi-compilers/2025.3.1-pbro intel-oneapi-mkl/2025.3.1-iqtm

export OMP_NUM_THREADS=1
export OMP_STACKSIZE=256M

for kgrn_in in fe16c1_2.*.kgrn; do
    base=${kgrn_in%.kgrn}
    (
        kgrn_cpa < "${base}.kgrn" > "${base}_kgrn.output" 2>&1
        kfcd_cpa < "${base}.kfcd" > "${base}_kfcd.output" 2>&1
    ) &
done

wait
echo "All EOS points finished."
RUNEOF
chmod +x FeC_bcc_sc/run_eos_sws.sh
```

- [ ] **Step 5: Commit**

```bash
git add FeC_bcc_sc_eos.py FeC_bcc_sc/run_eos_sws.sh
git commit -m "feat: add Fe16C1 supercell EOS script (Step 2)"
```
