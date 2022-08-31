import numpy as np
from astropy.io import fits
from astropy.time import Time

from telescope_baseline.tools.pipeline_v2.detector_image import DetectorImage
from telescope_baseline.tools.pipeline_v2.map_on_detector import MapOnDetector


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

    def from_stellar_image(self, si: MapOnDetector) -> DetectorImage:
        """Build DetectorImage from StellarImage class

        Args:
            si: StellarImage

        Returns:DetctorImage

        """
        dp = si.positions_on_detector
        a = np.random.uniform(0.0, 10.0, (self.__nx, self.__ny))
        t_max = Time('1960-01-01 00:00:00')
        for dps in dp:
            if dps.datetime > t_max:
                t_max = dps.datetime
            self._generate_a_stellar_image(a, dps)
        hdu = fits.PrimaryHDU()
        hdu.data = a
        hdu.header['DATE-OBS'] = str(t_max)
        di = DetectorImage(hdu)
        return di

    def _generate_a_stellar_image(self, a, dps):
        for k in range(int(dps.mag)):
            xp = int(self.__psf_w * np.random.randn() + dps.y + 0.5)
            yp = int(self.__psf_w * np.random.randn() + dps.x + 0.5)
            if 0 <= xp < self.__nx and 0 <= yp < self.__ny:
                a[xp][yp] += 1
