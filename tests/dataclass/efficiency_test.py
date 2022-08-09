"""test for wl_eff

"""
from pytest import approx
import pkg_resources
from telescope_baseline.dataclass.efficiency import Efficiency
import numpy as np

def test_from_json():
    testdata = 'data/teleff.json'
    speclist = pkg_resources.resource_filename('telescope_baseline', testdata)
    efficiency = Efficiency.from_json(speclist)
    assert efficiency.efficiency_grid[3] == approx(0.84)
    assert efficiency.wavelength_grid[3] == approx(1.4)

def test_evaluate():
    testdata = 'data/teleff.json'
    speclist = pkg_resources.resource_filename('telescope_baseline', testdata)
    efficiency = Efficiency.from_json(speclist)
    wavref=np.linspace(0.8,1.6,1000)
    val=efficiency.evaluate(wavref)

    assert np.sum(val) == approx(809.045945945946)

def test_weighted_mean():
    testdata = 'data/teleff.json'
    speclist = pkg_resources.resource_filename('telescope_baseline', testdata)
    efficiency = Efficiency.from_json(speclist)
    wavref=np.linspace(0.8,1.6,1000)
    weight=np.exp(-(wavref-1.2)**2.0)
    val=efficiency.weighted_mean(wavref,weight)
    assert val==approx(0.8095121156784766)
    
