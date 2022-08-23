from astropy.time import Time

class SkyPosition:
    """Data class for the position in the sky coordinate for individual time

    """
    def __init__(self, num, orbit_id, coord, mag, datetime: Time):
        """Constructor

        Args:
            num: ID
            coord: coordinate
            mag: magnitude
        """
        self.__stellar_id = num
        self.__orbit_id = orbit_id
        self.__coord = coord
        self.__mag = mag
        self.__datetime = datetime

    @property
    def stellar_id(self):
        return self.__stellar_id

    @property
    def orbit_id(self):
        return self.__orbit_id

    @property
    def coord(self):
        return self.__coord

    @property
    def mag(self):
        return self.__mag

    @property
    def datetime(self):
        return self.__datetime