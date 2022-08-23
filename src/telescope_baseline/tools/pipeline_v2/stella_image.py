from astropy.wcs import WCS

from telescope_baseline.tools.pipeline_v2.ondetectorposition import OnDetectorPosition
from telescope_baseline.tools.pipeline_v2.skyposition import SkyPosition


class StellarImage:
    """Data Holder class for OnDetectorPosition.

    """
    def __init__(self, wcs: WCS, detector_positions: list[OnDetectorPosition] = []):
        """constructor

        Args:
            wcs: world coordinate system instance
            detector_positions: the position on the detector coordinate.
        """
        self.__wcs = wcs
        self.__detector_positions = detector_positions

    def get_sky_positions(self):
        ret = []
        for i in range(len(self.__detector_positions)):
            position = self.__detector_positions[i]
            sky = self.__wcs.pixel_to_world(position.x, position.y)
            # TODO: Consideration is needed how ids are set.
            ret.append(SkyPosition(position.exposure_id, 0, sky, position.mag, position.datetime))
        return ret

    @property
    def detector_posotions(self):
        return self.__detector_positions
