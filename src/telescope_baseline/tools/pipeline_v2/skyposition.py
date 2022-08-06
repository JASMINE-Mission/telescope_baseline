from astropy.time import Time

class SkyPosition:
    def __init__(self, num, coord, mag, datetime: Time):
        """Constructor

        Args:
            num: ID
            coord: coordinate
            mag: magnitude
        """
        self.__id = num
        self.__coord = coord
        self.__mag = mag
        self.__datetime = datetime

    @property
    def id(self):
        return self.__id

    @property
    def coord(self):
        return self.__coord

    @property
    def mag(self):
        return self.__mag

    @property
    def datetime(self):
        return self.__datetime