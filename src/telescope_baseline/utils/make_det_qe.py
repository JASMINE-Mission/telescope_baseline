#!/usr/bin/env python3.8
"""Make detector QE.

usage:
    make_det_qe.py [-h|--help] -t temperature -j output.json

options:
    --help          show this help message and exit
    -t temperature  detector temperature, unit K
    -j output.json  output file name
"""
from docopt import docopt
import numpy as np
import json

# set default value
reference_doc      = 'JASMINE_HD_TN_HKZ_220515_01_qe.pdf'
output_file        = 'qe.json'
temperature_K      = 298
wavelength_base_nm = 45.63
alpha              = 4.4733e-4
wavelength_298K_um = np.array(
    [0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 1.00,
     1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.64, 1.70, 2.00])
quantum_efficiency = np.array(
    [0.00, 0.20, 0.35, 0.43, 0.48, 0.69, 0.83, 0.83,
     0.80, 0.81, 0.81, 0.78, 0.76, 0.73, 0.71, 0.00, 0.00])

# get values from the command line
if __name__ == '__main__':
    args = docopt(__doc__)
    temperature_K = float(args['-t'])
    output_file = args['-j']

"""
 wavelength(temperature, wavelengths_298K_um)
  = (wavelength_298K_um - wavelength_base_nm) * alpha * (temperature_K - 298 )
     + wavelength_298K_um

"""

wavelength = (wavelength_298K_um - wavelength_base_nm/1000) * \
    alpha * (temperature_K - 298) + wavelength_298K_um

title = 'Estimated QE at {:.1f} K,  polygonal line'.format(temperature_K)
comment = 'Reference {}'.format(reference_doc)
data = {'title': title, 'comment': comment,
        'wavelength': wavelength.tolist(),
        'efficiency': quantum_efficiency.tolist()}

with open(output_file, mode='w') as f:
    f.write(json.dumps(data, indent=4))
