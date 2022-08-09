#!/usr/bin/env python3.8
"""Plot efficinecy

    usage:
        plot_eff.py [-h|--help] -i eff.json [-p plotfile.png]

    options:
        --help            show this help message and exit
        -i eff.json       Efficinecy data
        -p plotfile.png   Output file
"""
from docopt import docopt                         # command line interface
import matplotlib.pyplot as plt
from telescope_baseline.dataclass.efficiency import Efficiency

if __name__ == '__main__':
    args = docopt(__doc__)
    input_file = args['-i']
    if(args['-p']):
        plotfile = args['-p']
    else:
        plotfile = False

    efficiency = Efficiency.from_json(input_file)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(0.8, 1.7)
    ax.set_ylim(0.0, 1)
    ax.set_xlabel('Wavelength ($\\mu$m)')
    ax.set_ylabel('Efficiency')
    ax.set_title(efficiency.title)
    ax.text(0.85, 0.50, efficiency.comment, size=7)
    ax.plot(efficiency.wavelength, efficiency.efficiency,
            label=efficiency.title)
    ax.legend()
    plt.show()
    if(plotfile):
        fig.savefig(plotfile, transparent=True)
