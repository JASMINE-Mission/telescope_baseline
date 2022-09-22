import csv
import pytest
from astropy.coordinates import SkyCoord
from astropy.time import Time
from telescope_baseline.tools.pipeline.map_on_the_sky import MapOnTheSky
from telescope_baseline.tools.pipeline.position_on_the_sky import PositionOnTheSky
from test_pipeline import get_tests_file_name
from test_tools.test_file_utils import get_temp_file


@pytest.fixture
def mos():
    coord = SkyCoord(l=0, b=0, frame='galactic', unit=('rad', 'rad'))
    p = PositionOnTheSky(1, coord, 12.5, Time('2000-01-01 00:00:00'))
    m = MapOnTheSky(positions_on_the_sky=[p])
    return m


def test_save(mos):
    tmp_file = get_temp_file()
    f_name = str(tmp_file)
    mos.save(f_name)
    file = open(f_name, 'r', newline='')
    csv_line = csv.reader(file, delimiter=',')
    for r in csv_line:
        if len(r) == 1:
            assert int(r[0]) == -1
        else:
            assert int(r[0]) == 1
            assert abs(float(r[1]) - 4.649644189337132) < 0.001
            assert abs(float(r[2]) + 0.5050315748856247) < 0.001
            assert abs(float(r[3]) - 12.5) < 0.1
            assert r[4] == '2000-01-01 00:00:00.000'


@pytest.fixture
def position_on_the_sky():
    f_name = str(get_tests_file_name('sky.csv'))
    m = MapOnTheSky.load(f_name)
    return m.positions_on_the_sky[0]


def test_load1():
    f_name = str(get_tests_file_name('sky.csv'))
    m = MapOnTheSky.load(f_name)
    assert m.orbit_id == -1


def test_load2(position_on_the_sky):
    assert position_on_the_sky.stellar_id == 1
    assert abs(position_on_the_sky.coord.icrs.ra.rad - 4.649644189337132) < 0.01


def test_load3(position_on_the_sky):
    assert abs(position_on_the_sky.coord.icrs.dec.rad + 0.5050315748856247) < 0.01
    assert abs(position_on_the_sky.mag - 12.5) < 0.1
    assert str(position_on_the_sky.datetime) == '2000-01-01 00:00:00.000'


def test_position_on_the_sky(mos):
    p = mos.positions_on_the_sky
    assert len(p) == 1


def test_orbit_id(mos):
    assert mos.orbit_id == -1
