import numpy as np
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.time import Time

from telescope_baseline.tools.pipeline.analysis import Analysis
from telescope_baseline.tools.pipeline.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
from telescope_baseline.tools.pipeline.ontheskypositions import OnTheSkyPositions, SkyPosition
from telescope_baseline.tools.pipeline.simulation import Simulation
from telescope_baseline.tools.pipeline.stellarimage import StellarImage, OnDetectorPosition


def test_step1():
    """

    Returns:
    TODO: Error(s) sometimes occurs because the value is generated from random number.
    """
    a = [OnDetectorPosition(1, 50., 50., 3000.)]
    for i in range(10):
        a.append(OnDetectorPosition(i + 1, 5 + 90 * np.random.rand(), 5 + 90 * np.random.rand(),
                                    int(2000 + 2000 * np.random.rand())))
    w = WCS(naxis=2)

    s1 = StellarImage(w)
    s1.add_position(a)
    d1 = DetectorImage("outputa.fits")
    s1.add_child(d1)
    vs = Simulation()
    s1.accept(vs)

    s2 = StellarImage(w)
    d2 = DetectorImage("outputa.fits")
    s2.add_child(d2)
    va = Analysis()
    s2.accept(va)

    a1 = s1.get_list()
    a2 = s2.get_list()

    n1 = []
    for s in a1:
        n1.append([s.x, s.y])
    n2 = []
    for s in a2:
        n2.append([s.x, s.y])
    np1 = np.sort(np.array(n1, dtype=np.float64), axis=0)
    np2 = np.sort(np.array(n2, dtype=np.float64), axis=0)
    for i in range(len(n1)):
        assert (abs(np1[i][0] - np2[i][0]) < 0.15)
        assert (abs(np1[i][1] - np2[i][1]) < 0.15)


def test_step2():
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
    v = Analysis()
    o.accept(v)
    a = o.get_list()
    assert (abs(a[0].coord.galactic.l.deg) < 1e-10)
    assert (abs(a[0].coord.galactic.b.deg - 1.31e-4) < 1e-8)
    assert (abs(a[1].coord.galactic.l.deg - 1.31e-4) < 1e-8)
    assert (abs(a[1].coord.galactic.b.deg) < 1e-10)


def test_step3():
    t = [Time('2000-01-01 00:00:00.0'), Time('2000-02-01 00:00:00.0'), Time('2000-03-01 00:00:00.0'),
         Time('2000-04-01 00:00:00.0'), Time('2000-05-01 00:00:00.0'), Time('2000-06-01 00:00:00.0'),
         Time('2000-07-01 00:00:00.0'), Time('2000-08-01 00:00:00.0'), Time('2000-09-01 00:00:00.0'),
         Time('2000-10-01 00:00:00.0'), Time('2000-11-01 00:00:00.0'), Time('2000-12-01 00:00:00.0'),
         Time('2001-01-01 00:00:00.0')]

    londata = [4.657229292609037, 4.657231613943884, 4.6572328740589235, 4.657232905752553, 4.657231693733922,
               4.657229540136522, 4.657227130343018, 4.657224922535985, 4.65722356203127, 4.6572234180551595,
               4.657224576568599, 4.657226710038408, 4.657229355524401]
    latdata = [-0.09662669750312813, -0.09662682006310001, -0.0966270232593704, -0.09662727212328368,
               -0.09662747861779832, -0.09662760274710183, -0.0966276096289789, -0.09662749965491312,
               -0.09662729760688273, -0.09662706177588641, -0.09662684008417984, -0.09662670773667688,
               -0.09662669894287566]
    a = AstrometricCatalogue()
    o = []
    for i in range(len(t)):
        o.append(OnTheSkyPositions(t[i]))
        o[i].add_entry(SkyPosition(1, SkyCoord(lon=londata[i], lat=latdata[i], unit=('rad', 'rad'),
                                               frame='barycentricmeanecliptic'), 12.5))
        a.add_child(o[i])
    v = Analysis()
    a.accept(v)

    result = a.get_parameters()

    assert(abs(result[0][0] - 4.657228194950601) < 1e-7)
    assert(abs(result[0][1] + 0.09662715320481664) < 1e-7)
    assert(abs(result[0][2]) < 1e-7)
    assert(abs(result[0][3]) < 1e-7)
    assert(abs(result[0][4] - 4.84813681109536e-06) < 1e-7)
