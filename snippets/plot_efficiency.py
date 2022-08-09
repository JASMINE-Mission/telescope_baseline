import pkg_resources
from telescope_baseline.dataclass.efficiency import Efficiency
import matplotlib.pyplot as plt
import numpy as np


def plot_efficiency_evaluate():
    testdata = 'data/teleff.json'
    speclist = pkg_resources.resource_filename('telescope_baseline', testdata)
    efficiency = Efficiency.from_json(speclist)
    wavref = np.linspace(0.8, 1.6, 1000)
    val = efficiency.evaluate(wavref)

    plt.plot(wavref, val)
    plt.xlabel('wavelength')
    plt.ylabel('efficiency')
    plt.savefig('efficiency_evaluate.png')
    plt.show()


if __name__ == '__main__':
    plot_efficiency_evaluate()
