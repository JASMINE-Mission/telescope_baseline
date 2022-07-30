from telescope_baseline.tools.pipeline.visitor import SimVisitor
import pytest


class SimpleDownwardVisitor(SimVisitor):
    def __init__(self):
        self.__num = 0

    def visit_di(self, obj):
        print("DetectorImage")
        self.__num += 1

    def visit_si(self, obj):
        print("StellarImage")
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)
        self.__num += 10

    def visit_os(self, obj):
        print("OnTheSkyPosition")
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)
        self.__num += 100

    def visit_ap(self, obj):
        print("AstrometricCatalogue")
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)
        self.__num += 1000

    def num(self):
        return self.__num


@pytest.fixture(scope="module")
def fixture1():
    from telescope_baseline.tools.pipeline.stellarimage import StellarImage
    from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
    from astropy.wcs import WCS
    wcs = WCS(naxis=2)
    print("Pre Processing\n")
    v = SimpleDownwardVisitor()
    a = DetectorImage("output.fits")
    b = DetectorImage("output.fits")
    c = StellarImage(wcs)
    c.add_child(a)
    c.add_child(b)
    c.accept(v)
    return v


def test_1(fixture1):
    assert fixture1.num() == 12
