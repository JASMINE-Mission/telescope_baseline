from telescope_baseline.tools.pipeline.astrometric_catalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.detector_image_builder import DetectorImageBuilder
from telescope_baseline.tools.pipeline.detector_image_catalogue import DetectorImageCatalogue
from telescope_baseline.tools.pipeline.map_on_the_sky_builder import MapOnTheSkyBuilder
from telescope_baseline.tools.pipeline.map_on_detector_builder import MapOnDetectorBuilder
from telescope_baseline.tools.pipeline.wcswid import WCSwId
from pathlib import Path
from astropy.time import Time


class Simulation:
    """The class for pipeline

    """

    def __init__(self, t: list[Time], w_list: list[WCSwId], folder: str, overwrite: bool):
        self.__t = t
        self.__w_list = w_list
        self.__folder = folder
        self.__overwrite = overwrite

    def do(self, a: AstrometricCatalogue, pix_max: int, psf_w: float) \
            -> list[DetectorImageCatalogue]:
        """pipeline of generate image from astrometric catalogue

        Args:
            a: AstrometricCatalogue which contains list of 5 astrometric parameters of whole stars plus magnitude.
            pix_max: array size
            psf_w: PSF width in pixel unit.

        Returns:
            # TODO: it should be the DetectorImageCatalogue
            List of A DetectorImage objects of whole mission.

        """
        sky_positions_builder = MapOnTheSkyBuilder(self.__w_list[0].wcs)
        sib = MapOnDetectorBuilder(9, pix_max, pix_max)
        dib = DetectorImageBuilder(pix_max, pix_max, psf_w)
        Path(self.__folder).mkdir(parents=True, exist_ok=True)

        sky_positions = sky_positions_builder.from_astrometric_catalogue_2_list(a, self.__t)
        dic = []
        # loop of orbit
        for o in sky_positions:
            wl = self._get_effective_wcs_list(o)
            if len(wl) > 0:
                di = self._generate_hdus(dib, o, sib, wl)
            dic.append(DetectorImageCatalogue(di))
        return dic

    def _get_effective_wcs_list(self, o):
        wl = []
        for w in self.__w_list:
            if w.orbit_id == o.orbit_id:
                wl.append(w)
        return wl

    def _generate_hdus(self, dib, o, sib, wl):
        di = []
        # loop of exposure
        si = sib.from_on_the_sky_position(o, wl)
        for j in range(len(wl)):
            di.append(dib.from_map_on_detector(si[j]))
            di[j].hdu.header.extend(wl[j].wcs.to_fits()[0].header)
            di[j].hdu.header['DATE-OBS'] = str(self.__t[o.orbit_id])
            fname = "tmp" + str(o.orbit_id) + "_" + str(j) + ".fits"
            fpathname = Path(self.__folder, fname)
            di[j].hdu.writeto(str(fpathname), overwrite=self.__overwrite)
        return di
