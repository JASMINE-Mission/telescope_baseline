import copy
import astropy
from astropy.time import Time
from telescope_baseline.tools.pipeline.analysis import Analysis
from telescope_baseline.tools.pipeline.astrometric_catalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.catalog_entry import CatalogueEntry
from telescope_baseline.tools.pipeline.detector_image import DetectorImage
from telescope_baseline.tools.pipeline.detector_image_catalogue import DetectorImageCatalogue
from telescope_baseline.tools.pipeline.simulation import Simulation
from telescope_baseline.tools.pipeline.wcswid import WCSwId
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.wcs import WCS
from pathlib import Path


def test_simulation():
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
    c = Simulation(t=t, w_list=wlist, folder="tmp", overwrite=True)
    b = c.do(a, 1024, 1.0)
    assert(b is not None)


def get_tests_file_name(fname: str, folder='data'):
    a = Path.cwd()
    tests_dir = 'tests/pipeline'    # change it when test dir move
    if 'telescope_baseline' not in str(a):
        return Path(a, tests_dir, folder, fname)
    while a.name != 'telescope_baseline':
        a = a.parent
    if folder != 'data':
        tmp_path = Path(a, tests_dir, folder)
        if not tmp_path.exists():
            tmp_path.mkdir()
    file = Path(a, tests_dir, folder, fname)
    return file


def test_analysis():
    c = Analysis()
    d = DetectorImageCatalogue([
        DetectorImage.load(str(get_tests_file_name('tmp1_0.fits'))),
        DetectorImage.load(str(get_tests_file_name('tmp2_0.fits'))),
        DetectorImage.load(str(get_tests_file_name('tmp7_0.fits'))),
        DetectorImage.load(str(get_tests_file_name('tmp3_0.fits'))),
        DetectorImage.load(str(get_tests_file_name('tmp8_0.fits'))),
        DetectorImage.load(str(get_tests_file_name('tmp9_0.fits')))
    ])
    hdu = d.get_detector_images()[0].hdu
    t = hdu.header['DATE-OBS']
    w = astropy.wcs.WCS(hdu.header)
    a = c.do(d, w)
    assert(a is not None)
