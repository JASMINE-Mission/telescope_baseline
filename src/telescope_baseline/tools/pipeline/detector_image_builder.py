import math

import numpy as np
from astropy.io import fits
from astropy.time import Time
from telescope_baseline.tools.pipeline.detector_image import DetectorImage
from telescope_baseline.tools.pipeline.map_on_detector import MapOnDetector


class DetectorImageBuilder:
    """Builder class for DetectorImage

    """
    def __init__(self, nx: int, ny: int, psf_w: float):
        """constructor

        Args:
            nx: array size of x direction
            ny: array size of y direction
            psf_w: psf width
        """
        self.__nx = nx
        self.__ny = ny
        self.__psf_w = psf_w

    def from_map_on_detector(self, si: MapOnDetector) -> DetectorImage:
        """Build DetectorImage from MapOnDetector class

        Args:
            si: MapOnDetector

        Returns:DetectorImage

        """
        positions_on_detector = si.positions_on_detector
        data_array = np.random.uniform(0.0, 10.0, (self.__nx, self.__ny))
        t_max = Time('1960-01-01 00:00:00')
        for dps in positions_on_detector:
            if dps.datetime > t_max:
                t_max = dps.datetime
            self._generate_a_stellar_image(data_array, dps)
        hdu = fits.PrimaryHDU()
        hdu.data = data_array
        hdu.header['DATE-OBS'] = str(t_max)
        detector_image = DetectorImage(hdu)
        return detector_image

    def get_nphoton(self) -> float:
        # TODO: Conversion factor is considered. 4.2e9 * 10 ** (-0.4 * self.mag)?
        return self.mag

    def _generate_a_stellar_image(self, a, dps):
        n = dps.n_photon + np.random.randn() * math.sqrt(dps.n_photon)
        if n < 0:
            n = 0
        for k in range(int(n)):
            xp = int(self.__psf_w * np.random.randn() + dps.y + 0.5)
            yp = int(self.__psf_w * np.random.randn() + dps.x + 0.5)
            if 0 <= xp < self.__nx and 0 <= yp < self.__ny:
                a[xp][yp] += 1
