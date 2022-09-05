import pytest
from astropy.coordinates import SkyCoord
from astropy.time import Time
import astropy.units as u
from astropy.wcs import WCS

from telescope_baseline.tools.pipeline_v2.astrometric_catalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline_v2.catalog_entry import CatalogueEntry
from telescope_baseline.tools.pipeline_v2.position_on_detector import PositionOnDetector
from telescope_baseline.tools.pipeline_v2.map_on_the_sky_builder import MapOnTheSkyBuilder, \
    position_at_certain_time
from telescope_baseline.tools.pipeline_v2.position2d import Position2D
from telescope_baseline.tools.pipeline_v2.map_on_detector import MapOnDetector


@pytest.fixture
def sky_coordinate():
    return SkyCoord(l=0, b=0, unit=('deg', 'deg'), frame="galactic", distance=1 * u.pc,
                    obstime=Time('2000-01-01 00:00:00'), pm_l_cosb=1000 * u.mas / u.yr, pm_b=500 * u.mas / u.yr)


def test_position_at_certain_time(sky_coordinate):
    t = Time('2000-06-01 00:00:00')
    lon, lat = position_at_certain_time(sky_coordinate, t)
    assert 4.647 < lon < 4.667
    assert -0.101 < lat < -0.091


def test_from_astrometric_catalogue_2_list(sky_coordinate):
    w = WCS(naxis=2)
    builder = MapOnTheSkyBuilder(w)
    a = AstrometricCatalogue([CatalogueEntry(1, sky_coordinate, 3000)])
    t = [Time('2000-06-01 00:00:00')]
    o = builder.from_astrometric_catalogue_2_list(a, t)
    c0 = o[0].positions_on_the_sky[0].coord
    assert -4e-5 < c0.galactic.b.deg < 0
    assert 0.0001 < c0.galactic.l.deg < 0.00016


def test_from_stellar_image():
    w = WCS(naxis=2)
    w.wcs.crpix = [50, 50]  # Reference point in pixel
    w.wcs.cd = [[1.31e-4, 0], [0, 1.31e-4]]  # cd matrix
    w.wcs.crval = [0, 0]  #
    w.wcs.ctype = ["GLON-TAN", "GLAT-TAN"]
    builder = MapOnTheSkyBuilder(w)
    o = PositionOnDetector(1, Position2D(64., 64.), Time('2000-01-01 00:00:00'), 3000)
    s = MapOnDetector([o])
    o = builder.from_stellar_image([s])
    oc = o.positions_on_the_sky[0].coord.galactic
    assert o.positions_on_the_sky[0].datetime == '2000-01-01 00:00:00'
    assert 0.001 < oc.l.deg < 0.0025
    assert 0.001 < oc.b.deg < 0.0025
