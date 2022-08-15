import pytest
from telescope_baseline.obsplan.mapsim1 import degxys
import filecmp


def test_it():
    assert(filecmp.cmp("map.svg", "../tests/obsplan/out.svg"))
