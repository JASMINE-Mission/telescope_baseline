from astropy.io import fits
from photutils.detection import find_peaks
from astropy.table import Table
from astropy.nddata import NDData
from photutils import extract_stars, EPSFBuilder
from astropy.time import Time
import uuid

from telescope_baseline.tools.pipeline_v2.ondetectorposition import OnDetectorPosition


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

    def get_on_detector_positions(self, window_size: int) -> list[OnDetectorPosition]:
        """Calculate image center position from image array data.

        Args:
            window_size: The size of window which is extracted from the image

        Returns: list of positions in detector coordinate.

        """
        data = self.__hdu.data
        peaks_tbl = find_peaks(data, threshold=200.)
        half_size = (window_size - 1) / 2
        x = peaks_tbl['x_peak']
        y = peaks_tbl['y_peak']
        mask = ((x > half_size) & (x < (data.shape[1] - 1 - half_size)) & (y > half_size) &
                (y < (data.shape[0] - 1 - half_size)))
        stars_tbl = Table()
        stars_tbl['x'] = x[mask]
        stars_tbl['y'] = y[mask]
        nddata = NDData(data=data)
        e_psf_stars = extract_stars(nddata, stars_tbl, size=window_size)
        # TODO need to convert A/D value to photon count
        e_psf_builder = EPSFBuilder(oversampling=4, maxiters=3, progress_bar=True)
        es = e_psf_stars
        e_psf_model, e_psf_stars = e_psf_builder(es)
        # TODO need to implement cross-match
        position_list = []
        for s in e_psf_stars.all_stars:
            # TODO IDもこれじゃ駄目〜
            # TODO 明るさの計算はまだ（0にしてる）
            # TODO 時刻をHBUから取ってる来る処理がまだ！！
            position_list.append(
                OnDetectorPosition(uuid.uuid4(), s.center[0], s.center[1], 0, Time('2000-01-01 00:00:00.0')))
        return position_list