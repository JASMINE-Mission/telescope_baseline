import csv

from astropy.time import Time

from telescope_baseline.tools.pipeline.position2d import Position2D
from telescope_baseline.tools.pipeline.position_on_detector import PositionOnDetector


class MapOnDetector:
    """Data Holder class for OnDetectorPosition.

    """
    def __init__(self, positions_on_detector: list[PositionOnDetector] = []):
        """constructor

        Args:
            positions_on_detector: the position on the detector coordinate.
        """
        self.__positions_on_detector = positions_on_detector

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
