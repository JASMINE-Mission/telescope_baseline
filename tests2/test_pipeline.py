import copy
import os

import pytest
from astropy.time import Time

from telescope_baseline.tools.pipeline_v2.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline_v2.catalogentry import CatalogueEntry
from telescope_baseline.tools.pipeline_v2.detectorimagecatalogue import DetectorImageCatalogue
from telescope_baseline.tools.pipeline_v2.pipeline import Pipeline
from telescope_baseline.tools.pipeline_v2.fitsstorage import FitsStorage
from telescope_baseline.tools.pipeline_v2.wcswid import WCSwId
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.wcs import WCS


def test_simulation():
    c = Pipeline()
    a = AstrometricCatalogue([
        CatalogueEntry(1,
                       SkyCoord(l=0., b=0., unit=('rad', 'rad'), frame='galactic', obstime='2000-01-01 00:00:00.0',
                                distance=1.0 * u.pc, pm_l_cosb=10 * u.mas / u.yr, pm_b=10 * u.mas / u.yr),
                       12.5),
    ])
    t = [Time('2000-01-01 00:00:00.0'), Time('2000-02-01 00:00:00.0'), Time('2000-03-01 00:00:00.0'),
         Time('2000-04-01 00:00:00.0'), Time('2000-05-01 00:00:00.0'), Time('2000-06-01 00:00:00.0'),
         Time('2000-07-01 00:00:00.0'), Time('2000-08-01 00:00:00.0'), Time('2000-09-01 00:00:00.0'),
         Time('2000-10-01 00:00:00.0'), Time('2000-11-01 00:00:00.0'), Time('2000-12-01 00:00:00.0'),
         Time('2001-01-01 00:00:00.0')]
    w = WCS(naxis=2)
    w.wcs.crpix = [256, 256]  # Reference point in pixel
    w.wcs.cd = [[1.31e-4, 0], [0, 1.31e-4]]  # cd matrix
    w.wcs.crval = [0, 0]  #
    w.wcs.ctype = ["GLON-TAN", "GLAT-TAN"]
    wlist = []
    for i in range(len(t)):
        wlist.append(WCSwId(i, 1, copy.deepcopy(w)))
    b = c.simulation(a, t, wlist, 1024, 1.0)
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
