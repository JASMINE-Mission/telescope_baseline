from telescope_baseline.tools.pipeline_v2.detector_image import DetectorImage


class DetectorImageCatalogue:
    def __init__(self, detector_images: list[DetectorImage] = []):
        self.__detector_images = detector_images

    def get_detector_images(self) -> list[DetectorImage]:
        return self.__detector_images