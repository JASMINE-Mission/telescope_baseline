from astropy.coordinates import SkyCoord
import astropy.units as u


class CatalogueEntry:
    def __init__(self, number, coord:SkyCoord, mag):
        self.__id = number
        self.__coord = coord
        self.__mag = mag

    @property
    def id(self):
        return self.__id

    @property
    def coord(self):
        return self.__coord

    @property
    def ra(self):
        return self.__coord.icrs.ra.deg

    @property
    def dec(self):
        return self.__coord.icrs.dec.deg

    @property
    def parallax(self):
        return 1 * u.pc / self.__coord.distance * 1000 * u.mas

    @property
    def pm_ra(self):
        return self.__coord.icrs.pm_ra_cosdec

    @property
    def pm_dec(self):
        return self.__coord.icrs.pm_dec

    @property
    def mag(self):
        return self.__mag
