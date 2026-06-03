from pyemto.EOS.EOS import EOS
import matplotlib
matplotlib.use('Agg')
import os, re, sys

kfcd_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kfcd')
files = [file for file in os.listdir(kfcd_dir) if file.endswith('.prn')]
if len(files) == 0:
    sys.exit(0)

sws_values = []
e_values = []
for file_path in sorted(files):
    file_name = os.path.basename(file_path)
    element = re.findall('[A-Z][^A-Z]*', file_name.split('_')[0])
    lat = file_name.split('_')[1]
    sws = float(file_name.split('_')[-1].rsplit('.prn')[0]) ; sws_values.append(sws)
    with open(os.path.join(kfcd_dir, file_path), 'r') as f:
        for line in f:
            if 'TOT-PBE' in line:
                e = float(line.split()[3]) ; e_values.append(e)

lowest_index = e_values.index(min(e_values))
sws_test = sws_values[lowest_index]
print(f'sws_test = {sws_test}')
name = ''.join(element)+f'_{lat}'
eos = EOS(name=name)
sws0, e0, B0, grun, R_squared = eos.fit(sws_values, e_values, show_plot=False)

out_dir = os.path.dirname(os.path.abspath(__file__))
out_name = os.path.basename(os.path.dirname(out_dir)) + '_eos'
eos.plot(filename=out_name, show=False)

import matplotlib.pyplot as plt
plt.savefig(os.path.join(out_dir, f'{out_name}.png'), dpi=150)
print(f'Plot saved to: {out_dir}/{out_name}.png')
