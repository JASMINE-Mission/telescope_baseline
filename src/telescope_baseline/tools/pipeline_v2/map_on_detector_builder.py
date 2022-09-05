from astropy.time import Time
from photutils.detection import find_peaks
from astropy.table import Table
from astropy.nddata import NDData
from photutils import extract_stars, EPSFBuilder

from telescope_baseline.tools.pipeline_v2.detector_image import DetectorImage
from telescope_baseline.tools.pipeline_v2.map_on_the_sky import MapOnTheSky
from telescope_baseline.tools.pipeline_v2.position2d import Position2D
from telescope_baseline.tools.pipeline_v2.wcswid import WCSwId
from telescope_baseline.tools.pipeline_v2.detector_image_catalogue import DetectorImageCatalogue
from telescope_baseline.tools.pipeline_v2.position_on_detector import PositionOnDetector
from telescope_baseline.tools.pipeline_v2.map_on_detector import MapOnDetector
from astropy.wcs import WCS


class MapOnDetectorBuilder:
    """Builder class for Stellarimage class

    """
    def __init__(self, window_size: int, nx: int, ny: int):
        """constructor

        Args:
            window_size: Size of extracte window
            nx: array size in x direction
            ny: array size in y direction
        """
        self.__window_size = window_size
        self.__nx = nx
        self.__ny = ny
        pass

    def from_detector_image_catalogue(self, wcs: WCS, c: DetectorImageCatalogue) -> list[MapOnDetector]:
        """method for build from DetectorImageCatalogue to the list of StellarImage

        Args:
            wcs: world coordinate system
            c: DtectorImageCatalogue

        Returns:StellarImage

        DtectorImageCatalogue is the list of DetectorImage.  One DtectorImage instance corresponds to one StellarImage
         instance.

        """
        sil = []
        for di in c.get_detector_images():
            sil.append(MapOnDetector(self.get_on_detector_positions(di, self.__window_size)))
        return sil

    def from_on_tye_sky_position(self, o: MapOnTheSky, wl: list[WCSwId]) -> list[MapOnDetector]:
        """method for building from OnTheSkyPOsition to the list of StellarImage

        Args:
            o: OnTheSkyPosition instance
            wl: list of WCSwID, which is wrapper class of wcs with orbit_id and exposuer_id

        Returns:

        """
        sky_positions = o.positions_on_the_sky
        si = []
        for w in wl:
            if "GLON" not in w.wcs.wcs.ctype[0]:
                raise ValueError("Coordinate system " + w.wcs.wcs.ctype[0] + " is not supported")
            tmp = []
            for s in sky_positions:
                tmp.append([s.coord.galactic.l.deg, s.coord.galactic.b.deg])
            tmp = w.wcs.wcs_world2pix(tmp, 0)
            a = self._store_list_of_detector_position(sky_positions, tmp)
            si.append(MapOnDetector(positions_on_detector=a))
        return si

    def _store_list_of_detector_position(self, sky_positions, tmp):
        a = []
        for k in range(len(tmp)):
            self._check_range_of_position(a, k, sky_positions, tmp)
        return a

    def _check_range_of_position(self, a, k, sky_positions, tmp):
        if not (tmp[k][0] < 0 or tmp[k][1] < 0 or tmp[k][0] > self.__nx or tmp[k][1] > self.__ny):
            a.append(PositionOnDetector(k, Position2D(tmp[k][0], tmp[k][1]), sky_positions[0].datetime, mag=3000))

    def get_on_detector_positions(self, detector_image: DetectorImage, window_size: int) -> list[PositionOnDetector]:
        """Calculate image center position from image array data.

        Args:
            window_size: The size of window which is extracted from the image

        Returns: list of positions in detector coordinate.

        """
        data = detector_image.hdu.data
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
                PositionOnDetector(1, Position2D(s.center[0], s.center[1]), Time('2000-01-01 00:00:00.0'), mag=3000))
        return position_list
