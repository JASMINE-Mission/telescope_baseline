from pathlib import Path

from telescope_baseline.tools.pipeline_v2.detector_image import DetectorImage


class DetectorImageCatalogue:
    """Data holder class for (multiple) DetectorImage

    """
    def __init__(self, detector_images: list[DetectorImage] = []):
        """constructor

        Args:
            detector_images: List of DetectorImage
        """
        self.__detector_images = detector_images

    def get_detector_images(self) -> list[DetectorImage]:
        """getter method

        Returns:detector_image

        """
        return self.__detector_images

    @staticmethod
    def load(foldername: str):
        p = Path(foldername)
        d = []
        for s in p.glob('*.fits'):
            d.append(DetectorImage.load(str(s)))
        return DetectorImageCatalogue(d)

    def save(self, foldername: str):
        p = Path(foldername)
        if not p.exists():
            raise FileNotFoundError()
        i = 0
        for d in self.__detector_images:
            filename = 'tmp_{:0=4}'.format(i) + '.fits'
            fpath = Path(p, filename)
            d.save(str(fpath))
            i += 1
