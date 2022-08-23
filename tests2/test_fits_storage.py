import pytest
from test_pipeline import get_fits_file_name

from telescope_baseline.tools.pipeline_v2.fitsstorage import FitsStorage


def test_load():
    di = FitsStorage.load(get_fits_file_name(0, 0))
    assert(di != None)