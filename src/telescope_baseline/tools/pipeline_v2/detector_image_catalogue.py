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
        if not p.exists():
            raise NotADirectoryError()
        d = []
        for s in p.glob('*.fits'):
            d.append(DetectorImage.load(str(s)))
        return DetectorImageCatalogue(d)

    def save(self, foldername: str):
        p = Path(foldername)
        if not p.exists():
            p.mkdir(parents=True)
        for i in range(len(self.__detector_images)):
            filename = 'tmp_{:0=4}'.format(i) + '.fits'
            fpath = Path(p, filename)
            self.__detector_images[i].save(str(fpath))
