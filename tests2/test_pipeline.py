import os

import pytest
from telescope_baseline.tools.pipeline_v2.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline_v2.detectorimagecatalogue import DetectorImageCatalogue
from telescope_baseline.tools.pipeline_v2.pipeline import Pipeline
from telescope_baseline.tools.pipeline_v2.fitsstorage import FitsStorage
from telescope_baseline.tools.pipeline_v2.ontheskyposition import OnTheSkyPosition
from astropy.wcs import WCS


def test_simulation():
    c = Pipeline()
    a = AstrometricCatalogue([
        OnTheSkyPosition(),
        OnTheSkyPosition(),
    ])
    b = c.simulation(a)
    assert(b != None)


def get_fits_file_name():
    file = os.getcwd()
    sep = file.split('\\')
    file = ""
    for i in range(len(sep)):
        file = file + sep[i] + "\\"
        if sep[i] == 'telescope_baseline':
            break
    file = file + "src\\telescope_baseline\\tools\\pipeline\\for_test.fits"
    return file


def test_analysis():
    c = Pipeline()
    file = get_fits_file_name()
    d = DetectorImageCatalogue([
        FitsStorage.load(file)
    ])
    w = WCS(naxis=2)
    w.wcs.crpix = [256, 256]  # Reference point in pixel
    w.wcs.cd = [[1.31e-4, 0], [0, 1.31e-4]]  # cd matrix
    w.wcs.crval = [0, 0]  #
    w.wcs.ctype = ["GLON-TAN", "GLAT-TAN"]
    a = c.analysis(d, w)
    assert(a != None)
