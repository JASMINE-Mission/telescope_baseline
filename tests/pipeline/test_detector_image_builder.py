import numpy as np
import pytest
from astropy.time import Time
from telescope_baseline.tools.pipeline.position2d import Position2D
from telescope_baseline.tools.pipeline.detector_image_builder import DetectorImageBuilder
from telescope_baseline.tools.pipeline.map_on_detector_builder import MapOnDetectorBuilder
from telescope_baseline.tools.pipeline.position_on_detector import PositionOnDetector
from telescope_baseline.tools.pipeline.map_on_detector import MapOnDetector


@pytest.fixture
def detector_image():
    o = PositionOnDetector(1, Position2D(64., 64.), Time('2000-01-01 00:00:00'), 3000)
    s = MapOnDetector([o])
    dib = DetectorImageBuilder(128, 128, 1.0)
    return dib.from_map_on_detector(s)


def test_from_stellar_image1(detector_image):
    assert detector_image.time == '2000-01-01 00:00:00'
    assert detector_image.hdu.data.shape[0] == 128
    assert detector_image.hdu.data.shape[1] == 128


def test_from_stellar_image2(detector_image):
    builder = MapOnDetectorBuilder(9, 256, 256)
    aa = builder.get_positions_on_detector(detector_image, 9)
    assert 63.5 < aa[0].x < 64.5
    assert 63.5 < aa[0].y < 64.5


def test_generate_stellar_image(monkeypatch):
    monkeypatch.setattr(np.random, 'randn', lambda: 0)
    dib = DetectorImageBuilder(128, 128, 1.0)
    a = np.zeros((128, 128))
    si = PositionOnDetector(1, Position2D(50.0, 50.0), Time('2000-01-01 00:00:00'), 10)
    dib._generate_a_stellar_image(a, si)
    assert a[50][50] == 10.0
    assert a[50][51] == 0
    assert a[49][50] == 0
