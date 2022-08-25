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
            sil.append(MapOnDetector(wcs, di.get_on_detector_positions(self.__window_size)))
        return sil

    def from_on_tye_sky_position(self, o: MapOnTheSky, wl: list[WCSwId]) -> list[MapOnDetector]:
        """method for building from OnTheSkyPOsition to the list of StellarImage

        Args:
            o: OnTheSkyPosition instance
            wl: list of WCSwID, which is wrapper class of wcs with orbit_id and exposuer_id

        Returns:

        """
        sky_positions = o.sky_positions
        si = []
        for w in wl:
            if "GLON" not in w.wcs.wcs.ctype[0]:
                print("Coordinate system " + w.wcs.wcs.ctype[0] + " is not supported")
                raise ValueError
            tmp = []
            for s in sky_positions:
                tmp.append([s.coord.galactic.l.deg, s.coord.galactic.b.deg])
            tmp = w.wcs.wcs_world2pix(tmp, 0)
            a = self._store_list_of_detector_position(sky_positions, tmp)
            si.append(MapOnDetector(wl[0].wcs, detector_positions=a))
        return si

    def _store_list_of_detector_position(self, sky_positions, tmp):
        a = []
        for k in range(len(tmp)):
            if not (tmp[k][0] < 0 or tmp[k][1] < 0 or tmp[k][0] > self.__nx or tmp[k][1] > self.__ny):
                a.append(PositionOnDetector(k, Position2D(tmp[k][0], tmp[k][1]), sky_positions[0].datetime, mag=3000))
        return a
