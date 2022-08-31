from pathlib import Path

import pytest

from telescope_baseline.tools.pipeline_v2.detector_image_catalogue import DetectorImageCatalogue
from tests2.test_pipeline import get_tests_file_name


def test_load():
    f = Path(get_tests_file_name('tmp0_0.fits'))
    folder = f.parent
    dc = DetectorImageCatalogue.load(folder)
    di = dc.get_detector_images()
    assert len(di) == 7
    folder2 = Path(folder, "tmp")
    with pytest.raises(NotADirectoryError) as e:
        _ = DetectorImageCatalogue.load(folder2)

# TODO. test for save ?
