import pytest
from astropy.coordinates import SkyCoord
from astropy.time import Time

from telescope_baseline.tools.pipeline_v2.position_on_the_sky import PositionOnTheSky


@pytest.fixture
def position_on_the_sky():
    coord = SkyCoord(l=0., b=0., unit=('rad', 'rad'), frame='galactic')
    return PositionOnTheSky(1, coord, 12.5, Time('2000-01-01 00:00:00'))


def test_pos1(position_on_the_sky):
    assert abs(position_on_the_sky.mag - 12.5) < 0.1
    assert position_on_the_sky.stellar_id == 1


def test_pos2(position_on_the_sky):
    assert str(position_on_the_sky.datetime) == '2000-01-01 00:00:00.000'
    assert abs(position_on_the_sky.coord.galactic.l.deg) < 0.1
    assert abs(position_on_the_sky.coord.galactic.b.deg) < 0.1
