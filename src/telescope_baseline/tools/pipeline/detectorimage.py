import numpy as np
from astropy.io import fits

from telescope_baseline.tools.pipeline.simcomponent import SimComponent


class DetectorImage(SimComponent):
    """Data hold class for detector whole image.

    Attributes:
        __nx: number of pixel in x direction
        __ny: number of pixel in u direction
        __psf_w: psf width in pixel unit.
        __array: ndarray of pixel data
        __hdu: fits primary hdu

    Todo:
        * detector format should be flexible
        * PSF shape should be flexible, is now assumed as Gaussian

    """
    def __init__(self, file_name):
        super().__init__()
        self.__nx = 100
        self.__ny = 100
        self.__psf_w = 1.0
        self.__array = []
        self.__hdu = fits.PrimaryHDU()
        self.__file_name = file_name

    def get_child_size(self):
        pass

    def get_child(self, i: int):
        pass

    def get_hdu(self):
        return self.__hdu

    def make_image(self):
        self.__array = np.random.uniform(0.0, 10.0, (self.__nx, self.__ny))
        for s in self.get_parent_list():
            for j in range(int(s.mag)):
                xp = int(self.__psf_w * np.random.randn() + s.y + 0.5)
                yp = int(self.__psf_w * np.random.randn() + s.x + 0.5)
                if 0 <= xp < self.__nx and 0 <= yp < self.__ny:
                    self.__array[xp][yp] += 1

    def load(self):
        ft = fits.open(self.__file_name)
        self.__nx = ft[0].header['NAXIS1']
        self.__ny = ft[0].header['NAXIS2']
        self.__hdu = ft[0]

    def make_fits(self):
        self.__hdu = fits.PrimaryHDU()
        self.__hdu.data = self.__array
        return self.__hdu

    def save_fits(self):
        self.__hdu.writeto(self.__file_name, overwrite=True)

    def get_array(self):
        return self.__array

    def accept(self, v):
        v.visit(self)
