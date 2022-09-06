from pathlib import Path
import pytest
import tempfile
from telescope_baseline.tools.pipeline.detector_image_catalogue import DetectorImageCatalogue
from test_pipeline import get_tests_file_name


def test_load():
    f = Path(get_tests_file_name('tmp0_0.fits'))
    folder = f.parent
    dc = DetectorImageCatalogue.load(folder)
    di = dc.get_detector_images()
    assert len(di) == 8
    folder2 = Path(folder, "tmp")
    with pytest.raises(NotADirectoryError) as e:
        _ = DetectorImageCatalogue.load(folder2)


def test_save():
    f = Path(get_tests_file_name('tmp0_0.fits'))
    folder = f.parent
    loaded = DetectorImageCatalogue.load(folder)
    sut_len = len(loaded.get_detector_images())
    assert sut_len == 8
    with tempfile.TemporaryDirectory() as dname:
        print(dname)
        path = Path(dname, 'fits')
        loaded.save(path)
        assert len(list(path.iterdir())) == sut_len
