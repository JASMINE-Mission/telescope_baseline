import csv

import pytest
from astropy.coordinates import SkyCoord
from astropy.time import Time

from telescope_baseline.tools.pipeline_v2.map_on_the_sky import MapOnTheSky
from telescope_baseline.tools.pipeline_v2.position_on_the_sky import PositionOnTheSky
from tests2.test_pipeline import get_tests_file_name


@pytest.fixture
def mos():
    coord = SkyCoord(l=0, b=0, frame='galactic', unit=('rad', 'rad'))
    p = PositionOnTheSky(1, coord, 12.5, Time('2000-01-01 00:00:00'))
    m = MapOnTheSky(positions_on_the_sky=[p])
    return m


def test_save(mos):
    f_name = str(get_tests_file_name('a.csv', folder="tmp"))
    mos.save(f_name)
    file = open(f_name, 'r', newline='')
    f = csv.reader(file, delimiter=',')
    for r in f:
        if len(r) == 1:
            assert int(r[0]) == -1
        else:
            assert int(r[0]) == 1
            assert abs(float(r[1]) - 4.649644189337132) < 0.001
            assert abs(float(r[2]) + 0.5050315748856247) < 0.001
            assert abs(float(r[3]) - 12.5) < 0.1
            assert r[4] == '2000-01-01 00:00:00.000'


def test_load():
    f_name = str(get_tests_file_name('sky.csv'))
    m = MapOnTheSky.load(f_name)
    p = m.positions_on_the_sky[0]
    assert m.orbit_id == -1
    assert p.stellar_id == 1
    assert abs(p.coord.icrs.ra.rad - 4.649644189337132) < 0.01
    assert abs(p.coord.icrs.dec.rad + 0.5050315748856247) < 0.01
    assert abs(p.mag - 12.5) < 0.1
    assert str(p.datetime) == '2000-01-01 00:00:00.000'


def test_position_on_the_sky(mos):
    p = mos.positions_on_the_sky
    assert len(p) == 1


def test_orbit_id(mos):
    assert mos.orbit_id == -1
