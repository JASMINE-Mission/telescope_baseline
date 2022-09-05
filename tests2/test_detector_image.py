import pytest

from telescope_baseline.tools.pipeline_v2.detector_image import DetectorImage
from test_pipeline import get_tests_file_name


@pytest.fixture
def detector_image():
    return DetectorImage.load(get_tests_file_name('tmp0_0.fits'))


def test_load(detector_image):
    assert detector_image is not None


def test_time(detector_image):
    assert detector_image.time == '2000-01-01 00:00:00.000'


def test_position(detector_image):
    li = detector_image.get_on_detector_positions(9)
    assert len(li) == 1
    assert abs(li[0].x - 255) < 1.0
    assert abs(li[0].y - 255) < 1.0
