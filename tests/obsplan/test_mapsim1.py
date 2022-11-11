from telescope_baseline.obsplan.mapsim1 import Mapsim1
import filecmp
import os

def test_make_image():
    if os.path.isfile("map.svg"):
        os.remove("map.svg")
    Mapsim1().make_image()
    assert(filecmp.cmp("map.svg", "../tests/obsplan/out.svg"))
    os.remove("map.svg")

