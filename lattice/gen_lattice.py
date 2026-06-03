#!/usr/bin/env python3
"""Generate shared BMDL/KSTR/SHAPE input files for BCC and FCC lattices."""

import os
import pyemto

for lat in ['bcc', 'fcc']:
    folder = os.path.abspath(f"./{lat}")
    os.makedirs(folder, exist_ok=True)

    sys = pyemto.System(folder=folder)
    sys.lattice.set_values(
        jobname_lat=lat,
        latpath='.',
        lat=lat,
    )
    sys.lattice.write_structure_input_files(folder=folder, jobname_lat=lat)
    print(f"Generated {lat} structure files in: {folder}")
