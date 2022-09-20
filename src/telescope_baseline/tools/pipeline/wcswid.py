from astropy.wcs import WCS


class WCSwId:
    """data class of wcs

    """

    def __init__(self, orbit_id: int, exposure_id: int, wcs: WCS):
        """constructor

        Args:
            orbit_id: orbit ID
            exposure_id: exposuer ID
            wcs: World Coordinate System
        """
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
