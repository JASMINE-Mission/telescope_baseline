import csv

from astropy.coordinates import SkyCoord
from astropy.time import Time

from telescope_baseline.tools.pipeline_v2.position_on_the_sky import PositionOnTheSky


class MapOnTheSky:
    """Data holder class of SkyPosition for every orbit.

    """
    def __init__(self, orbit_id: int = -1, positions_on_the_sky: list[PositionOnTheSky] = []):
        """constructor

        Args:
            positions_on_the_sky: list of SkyPosition class object.
            orbit_id: orbit ID
        """
        self.__positions_on_the_sky = positions_on_the_sky
        self.__orbit_id = orbit_id

    @property
    def positions_on_the_sky(self):
        return self.__positions_on_the_sky

    @property
    def orbit_id(self):
        return self.__orbit_id

    @staticmethod
    def load(file_name: str):
        tmp = []
        file = open(file_name, 'r', newline='')
        f = csv.reader(file, delimiter=',')
        for row in f:
            if len(row) == 1:
                orbit_id = int(row[0])
            else:
                tmp.append(PositionOnTheSky(int(row[0]),
                                            SkyCoord(ra=float(row[1]), dec=float(row[2]), unit=('rad', 'rad'),
                                                     frame='icrs'), float(row[3]), Time(row[4])))
        return MapOnTheSky(orbit_id, tmp)

    def save(self, file_name: str):
        with open(file_name, 'w', newline='') as data_file:
            write = csv.writer(data_file)
            write.writerow([self.__orbit_id])
            for p in self.__positions_on_the_sky:
                write.writerow([p.stellar_id, p.coord.icrs.ra.rad, p.coord.icrs.dec.rad, p.mag, p.datetime])
