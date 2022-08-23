from astropy.time import Time

class OnDetectorPosition:
    """Data class for detector position of individual image.

    """
    def __init__(self, exposuer_id: int, x: float, y: float, mag: float, datetime: Time):
        """ constructor

        Args:
            exposuer_id: exposure_id
            x: x coordinate of position in detector coordinate
            y: y coordinate of position in detector coordinate
            mag: magnitude
            datetime: exposuer date
        """
        self.__exposure_id = exposuer_id
        self.__x = x
        self.__y = y
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

