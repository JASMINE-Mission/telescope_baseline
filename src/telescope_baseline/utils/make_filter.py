#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Filter transmission data.

usage:
    make_filter.py [-h|--help] -s wls -t tran -w width -j out.json

options:
    --help      show this help message and exit
    -s wls      Cut on wavelength, unit micron
    -t tran     Transmission at pass band
    -w width    Width of the transition wavelength, unit micron
    -j out.json Output json file name
"""
from docopt import docopt
import json

# set default value
cut_on_wavelength_um      = 0.90
transmission              = 0.997
transition_width_um       = 0.0167
reference_doc             = 'JASMINE_HO_TN_HKZ_220513_filter.pdf'
output_file               = 'filter{:03.0f}.json'.format(
                            cut_on_wavelength_um * 100)
short_limit_wavelength_um = 0.85
long_limit_wavelength_um  = 1.8

# get values from the command line
if __name__ == '__main__':
    args = docopt(__doc__)
    cut_on_wavelength_um = float(args['-s'])
    transmission         = float(args['-t'])
    transition_width_um  = float(args['-w'])
    cut_on_wavelength_um = float(args['-s'])
    output_file          = args['-j']

# Make transmission data
wavelength_array = [short_limit_wavelength_um,
                    cut_on_wavelength_um - transition_width_um / 2,
                    cut_on_wavelength_um + transition_width_um / 2,
                    long_limit_wavelength_um]
transmission_array = [0.0, 0.0, transmission, transmission]

# Make data for output
title = 'Cut-on {:.2f} Trans {:.3f} width {:.4f}  polygonal line'.format(
        cut_on_wavelength_um, transmission, transition_width_um)
comment = 'Reference {}'.format(reference_doc)
data = {'title': title, 'comment': comment,
        'wavelength': wavelength_array, 'efficiency': transmission_array}
with open(output_file, mode='w') as f:
    f.write(json.dumps(data, indent=4))
