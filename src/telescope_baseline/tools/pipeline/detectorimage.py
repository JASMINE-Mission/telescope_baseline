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
        """make image array data from stellar position array.

        Returns: None

        """
        a = np.random.uniform(0.0, 10.0, (self.__nx, self.__ny))
        for s in self.get_parent_list():
            self._add_a_star_on_detector(a, s)
        self.__array = a

    def _add_a_star_on_detector(self, a, s):
        for j in range(int(s.mag)):
            pos = self._incriment_position(s)
            if self._is_include_area(pos):
                a[pos[0]][pos[1]] += 1

    def _is_include_area(self, pos):
        return 0 <= pos[0] < self.__nx and 0 <= pos[1] < self.__ny

    def _incriment_position(self, s):
        xp = int(self.__psf_w * np.random.randn() + s.y + 0.5)
        yp = int(self.__psf_w * np.random.randn() + s.x + 0.5)
        return xp, yp

    def load(self):
        """ load fits data

        Returns: None

        """
        ft = fits.open(self.__file_name)
        self.__nx = ft[0].header['NAXIS1']
        self.__ny = ft[0].header['NAXIS2']
        self.__hdu = ft[0]

    def make_fits(self):
        """ make fits data from image array data.

        Returns: header data unit of fits.

        """
        self.__hdu = fits.PrimaryHDU()
        self.__hdu.data = self.__array
        return self.__hdu

    def save_fits(self):
        """ save image array to fits file

        Returns: None

        """
        self.__hdu.writeto(self.__file_name, overwrite=True)

    def get_array(self):
        """ get image array.

        Returns: image array

        """
        return self.__array

    def accept(self, v):
        v.visit(self)
