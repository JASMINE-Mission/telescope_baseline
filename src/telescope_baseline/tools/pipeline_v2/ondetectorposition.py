from astropy.time import Time

class OnDetectorPosition:
    def __init__(self, n: int, x: float, y: float, mag: float, datetime: Time):
        self.__id = n
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
    def id(self):
        return self.__id

    @property
    def mag(self):
        return self.__mag

    @property
    def datetime(self):
        return self.__datetime

