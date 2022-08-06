import numpy as np
from astropy.io import fits
from photutils.detection import find_peaks
from astropy.table import Table
from astropy.nddata import NDData
from photutils import extract_stars, EPSFBuilder
from astropy.time import Time
import uuid

from telescope_baseline.tools.pipeline_v2.ondetectorposition import OnDetectorPosition


class DetectorImage:
    def __init__(self, hbu=fits.PrimaryHDU()):
        self.__hbu = hbu

    def get_on_detector_positions(self, window_size:int) -> list[OnDetectorPosition] :
        data = self.__hbu.data
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
        position_list = []
        for s in e_psf_stars.all_stars:
            # TODO IDもこれじゃ駄目〜
            # TODO 明るさの計算はまだ（0にしてる）
            # TODO 時刻をHBUから取ってる来る処理がまだ！！
            position_list.append(
                OnDetectorPosition(uuid.uuid4(), s.center[0], s.center[1], 0, Time('2000-01-01 00:00:00.0')))
        return position_list