from astropy.coordinates import SkyCoord
from astropy.time import Time
import astropy.units as u
from astropy.wcs import WCS
from telescope_baseline.tools.pipeline.stellarimage import OnDetectorPosition, StellarImage
from telescope_baseline.tools.pipeline.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.catalogue_entry import CatalogueEntry
from telescope_baseline.tools.pipeline.ontheskypositions import OnTheSkyPositions


def test_set_on_the_sky_list():
    t = [Time('2000-01-01 00:00:00.0'), Time('2000-04-01 00:00:00.0'), Time('2000-07-01 00:00:00.0'),
         Time('2000-10-01 00:00:00.0'), Time('2001-01-01 00:00:00.0')]
    c1 = SkyCoord(l=0, b=0, unit=('deg', 'deg'), frame="galactic", distance=1 * u.pc, obstime=t[0],
                  pm_l_cosb=1000 * u.mas / u.yr, pm_b=500 * u.mas / u.yr)
    a = AstrometricCatalogue()
    a.add_entry(CatalogueEntry(1, c1, 12.5))
    o = []
    for i in range(len(t)):
        o.append(OnTheSkyPositions(t[i]))
    for i in range(len(o)):
        a.add_child(o[i])
    for i in range(len(o)):
        o[i].get_parent_list()
        o[i].set_on_the_sky_list()
    assert(abs(c1.gcrs.ra.deg - o[0].get(0).ra) < 1e-12)
    assert(abs(c1.gcrs.dec.deg - o[0].get(0).dec) < 1e-12)
    assert(abs(o[1].get(0).ra - 266.4068695044846) < 1e-12)
    assert(abs(o[1].get(0).dec + 28.935614274628954) < 1e-12)
    assert(abs(o[2].get(0).ra - 266.41117766773704) < 1e-12)
    assert(abs(o[2].get(0).dec + 28.93630326427914) < 1e-12)
    assert(abs(o[4].get(0).ra - 266.3986717229359) < 1e-12)
    assert(abs(o[4].get(0).dec + 28.935572272912243) < 1e-12)


def test_map_to_the_sky():
    t = Time('2000-01-01 00:00:00.0')
    w = WCS(naxis=2)
    w.wcs.crpix = [50, 50]  # Reference point in pixel
    w.wcs.cd = [[1.31e-4, 0], [0, 1.31e-4]]  # cd matrix
    w.wcs.crval = [0, 0]  #
    w.wcs.ctype = ["GLON-TAN", "GLAT-TAN"]
    a = [OnDetectorPosition(1, 49, 50, 3000.), OnDetectorPosition(2, 50, 49, 2500.)]

    o = OnTheSkyPositions(t)
    s = StellarImage(w)
    s.add_position(a)
    o.add_child(s)
    o.map_to_the_sky()
    a = o.get_list()
    assert (abs(a[0].coord.galactic.l.deg) < 1e-10)
    assert (abs(a[0].coord.galactic.b.deg - 1.31e-4) < 1e-8)
    assert (abs(a[1].coord.galactic.l.deg - 1.31e-4) < 1e-8)
    assert (abs(a[1].coord.galactic.b.deg) < 1e-10)
