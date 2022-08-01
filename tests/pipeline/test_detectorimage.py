import pytest
from pytest_mock import MockFixture

import numpy as np
from astropy.wcs import WCS
from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
from telescope_baseline.tools.pipeline.simulation import Simulation
from telescope_baseline.tools.pipeline.stellarimage import StellarImage, OnDetectorPosition


# Test code that continues to maintain what you didn't break by refactoring.
def test_makeImage(monkeypatch):
    monkeypatch.setattr(np.random, 'rand', lambda: 0.5)
    monkeypatch.setattr(np.random, 'randn', lambda: 0)
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
    assert (len(sut) == 100)
    for x in range(0, 100):
        assert (len(sut[x]) == 100)
        for y in range(0, 100):
            if (50, 50) == (x, y):
                assert (sut[x][y] == 3000)
            else:
                assert (sut[x][y] == 0)


@pytest.mark.parametrize('pos, randn, actual', [
    (OnDetectorPosition(1, 50., 50., 3000.), (0.0, 0.0), (50, 50)),
    (OnDetectorPosition(1, 30., 40., 3000.), (0.0, 0.0), (40, 30)),  # swap position
    (OnDetectorPosition(1, 50., 50., 3000.), (0.4, 0.0), (50, 50)),
    (OnDetectorPosition(1, 50., 50., 3000.), (0.5, 0.0), (51, 50)),
    (OnDetectorPosition(1, 50., 50., 3000.), (0.0, 0.4), (50, 50)),
    (OnDetectorPosition(1, 50., 50., 3000.), (0.0, 0.5), (50, 51)),
])
def test__incriment_position(mocker: MockFixture, pos, randn, actual):
    mocker.patch.object(np.random, 'randn').side_effect = randn
    d1 = DetectorImage("outputa.fits")
    sut = d1._incriment_position(pos);
    assert (sut == actual)

@pytest.mark.parametrize('pos, actual', [
    ((0, 0), True),
    ((-1, 0), False),
    ((0, -1), False),
    ((50, 50), True),
    ((99, 99), True),
    ((100, 99), False),
    ((99, 100), False),
])
def test__is_include_area(pos, actual):
    d1 = DetectorImage("outputa.fits")
    sut = d1._is_include_area(pos)
    assert(sut == actual)
