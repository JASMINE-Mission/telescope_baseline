import copy
import os

import astropy
import pytest
from astropy.io.fits.hdu import hdulist
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
from pathlib import Path


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
    b = c.simulation(a, t, wlist, 1024)
    assert(b != None)


def get_fits_file_name(i:int, j:int):
    a = Path.cwd()
    if 'telescope_baseline' not in str(a):
        print("Invalid path" + str(a))
        raise OSError()
    while a.name != 'telescope_baseline':
        a = a.parent
    fname = 'tmp' + str(i) + '_' + str(j) + '.fits'
    file = Path(a, 'tests2', 'data', fname)
    return file


def test_analysis():
    c = Pipeline()
    d = DetectorImageCatalogue([
        FitsStorage.load(get_fits_file_name(1, 0)),
        FitsStorage.load(get_fits_file_name(2, 0)),
        FitsStorage.load(get_fits_file_name(7, 0)),
        FitsStorage.load(get_fits_file_name(3, 0)),
        FitsStorage.load(get_fits_file_name(8, 0)),
        FitsStorage.load(get_fits_file_name(9, 0))
    ])
    hdu = d.get_detector_images()[0].hdu
    t = hdu.header['DATE-OBS']
    w = astropy.wcs.WCS(hdu.header)
    a = c.analysis(d, w)
    assert(a != None)
