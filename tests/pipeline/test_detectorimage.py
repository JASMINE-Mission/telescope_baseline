import pytest
from pytest_mock import MockFixture

import numpy as np
from astropy.wcs import WCS
from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
from telescope_baseline.tools.pipeline.simulation import Simulation
from telescope_baseline.tools.pipeline.stellarimage import StellarImage, OnDetectorPosition


def test_make_image_set_position(monkeypatch):
    monkeypatch.setattr(np.random, 'randn', lambda: 0)
    monkeypatch.setattr(np.random, 'uniform', lambda x, y, z: np.zeros(z))
    a = [OnDetectorPosition(1, 20., 30., 100.)]
    w = WCS(naxis=2)

    s1 = StellarImage(w)
    s1.add_position(a)
    d1 = DetectorImage("outputa.fits")
    s1.add_child(d1)
    vs = Simulation()
    s1.accept(vs)

    sut = d1.get_array()
    assert (sut[30][20] == 100)


@pytest.mark.parametrize('pos_array, actual_count', [
    ([OnDetectorPosition(1, 50., 50., 3000.)], 3000),
    ([OnDetectorPosition(1, 1000., 1000., 3000.)], 0),
    ([OnDetectorPosition(1, 50., 50., 4000.), OnDetectorPosition(1, 30., 30., 2000.), OnDetectorPosition(1, 1000., 1000., 3000.)], 6000),
    ([], 0),
    ([OnDetectorPosition(1, 50., 50., 0.)], 0),
])
def test_make_image_point_count(monkeypatch, pos_array, actual_count):
    monkeypatch.setattr(np.random, 'uniform', lambda x, y, z: np.zeros(z))
    w = WCS(naxis=2)
    s1 = StellarImage(w)
    s1.add_position(pos_array)
    d1 = DetectorImage("outputa.fits")
    s1.add_child(d1)
    vs = Simulation()
    s1.accept(vs)

    sut = d1.get_array()
    sut_count = 0
    for row in sut:
        for col in row:
            sut_count += col
    assert(sut_count == actual_count)


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
    sut = d1._incriment_position(pos)
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
