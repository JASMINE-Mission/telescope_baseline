from telescope_baseline.tools.pipeline_v2.ontheskyposition import OnTheSkyPosition
from telescope_baseline.tools.pipeline_v2.wcswid import WCSwId
from telescope_baseline.tools.pipeline_v2.detectorimagecatalogue import DetectorImageCatalogue
from telescope_baseline.tools.pipeline_v2.ondetectorposition import OnDetectorPosition
from telescope_baseline.tools.pipeline_v2.skyposition import SkyPosition
from telescope_baseline.tools.pipeline_v2.stella_image import StellarImage
from astropy.wcs import WCS


class StellarImageBuilder:
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

    def from_detector_image_catalogue(self, wcs: WCS, c: DetectorImageCatalogue) -> list[StellarImage]:
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
            sil.append(StellarImage(wcs, di.get_on_detector_positions(self.__window_size)))
        return sil

    def from_on_tye_sky_position(self, o: OnTheSkyPosition, wl: list[WCSwId]) -> list[StellarImage]:
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
            si.append(StellarImage(wl[0].wcs, detector_positions=a))
        return si

    def _store_list_of_detector_position(self, sky_positions, tmp):
        a = []
        for k in range(len(tmp)):
            if not (tmp[k][0] < 0 or tmp[k][1] < 0 or tmp[k][0] > self.__nx or tmp[k][1] > self.__ny):
                a.append(OnDetectorPosition(k, tmp[k][0], tmp[k][1], sky_positions[0].datetime, 3000))
        return a
