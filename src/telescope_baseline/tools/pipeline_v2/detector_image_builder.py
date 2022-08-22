import numpy as np
from astropy.io import fits
from telescope_baseline.tools.pipeline_v2.detector_image import DetectorImage
from telescope_baseline.tools.pipeline_v2.stella_image import StellarImage


class DetectorImageBuilder:
    def __init__(self, nx: int, ny: int, psf_w: float):
        self.__nx = nx
        self.__ny = ny
        self.__psf_w = psf_w

    def from_stellar_image(self, si: StellarImage) -> DetectorImage:
        dp = si.detector_posotions
        a = np.random.uniform(0.0, 10.0, (self.__nx, self.__ny))
        for s in range(len(dp)):
            for k in range(int(dp[s].mag)):
                xp = int(self.__psf_w * np.random.randn() + dp[s].y + 0.5)
                yp = int(self.__psf_w * np.random.randn() + dp[s].x + 0.5)
                if 0 <= xp < self.__nx and 0 <= yp < self.__ny:
                    a[xp][yp] += 1
        hdu = fits.PrimaryHDU()
        hdu.data = a
        di = DetectorImage(hdu)
        return di
