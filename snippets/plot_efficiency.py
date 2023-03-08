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


def plot_total_throughput():
    spec_list = pkg_resources.resource_filename('telescope_baseline',
                                                'data/teleff.json')
    optics_efficiency = Efficiency.from_json(spec_list)
    # detector temperature
    spec_list = pkg_resources.resource_filename('telescope_baseline',
                                                'data/qe/qe180.json')
    quantum_efficiency = Efficiency.from_json(spec_list)
    # filter cut on wavelength ???
    __short_wavelength_limit = 1.0e-6
    f_name = "data/filter/filter" + str(int(
        __short_wavelength_limit * 1e8)).zfill(3) + ".json"
    spec_list = pkg_resources.resource_filename('telescope_baseline', f_name)
    filter_efficiency = Efficiency.from_json(spec_list)
    
    
    N = 100
    wav = np.linspace(0.95,1.75,N)

    eff = np.interp(wav,optics_efficiency.wavelength_grid,optics_efficiency.efficiency_grid)
    qe = np.interp(wav,quantum_efficiency.wavelength_grid,quantum_efficiency.efficiency_grid)
    filter = np.interp(wav,filter_efficiency.wavelength_grid,filter_efficiency.efficiency_grid)

    total_throughput = eff*qe*filter
    np.savetxt("total_throuput_2023March.txt", np.array([wav,total_throughput]).T ,delimiter=",")
    plt.plot(wav,total_throughput)
    plt.show()


if __name__ == '__main__':
    #plot_efficiency_evaluate()
    plot_total_throughput()