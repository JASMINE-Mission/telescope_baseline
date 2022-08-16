from astropy.wcs import WCS


class WCSwId:

    def __init__(self, orbit_id: int, exposure_id: int, wcs: WCS):
        self.__orbit_id = orbit_id
        self.__exposure_id = exposure_id
        self.__wcs = wcs

    @property
    def orbit_id(self):
        return self.__orbit_id

    @property
    def exposure_id(self):
        return self.__exposure_id

    @property
    def wcs(self):
        return self.__wcs
