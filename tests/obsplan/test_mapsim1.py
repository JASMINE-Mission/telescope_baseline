import pytest
from telescope_baseline.obsplan.mapsim1 import make_image
import filecmp
import os

def test_it():
    os.remove("map.svg")
    make_image()
    assert(filecmp.cmp("map.svg", "../tests/obsplan/out.svg"))
    os.remove("map.svg")

