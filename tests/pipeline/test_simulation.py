from astropy.coordinates import SkyCoord
from astropy.time import Time
import astropy.units as u
from astropy.wcs import WCS

from telescope_baseline.tools.pipeline.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.catalogue_entry import CatalogueEntry
from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
from telescope_baseline.tools.pipeline.ontheskypositions import OnTheSkyPositions, SkyPosition
from telescope_baseline.tools.pipeline.stellarimage import StellarImage, OnDetectorPosition
from telescope_baseline.tools.pipeline.simulation import Simulation


def test_step1():
    """

    Returns:

    TODO: A test which depends on random number sometimes fails even if the code is valid. Need to fix.

    """
    pos = [OnDetectorPosition(1, 50, 50, 3000)]
    w = WCS(naxis=2)

    s = StellarImage(w)
    s.add_position(pos)
    d = DetectorImage("outputs.fits")
    s.add_child(d)

    v = Simulation()
    s.accept(v)

    a = d.get_array()
    assert(a[50][50] > 410)
    assert(231 < a[51][50] < 341)
    assert(231 < a[50][51] < 341)
    assert(231 < a[49][50] < 341)
    assert(231 < a[50][49] < 341)


def test_step2():
    """

    Returns:
    TODO: Usage of w is inconsistent to other source. Resolve reason and fix.
    """
    t = Time('2000-01-01 00:00:00.0')
    o = OnTheSkyPositions(t)
    c1 = SkyCoord(l=0, b=0, unit=('deg', 'deg'), frame='galactic')
    c2 = SkyCoord(l=0, b=0.1, unit=('deg', 'deg'), frame='galactic')
    c3 = SkyCoord(l=0.1, b=0, unit=('deg', 'deg'), frame='galactic')
    c4 = SkyCoord(l=0.1, b=1, unit=('deg', 'deg'), frame='galactic')
    o.add_entry(SkyPosition(1, c1, 12.5))
    o.add_entry(SkyPosition(1, c2, 12.5))
    o.add_entry(SkyPosition(1, c3, 12.5))
    o.add_entry(SkyPosition(1, c4, 12.5))

    w = WCS(naxis=2)
    w.wcs.crpix = [256, 256]  # Reference point in pixel
    w.wcs.cd = [[1.31e-4, 0], [0, 1.31e-4]]  # cd matrix
    w.wcs.crval = [0, 0]  #
    w.wcs.ctype = ["GLON-TAN", "GLAT-TAN"]
    s = StellarImage(w)

    o.add_child(s)
    v = Simulation()
    o.accept(v)
    plist = s.get_list()
    assert(len(plist), 3)
    assert(abs(plist[0].x - 255) < 2e-10)
    assert(abs(plist[0].y - 255) < 2e-10)
    assert(abs(plist[1].x - 255) < 2e-10)
    assert(abs(plist[1].y - 1018.35955373) < 1e-8)
    assert(abs(plist[2].x - 1018.35955373) < 1e-8)
    assert(abs(plist[2].y - 255) < 2e-10)


def test_step3():
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
    v = Simulation()
    a.accept(v)
    assert(abs(c1.gcrs.ra.deg - o[0].get(0).ra) < 1e-12)
    assert(abs(c1.gcrs.dec.deg - o[0].get(0).dec) < 1e-12)
    assert(abs(o[1].get(0).ra - 266.4068695044846) < 1e-12)
    assert(abs(o[1].get(0).dec + 28.935614274628954) < 1e-12)
    assert(abs(o[2].get(0).ra - 266.41117766773704) < 1e-12)
    assert(abs(o[2].get(0).dec + 28.93630326427914) < 1e-12)
    assert(abs(o[4].get(0).ra - 266.3986717229359) < 1e-12)
    assert(abs(o[4].get(0).dec + 28.935572272912243) < 1e-12)
