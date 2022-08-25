import pytest
from astropy.wcs import WCS

from build.lib.telescope_baseline.tools.pipeline_v2.position2d import Position2D
from telescope_baseline.tools.pipeline_v2.detector_image_builder import DetectorImageBuilder
from telescope_baseline.tools.pipeline_v2.position_on_detector import PositionOnDetector
from telescope_baseline.tools.pipeline_v2.map_on_detector import MapOnDetector


def test_from_stellar_image():
    w = WCS(naxis=2)
    o = PositionOnDetector(1, Position2D(64., 64.), '2000-01-01 00:00:00', 3000)
    s = MapOnDetector(w, [o])
    dib = DetectorImageBuilder(128, 128, 1.0)
    di = dib.from_stellar_image(s)
    aa = di.get_on_detector_positions(9)
    assert di.time == '2000-01-01 00:00:00'
    assert di.hdu.data.shape[0] == 128
    assert di.hdu.data.shape[1] == 128
    assert 63.5 < aa[0].x < 64.5
    assert 63.5 < aa[0].y < 64.5

