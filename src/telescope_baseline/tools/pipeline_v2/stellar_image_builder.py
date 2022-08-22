from telescope_baseline.tools.pipeline_v2.ontheskyposition import OnTheSkyPosition
from telescope_baseline.tools.pipeline_v2.wcswid import WCSwId
from telescope_baseline.tools.pipeline_v2.detectorimagecatalogue import DetectorImageCatalogue
from telescope_baseline.tools.pipeline_v2.ondetectorposition import OnDetectorPosition
from telescope_baseline.tools.pipeline_v2.skyposition import SkyPosition
from telescope_baseline.tools.pipeline_v2.stella_image import StellarImage
from astropy.wcs import WCS


class StellarImageBuilder:
    def __init__(self, window_size: int, nx: int, ny: int):
        self.__window_size = window_size
        self.__nx = nx
        self.__ny = ny
        pass

    def from_detector_image_catalogue(self, wcs: WCS, c: DetectorImageCatalogue) -> StellarImage:
        position_list = []
        for di in c.get_detector_images():
            position_list.extend(di.get_on_detector_positions(self.__window_size))
        return StellarImage(wcs, position_list)

    def from_on_tye_sky_position(self, o: OnTheSkyPosition, wl: list[WCSwId]) -> StellarImage:
        sky_positions = o.sky_positions
        if "GLON" not in wl[0].wcs.wcs.ctype[0]:
            print("Coordinate system " + wl[0].wcs.wcs.ctype[0] + " is not supported")
            raise ValueError
        tmp = []
        for k in range(len(sky_positions)):
            tmp.append([sky_positions[k].coord.galactic.l.deg, sky_positions[k].coord.galactic.b.deg])
        tmp = wl[0].wcs.wcs_world2pix(tmp, 0)
        a = []
        for k in range(len(tmp)):
            print(tmp[k])
            if not (tmp[k][0] < 0 or tmp[k][1] < 0 or tmp[k][0] > self.__nx or tmp[k][1] > self.__ny):
                a.append(OnDetectorPosition(k, tmp[k][0], tmp[k][1], 3000, sky_positions[0].datetime))
        return StellarImage(wl[0].wcs, detector_positions=a)

