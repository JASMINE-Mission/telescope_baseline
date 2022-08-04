from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.wcs import WCS
from telescope_baseline.tools.pipeline.stellarimage import StellarImage, OnDetectorPosition
from telescope_baseline.tools.pipeline.ontheskypositions import OnTheSkyPositions, SkyPosition


def test_world_to_pixel():
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
    s.world_to_pixel()
    plist = s.get_list()
    assert len(plist), 3
    assert abs(plist[0].x - 255) < 2e-10
    assert abs(plist[0].y - 255) < 2e-10
    assert abs(plist[1].x - 255) < 2e-10
    assert abs(plist[1].y - 1018.35955373) < 1e-8
    assert abs(plist[2].x - 1018.35955373) < 1e-8
    assert abs(plist[2].y - 255) < 2e-10


def test_pixel_to_world():
    w = WCS(naxis=2)
    w.wcs.crpix = [256, 256]  # Reference point in pixel
    w.wcs.cd = [[1.31e-4, 0], [0, 1.31e-4]]  # cd matrix
    w.wcs.crval = [0, 0]  #
    w.wcs.ctype = ["GLON-TAN", "GLAT-TAN"]
    s = StellarImage(w)
    plist = [OnDetectorPosition(1, 256., 256., 12.5), OnDetectorPosition(2, 256., 200., 12.5)]
    s.add_position(plist)
    dlist = s.pixel_to_world()
    assert((dlist[0][1].galactic.l.deg - 0.000131) < 1.0e-8)
    assert((dlist[0][1].galactic.b.deg - 0.000131) < 1.0e-8)
    assert((dlist[1][1].galactic.l.deg - 0.000131) < 1.0e-8)
    assert((dlist[1][1].galactic.b.deg + 0.007205) < 1.0e-8)
