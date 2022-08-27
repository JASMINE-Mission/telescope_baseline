import pytest

from telescope_baseline.tools.pipeline_v2.detector_image import DetectorImage
from test_pipeline import get_fits_file_name


def test_load():
    di = DetectorImage.load(get_fits_file_name('tmp0_0.fits'))
    assert(di != None)