from telescope_baseline.tools.pipeline_v2.detector_image import DetectorImage
from astropy.io import fits


class FitsStorage:
    @staticmethod
    def load(filename: str) -> DetectorImage:
        ft = fits.open(filename)
        return DetectorImage(ft[0])
