import pytest
from astropy.coordinates import SkyCoord
from astropy.time import Time

from telescope_baseline.tools.pipeline_v2.position_on_the_sky import PositionOnTheSky


def test_pos():
    coord = SkyCoord(l=0., b=0., unit=('rad', 'rad'), frame='galactic')
    p = PositionOnTheSky(1, coord, 12.5, Time('2000-01-01 00:00:00'))
    assert abs(p.mag - 12.5) < 0.1
    assert p.stellar_id == 1
    assert str(p.datetime) == '2000-01-01 00:00:00.000'
    assert abs(p.coord.galactic.l.deg) < 0.1
    assert abs(p.coord.galactic.b.deg) < 0.1
