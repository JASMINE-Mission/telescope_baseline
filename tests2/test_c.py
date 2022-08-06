import pytest
from telescope_baseline.tools.pipeline_v2.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline_v2.detectorimagecatalogue import DetectorImageCatalogue
from telescope_baseline.tools.pipeline_v2.c import C
from telescope_baseline.tools.pipeline_v2.fitsstorage import FitsStorage
from telescope_baseline.tools.pipeline_v2.ontheskyposition import OnTheSkyPosition
from astropy.wcs import WCS


def test_simulation():
    c = C()
    a = AstrometricCatalogue([
        OnTheSkyPosition(),
        OnTheSkyPosition(),
    ])
    b = c.simulation(a)
    assert(b != None)


def test_analysis():
    c = C()
    d = DetectorImageCatalogue([
        FitsStorage.load('telescope_baseline/tools/pipeline/for_test.fits')
    ])
    w = WCS(naxis=2)
    w.wcs.crpix = [256, 256]  # Reference point in pixel
    w.wcs.cd = [[1.31e-4, 0], [0, 1.31e-4]]  # cd matrix
    w.wcs.crval = [0, 0]  #
    w.wcs.ctype = ["GLON-TAN", "GLAT-TAN"]
    a = c.analysis(d, w)
    assert(a != None)
