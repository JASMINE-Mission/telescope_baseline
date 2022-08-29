import csv

from astropy.time import Time
from astropy.wcs import WCS

from telescope_baseline.tools.pipeline_v2.position2d import Position2D
from telescope_baseline.tools.pipeline_v2.position_on_detector import PositionOnDetector
from telescope_baseline.tools.pipeline_v2.position_on_the_sky import PositionOnTheSky


class MapOnDetector:
    """Data Holder class for OnDetectorPosition.

    """
    def __init__(self, wcs: WCS, positions_on_detector: list[PositionOnDetector] = []):
        """constructor

        Args:
            wcs: world coordinate system instance
            positions_on_detector: the position on the detector coordinate.
        """
        self.__wcs = wcs
        self.__positions_on_detector = positions_on_detector

    def get_sky_positions(self):
        ret = []
        for position in self.__positions_on_detector:
            sky = self.__wcs.pixel_to_world(position.x, position.y)
            # TODO: Consideration is needed how ids are set.
            ret.append(PositionOnTheSky(position.exposure_id, sky, position.mag, position.datetime))
        return ret

    @property
    def positions_on_detector(self):
        return self.__positions_on_detector

    @staticmethod
    def load(file_name: str):
        tmp = []
        file = open(file_name, 'r', newline='')
        f = csv.reader(file, delimiter=',')
        for row in f:
            tmp.append(PositionOnDetector(int(row[0]), Position2D(float(row[1]), float(row[2])), Time(row[4]),
                                          float(row[3])))
        return tmp

    def save(self, file_name: str):
        with open(file_name, 'w', newline='') as data_file:
            write = csv.writer(data_file)
            for p in self.__positions_on_detector:
                write.writerow([p.exposure_id, p.x, p.y, p.mag, p.datetime])
