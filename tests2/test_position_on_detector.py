import pytest
from astropy.time import Time

from telescope_baseline.tools.pipeline_v2.position2d import Position2D
from telescope_baseline.tools.pipeline_v2.position_on_detector import PositionOnDetector


@pytest.fixture
def position_on_detector():
    return PositionOnDetector(1, Position2D(1.0, 2.0), Time('2000-01-01 00:00:00'), 12.5)


def test_pos(position_on_detector):
    assert position_on_detector.exposure_id == 1
    assert str(position_on_detector.datetime) == '2000-01-01 00:00:00.000'


def test_pos2(position_on_detector):
    assert abs(position_on_detector.x - 1.0) < 1e-6
    assert abs(position_on_detector.y - 2.0) < 1e-6
    assert abs(position_on_detector.mag - 12.5) < 0.1
