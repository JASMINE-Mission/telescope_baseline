from astropy.coordinates import SkyCoord
import astropy.units as u

class CatalogueEntry:
    """Data class of astrometric parameters for an individual star

    """
    def __init__(self, stellar_id, coord: SkyCoord, mag):
        """The constructor

        Args:
            stellar_id: id of the entry.
            coord: astropy.coordinates.SkyCoord object which also contains proper motion and distnace.
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
        return 1 * u.pc / self.__coord.distance * 1000 * u.mas

    @property
    def distance(self):
        return self.__coord.distance / u.pc

    @property
    def pm_ra(self):
        return self.__coord.icrs.pm_ra_cosdec * u.yr / u.mas

    @property
    def pm_dec(self):
        return self.__coord.icrs.pm_dec * u.yr / u.mas

    @property
    def mag(self):
        return self.__mag
