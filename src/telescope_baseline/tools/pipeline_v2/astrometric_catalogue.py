import csv

from astropy.coordinates import SkyCoord
import astropy.units as u
from telescope_baseline.tools.pipeline_v2.catalog_entry import CatalogueEntry


class AstrometricCatalogue:
    """Data holder class for astrometric catalogue.

    Attributes:
        catalogue_entries: list of CatalogueEntry which is 5 parameter list for one star.

    """
    def __init__(self, catalogue_entries: list[CatalogueEntry] = []):
        """Constructor

        Args:
            catalogue_entries: list of CatalogueEntry
        """
        self.__catalogue_entries = catalogue_entries

    def get_catalogue(self) -> list[CatalogueEntry]:
        """

        Returns: array of CatalogueEntry

        """
        return self.__catalogue_entries

    def save(self, file_name: str):
        with open(file_name, 'w', newline='') as data_file:
            write = csv.writer(data_file)
            for e in self.__catalogue_entries:
                write.writerow([e.stellar_id, e.ra, e.dec, e.pm_ra, e.pm_dec, e.distance, e.coord.obstime, e.mag])

    @staticmethod
    def load(file_name: str):
        tmp = []
        file = open(file_name, 'r', newline='')
        f = csv.reader(file, delimiter=',')
        for row in f:
            print(row)
            tmp.append(CatalogueEntry(int(row[0]),
                                      SkyCoord(ra=float(row[1]), dec=float(row[2]), unit=('deg', 'deg'), obstime=row[6],
                                               pm_ra_cosdec=float(row[3]) * u.mas/u.yr,
                                               pm_dec=float(row[4]) * u.mas/u.yr, distance=float(row[5])*u.pc,
                                               frame='icrs'), float(row[7])))
        return AstrometricCatalogue(tmp)
