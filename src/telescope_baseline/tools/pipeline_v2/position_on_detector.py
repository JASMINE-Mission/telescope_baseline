from astropy.time import Time
from telescope_baseline.tools.pipeline_v2.position2d import Position2D


class PositionOnDetector:
    """Data class for detector position of individual image.

    """
    def __init__(self, exposure_id: int, p: Position2D, datetime: Time, mag: float = 12.5):
        """ constructor

        Args:
            exposure_id: exposure_id
            x: x coordinate of position in detector coordinate
            y: y coordinate of position in detector coordinate
            mag: magnitude
            datetime: exposuer date
        """
        self.__exposure_id = exposure_id
        self.__x = p.x
        self.__y = p.y
        self.__mag = mag
        self.__datetime = datetime

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def exposure_id(self):
        return self.__exposure_id

    @property
    def mag(self):
        return self.__mag

    @property
    def datetime(self):
        return self.__datetime

