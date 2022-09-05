import pytest
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.time import Time
from astropy.wcs import WCS

from telescope_baseline.tools.pipeline_v2.detector_image import DetectorImage
from telescope_baseline.tools.pipeline_v2.detector_image_catalogue import DetectorImageCatalogue
from telescope_baseline.tools.pipeline_v2.map_on_detector import MapOnDetector
from telescope_baseline.tools.pipeline_v2.map_on_the_sky import MapOnTheSky
from telescope_baseline.tools.pipeline_v2.map_on_the_sky_builder import MapOnTheSkyBuilder
from telescope_baseline.tools.pipeline_v2.position2d import Position2D
from telescope_baseline.tools.pipeline_v2.position_on_detector import PositionOnDetector
from telescope_baseline.tools.pipeline_v2.position_on_the_sky import PositionOnTheSky
from telescope_baseline.tools.pipeline_v2.map_on_detector_builder import MapOnDetectorBuilder
from telescope_baseline.tools.pipeline_v2.wcswid import WCSwId

@pytest.fixture
def map_on_the_sky():
    s = PositionOnTheSky(1, SkyCoord(l=0, b=0, unit=('deg', 'deg'), frame='galactic'), 3000,
                         Time('2000-01-01 00:00:00'))
    return MapOnTheSky(positions_on_the_sky=[s])


def test_from_detector_image_catalogue():
    ft = fits.open("tmp.fits")
    d = DetectorImage(ft[0])
    c = DetectorImageCatalogue([d])
    w = WCS(naxis=2)
    w.wcs.crpix = [256, 256]  # Reference point in pixel
    w.wcs.cd = [[1.31e-4, 0], [0, 1.31e-4]]  # cd matrix
    w.wcs.crval = [0, 0]  #
    w.wcs.ctype = ["GLON-TAN", "GLAT-TAN"]
    mo = MapOnDetector(w, [PositionOnDetector(1, Position2D(64.0, 64.0), Time('2000-01-01 00:00:00'), 12.5)])
    builder = MapOnDetectorBuilder(9, 128, 128)
    si = builder.from_detector_image_catalogue(w, c)
    co = MapOnTheSkyBuilder.get_sky_positions(mo)[0].coord.galactic
    assert 359.97 < co.l.deg < 359.98
    assert -0.03 < co.b.deg < -0.02
    assert 63.5 < si[0].positions_on_detector[0].x < 64.5
    assert 63.5 < si[0].positions_on_detector[0].y < 64.5


def test_from_on_tye_sky_position(map_on_the_sky):
    builder = MapOnDetectorBuilder(9, 256, 256)
    w = WCS(naxis=2)
    w.wcs.crpix = [128, 128]  # Reference point in pixel
    w.wcs.cd = [[1.31e-4, 0], [0, 1.31e-4]]  # cd matrix
    w.wcs.crval = [0, 0]  #
    w.wcs.ctype = ["GLON-TAN", "GLAT-TAN"]
    wl = [WCSwId(1, 1, w)]
    si = builder.from_on_tye_sky_position(map_on_the_sky, wl)
    a = si[0].positions_on_detector
    assert 126.5 < a[0].x < 127.5
    assert 126.5 < a[0].y < 127.5


def test_from_on_tye_sky_position_value_error(map_on_the_sky):
    builder = MapOnDetectorBuilder(9, 256, 256)
    w = WCS(naxis=2)
    w.wcs.ctype = ["ICRS-TAN", "ICRS-TAN"]
    wl = [WCSwId(1, 1, w)]
    with pytest.raises(Exception) as e:
        si = builder.from_on_tye_sky_position(map_on_the_sky, wl)
    assert str(e.value) == 'Coordinate system ICRS-TAN is not supported'


# TODO: implments test for store_list_of_detector_position method
