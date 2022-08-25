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