from astropy.coordinates import SkyCoord
import astropy.units as u


class CatalogueEntry:
    """Data class of astrometric parameters for an individual star

    """
    def __init__(self, stellar_id: int, coord: SkyCoord, mag: float):
        """The constructor

        Args:
            stellar_id: id of the entry.
            coord: astropy.coordinates.SkyCoord object which also contains proper motion and distance.
            mag: magnitude of the star

        TODO: Need to consistent implementation of what frame we should use.

        """
        self.__stellar_id = stellar_id
        self.__coord = coord
        self.__mag = mag

    @property
    def stellar_id(self):
        return self.__stellar_id

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
        return 1 / self.__coord.distance.to_value(u.pc) * 1000 * u.mas

    @property
    def distance(self):
        return self.__coord.distance.to_value(u.pc)

    @property
    def pm_ra_cosdec(self):
        return self.__coord.icrs.pm_ra_cosdec.to_value(u.mas / u.yr)

    @property
    def pm_dec(self):
        return self.__coord.icrs.pm_dec.to_value(u.mas / u.yr)

    @property
    def mag(self):
        return self.__mag
