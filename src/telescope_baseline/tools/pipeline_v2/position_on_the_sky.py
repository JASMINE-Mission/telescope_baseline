from astropy.coordinates import SkyCoord
from astropy.time import Time


class PositionOnTheSky:
    """Data class for the position in the sky coordinate for individual time

    """
    def __init__(self, stellar_id: int, coord: SkyCoord, mag: float, datetime: Time):
        """Constructor

        Args:
            stellar_id: stellar ID
            orbit_id: orbit ID
            coord: coordinate
            mag: magnitude
        """
        self.__stellar_id = stellar_id
        self.__coord = coord
        self.__mag = mag
        self.__datetime = datetime

    @property
    def stellar_id(self):
        return self.__stellar_id

    @property
    def coord(self):
        return self.__coord

    @property
    def mag(self):
        return self.__mag

    @property
    def datetime(self):
        return self.__datetime