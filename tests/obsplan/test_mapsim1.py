import pytest
from telescope_baseline.obsplan.mapsim1 import make_image
import filecmp


def test_it():
    make_image()
    assert(filecmp.cmp("map.svg", "../tests/obsplan/out.svg"))
