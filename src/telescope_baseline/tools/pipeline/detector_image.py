from astropy.io import fits
from astropy.time import Time


class DetectorImage:
    """Data class for individual detector image.

    Attributes:
        hdu: hdu (header data unit) of fits.

    """
    def __init__(self, hdu=fits.PrimaryHDU()):
        """

        Args:
            hdu: header data unit for fits file
        """
        self.__hdu = hdu

    @property
    def hdu(self):
        return self.__hdu

    @property
    def time(self):
        return Time(self.__hdu.header['DATE-OBS'])

    @staticmethod
    def load(filename: str):
        ft = fits.open(filename)
        return DetectorImage(ft[0])

    def save(self, filename: str, overwrite: bool) -> None:
        self.__hdu.writeto(filename, overwrite=overwrite)