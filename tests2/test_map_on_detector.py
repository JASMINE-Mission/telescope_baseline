import csv

import pytest
from astropy.wcs import WCS

from telescope_baseline.tools.pipeline_v2.map_on_detector import MapOnDetector
from telescope_baseline.tools.pipeline_v2.position2d import Position2D
from telescope_baseline.tools.pipeline_v2.position_on_detector import PositionOnDetector
from tests2.test_pipeline import get_fits_file_name


def test_save():
    m = MapOnDetector(WCS(naxis=2), [
        PositionOnDetector(1, Position2D(0.0, 0.0), '2000-01-01 00:00:00', 12.5),
    ])
    f_name = get_fits_file_name('a.csv')
    m.save(f_name)
    file = open(f_name, 'r', newline='')
    f = csv.reader(file, delimiter=',')
    for p in f:
        pass
    assert int(p[0]) == 1
    assert float(p[1]) == 0.0
    assert float(p[2]) == 0.0
    assert float(p[3]) == 12.5
    assert p[4] == '2000-01-01 00:00:00'


def test_load():
    f_name = str(get_fits_file_name('a.csv'))
    m = MapOnDetector.load(f_name)[0]
    assert m.x == 0.0
    assert m.y == 0.0
    assert m.mag == 12.5
    assert m.exposure_id == 1
    assert m.datetime == '2000-01-01 00:00:00'
