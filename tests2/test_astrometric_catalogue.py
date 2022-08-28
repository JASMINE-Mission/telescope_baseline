import csv

import pytest
from astropy.coordinates import SkyCoord
import astropy.units as u

from telescope_baseline.tools.pipeline_v2.astrometric_catalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline_v2.catalog_entry import CatalogueEntry
from tests2.test_pipeline import get_tests_file_name


def test_save():
    f_name = str(get_tests_file_name('a.csv', folder='tmp'))
    a = AstrometricCatalogue([
        CatalogueEntry(1,
                       SkyCoord(l=0., b=0., unit=('rad', 'rad'), frame='galactic', obstime='2000-01-01 00:00:00.0',
                                distance=1.0 * u.pc, pm_l_cosb=10 * u.mas / u.yr, pm_b=10 * u.mas / u.yr),
                       12.5),
    ])
    a.save(f_name)
    file = open(f_name, 'r', newline='')
    f = csv.reader(file, delimiter=',')
    for r in f:
        pass
    assert int(r[0]) == 1
    assert abs(float(r[1]) - 266.4049882865447) < 0.01
    assert abs(float(r[2]) + 28.936177761791473) < 0.01
    assert abs(float(r[3]) + 3.325090692327255) < 0.01
    assert abs(float(r[4]) - 13.745681936077188) < 0.01
    assert abs(float(r[5]) - 1.0) < 0.1
    assert r[6] == '2000-01-01 00:00:00.000'
    assert abs(float(r[7]) - 12.5) < 0.1


def test_load():
    f_name = str(get_tests_file_name('a.csv'))
    a = AstrometricCatalogue.load(f_name)
    c = a.get_catalogue()
    assert c[0].stellar_id == 1
    assert abs(c[0].ra - 266.4049882865447) < 0.01
    assert abs(c[0].dec + 28.936177761791473) < 0.01
    assert abs(c[0].pm_ra + 3.325090692327255) < 0.01
    assert abs(c[0].pm_dec - 13.745681936077188) < 0.01
    assert abs(c[0].distance - 1.0) < 0.1
    assert str(c[0].coord.obstime) == '2000-01-01 00:00:00.000'
    assert abs(c[0].mag - 12.5) < 0.1
