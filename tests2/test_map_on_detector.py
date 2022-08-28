import csv

import pytest
from astropy.time import Time
from astropy.wcs import WCS

from telescope_baseline.tools.pipeline_v2.map_on_detector import MapOnDetector
from telescope_baseline.tools.pipeline_v2.position2d import Position2D
from telescope_baseline.tools.pipeline_v2.position_on_detector import PositionOnDetector
from tests2.test_pipeline import get_tests_file_name


@pytest.fixture
def mod():
    w = WCS(naxis=2)
    w.wcs.crpix = [256, 256]  # Reference point in pixel
    w.wcs.cd = [[1.31e-4, 0], [0, 1.31e-4]]  # cd matrix
    w.wcs.crval = [0, 0]  #
    w.wcs.ctype = ["GLON-TAN", "GLAT-TAN"]
    m = MapOnDetector(w, [
        PositionOnDetector(1, Position2D(0.0, 0.0), Time('2000-01-01 00:00:00'), 12.5),
    ])
    return m


def test_save(mod):
    f_name = get_tests_file_name('a.csv', folder="tmp")
    mod.save(f_name)
    file = open(f_name, 'r', newline='')
    f = csv.reader(file, delimiter=',')
    p = next(iter(f))
    assert int(p[0]) == 1
    assert float(p[1]) == 0.0
    assert float(p[2]) == 0.0
    assert float(p[3]) == 12.5
    assert p[4] == '2000-01-01 00:00:00.000'


def test_load():
    f_name = str(get_tests_file_name('detector.csv'))
    m = MapOnDetector.load(f_name)[0]
    assert m.x == 0.0
    assert m.y == 0.0
    assert m.mag == 12.5
    assert m.exposure_id == 1
    assert m.datetime == '2000-01-01 00:00:00'


def test_get_sky_positions(mod):
    p = mod.get_sky_positions()
    assert len(p) == 1
    assert str(p[0].datetime) == '2000-01-01 00:00:00.000'
    assert abs(p[0].mag - 12.5) < 0.1
    assert p[0].stellar_id == 1
    assert abs(p[0].coord.galactic.b.deg + 0.0334) < 0.0001
    assert abs(p[0].coord.galactic.l.deg - 359.9666) < 0.0001


def test_positions_on_detector(mod):
    assert len(mod.positions_on_detector) == 1
