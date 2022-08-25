import pytest
from test_pipeline import get_fits_file_name

from telescope_baseline.tools.pipeline_v2.detectorimagestorage import DetectorImageStorage


def test_load():
    di = DetectorImageStorage.load(get_fits_file_name(0, 0))
    assert(di != None)