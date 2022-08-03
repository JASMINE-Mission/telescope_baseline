from astropy.coordinates import SkyCoord
import astropy.units as u
from telescope_baseline.tools.pipeline.catalogue_entry import CatalogueEntry


def test_catalogue_entry():
    s = SkyCoord(lon=1., lat=1., unit=('rad', 'rad'), frame='barycentricmeanecliptic', distance=1.0 * u.pc,
                 pm_lon_coslat=1000 * u.mas / u.yr, pm_lat=500 * u.mas / u.yr)
    c = CatalogueEntry(1, s, 12.5)
    assert(abs(c.ra - 15.76) < 0.01)
    assert(abs(c.dec - 72.34) < 0.01)
    assert(abs(c.parallax / u.mas - 1000) < 1)
    assert(abs(c.pm_dec * u.yr / u.mas - 1061) < 1)
    assert(abs(c.pm_ra * u.yr / u.mas - 351) < 1)

