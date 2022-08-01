import numpy as np
from astropy.wcs import WCS

from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
from telescope_baseline.tools.pipeline.simulation import Simulation
from telescope_baseline.tools.pipeline.stellarimage import StellarImage, OnDetectorPosition

# Test code that continues to maintain what you didn't break by refactoring.
def test_makeImage(monkeypatch) :
    monkeypatch.setattr(np.random, 'rand', lambda : 0.5)
    monkeypatch.setattr(np.random, 'randn', lambda : 0)
    monkeypatch.setattr(np.random, 'uniform', lambda x, y, z: np.zeros(z))
    a = [OnDetectorPosition(1, 50., 50., 3000.)]
    w = WCS(naxis=2)

    s1 = StellarImage(w)
    s1.add_position(a)
    d1 = DetectorImage("outputa.fits")
    s1.add_child(d1)
    vs = Simulation()
    s1.accept(vs)

    sut = d1.get_array()
    assert(len(sut) == 100)
    for x in range(0, 100):
        assert(len(sut[x]) == 100)
        for y in range(0, 100):
            if (50, 50) == (x, y):
                assert(sut[x][y] == 3000)
            else:
                assert(sut[x][y] == 0)