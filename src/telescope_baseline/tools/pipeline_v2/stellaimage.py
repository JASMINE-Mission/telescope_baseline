from astropy.wcs import WCS

from telescope_baseline.tools.pipeline_v2.ondetectorposition import OnDetectorPosition

#windows_sizeいらないかも
from telescope_baseline.tools.pipeline_v2.skyposition import SkyPosition


class StellarImage:
    def __init__(self, wcs: WCS, window_size: int = 9, detector_positions: list[OnDetectorPosition] = []):
        self.__wcs = wcs
        self.__window_size = window_size
        self.__detector_positions = detector_positions

    def get_window_size(self):
        return self.__window_size

    def get_sky_positions(self):
        ret = []
        for i in range(len(self.__detector_positions)):
            position = self.__detector_positions[i]
            sky = self.__wcs.pixel_to_world(position.x, position.y)
            print(sky)
            # TODO: Consideration is needed how ids are set.
            ret.append(SkyPosition(position.exposure_id, 0, sky, position.mag, position.datetime))
        return ret

    @property
    def detector_posotions(self):
        return self.__detector_positions
