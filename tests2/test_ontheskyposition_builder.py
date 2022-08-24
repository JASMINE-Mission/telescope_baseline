import pytest
from astropy.coordinates import SkyCoord
from astropy.time import Time
import astropy.units as u
from astropy.wcs import WCS

from telescope_baseline.tools.pipeline_v2.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline_v2.catalogentry import CatalogueEntry
from telescope_baseline.tools.pipeline_v2.ondetectorposition import OnDetectorPosition
from telescope_baseline.tools.pipeline_v2.ontheskyposition_builder import OnTheSkyPositionBuilder, \
    position_at_certain_time
from telescope_baseline.tools.pipeline_v2.position2d import Position2D
from telescope_baseline.tools.pipeline_v2.stella_image import StellarImage


def test_position_at_certain_time():
    t = Time('2000-06-01 00:00:00')
    c = SkyCoord(l=0, b=0, unit=('deg', 'deg'), frame="galactic", distance=1 * u.pc,
                 obstime=Time('2000-01-01 00:00:00'), pm_l_cosb=1000 * u.mas / u.yr, pm_b=500 * u.mas / u.yr)
    lon, lat = position_at_certain_time(c, t)
    assert 4.647 < lon < 4.667
    assert -0.101 < lat < -0.091


def test_from_astrometric_catalogue_2_list():
    builder = OnTheSkyPositionBuilder()
    c = SkyCoord(l=0, b=0, unit=('deg', 'deg'), frame="galactic", distance=1 * u.pc,
                 obstime=Time('2000-01-01 00:00:00'), pm_l_cosb=1000 * u.mas / u.yr, pm_b=500 * u.mas / u.yr)
    a = AstrometricCatalogue([CatalogueEntry(1, c, 3000)])
    t = [Time('2000-06-01 00:00:00')]
    o = builder.from_astrometric_catalogue_2_list(a, t)
    c0 = o[0].sky_positions[0].coord
    assert -4e-5 < c0.galactic.b.deg < 0
    assert 0.0001 < c0.galactic.l.deg < 0.00016


def test_from_stellar_image():
    builder = OnTheSkyPositionBuilder()
    w = WCS(naxis=2)
    w.wcs.crpix = [50, 50]  # Reference point in pixel
    w.wcs.cd = [[1.31e-4, 0], [0, 1.31e-4]]  # cd matrix
    w.wcs.crval = [0, 0]  #
    w.wcs.ctype = ["GLON-TAN", "GLAT-TAN"]
    o = OnDetectorPosition(1, Position2D(64., 64.), '2000-01-01 00:00:00', 3000)
    s = StellarImage(w, [o])
    o = builder.from_stellar_image([s])
    oc = o.sky_positions[0].coord.galactic
    assert o.sky_positions[0].datetime == '2000-01-01 00:00:00'
    assert 0.001 < oc.l.deg < 0.0025
    assert 0.001 < oc.b.deg < 0.0025
