import pytest
from astropy.time import Time

from telescope_baseline.tools.pipeline_v2.position2d import Position2D
from telescope_baseline.tools.pipeline_v2.position_on_detector import PositionOnDetector


def test_pos():
    p = PositionOnDetector(1, Position2D(1.0, 2.0), Time('2000-01-01 00:00:00'), 12.5)
    assert p.exposure_id == 1
    assert str(p.datetime) == '2000-01-01 00:00:00.000'
    assert abs(p.x - 1.0) < 1e-6
    assert abs(p.y - 2.0) < 1e-6
    assert abs(p.mag - 12.5) < 0.1
