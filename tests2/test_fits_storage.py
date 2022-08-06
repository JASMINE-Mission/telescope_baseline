import pytest

from telescope_baseline.tools.pipeline_v2.fitsstorage import FitsStorage


def test_load():
    di = FitsStorage.load('telescope_baseline/tools/pipeline/for_test.fits')
    assert(di != None)