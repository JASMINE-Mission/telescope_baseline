import csv

import pytest
from astropy.time import Time
from astropy.wcs import WCS

from telescope_baseline.tools.pipeline_v2.map_on_detector import MapOnDetector
from telescope_baseline.tools.pipeline_v2.map_on_the_sky_builder import MapOnTheSkyBuilder
from telescope_baseline.tools.pipeline_v2.position2d import Position2D
from telescope_baseline.tools.pipeline_v2.position_on_detector import PositionOnDetector
from tests2.test_pipeline import get_tests_file_name


@pytest.fixture
def mod():
    m = MapOnDetector([PositionOnDetector(1, Position2D(0.0, 0.0), Time('2000-01-01 00:00:00'), 12.5)])
    return m


@pytest.fixture
def csv_read(mod):
    f_name = get_tests_file_name('a.csv', folder="tmp")
    mod.save(f_name)
    file = open(f_name, 'r', newline='')
    f = csv.reader(file, delimiter=',')
    return next(iter(f))


def test_save(csv_read):
    assert int(csv_read[0]) == 1
    assert float(csv_read[1]) == 0.0
    assert float(csv_read[2]) == 0.0
    assert float(csv_read[3]) == 12.5
    assert csv_read[4] == '2000-01-01 00:00:00.000'


@pytest.fixture
def map_on_detector():
    f_name = str(get_tests_file_name('detector.csv'))
    return MapOnDetector.load(f_name)[0]


def test_load1(map_on_detector):
    assert map_on_detector.x == 0.0
    assert map_on_detector.y == 0.0


def test_load2(map_on_detector):
    assert map_on_detector.mag == 12.5
    assert map_on_detector.exposure_id == 1
    assert map_on_detector.datetime == '2000-01-01 00:00:00'


@pytest.fixture
def sky_positions(mod):
    w = WCS(naxis=2)
    w.wcs.crpix = [256, 256]  # Reference point in pixel
    w.wcs.cd = [[1.31e-4, 0], [0, 1.31e-4]]  # cd matrix
    w.wcs.crval = [0, 0]  #
    w.wcs.ctype = ["GLON-TAN", "GLAT-TAN"]
    builder = MapOnTheSkyBuilder(w)
    return builder.get_sky_positions(mod)


def test_get_sky_positions1(sky_positions):
    assert len(sky_positions) == 1
    assert str(sky_positions[0].datetime) == '2000-01-01 00:00:00.000'
    assert abs(sky_positions[0].mag - 12.5) < 0.1


def test_get_sky_positions2(sky_positions):
    assert sky_positions[0].stellar_id == 1
    assert abs(sky_positions[0].coord.galactic.b.deg + 0.0334) < 0.0001
    assert abs(sky_positions[0].coord.galactic.l.deg - 359.9666) < 0.0001


def test_positions_on_detector(mod):
    assert len(mod.positions_on_detector) == 1
