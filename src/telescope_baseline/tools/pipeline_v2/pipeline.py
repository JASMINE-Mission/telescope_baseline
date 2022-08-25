from telescope_baseline.tools.pipeline_v2.astrometric_catalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline_v2.astrometric_catalogue_builder import AstrometricCatalogueBuilder
from telescope_baseline.tools.pipeline_v2.detector_image_builder import DetectorImageBuilder
from telescope_baseline.tools.pipeline_v2.detector_image_catalogue import DetectorImageCatalogue
from telescope_baseline.tools.pipeline_v2.map_on_the_sky_builder import MapOnTheSkyBuilder
from telescope_baseline.tools.pipeline_v2.map_on_detector_builder import MapOnDetectorBuilder
from telescope_baseline.tools.pipeline_v2.wcswid import WCSwId
from pathlib import Path
from astropy.wcs import WCS
from astropy.time import Time


class Pipeline:
    """The class for pipeline

    """

    def __init__(self, t: list[Time] = [], w_list: list[WCSwId] = []):
        self.__t = t
        self.__w_list = w_list
        self.__folder = 'data'

    def simulation(self, a: AstrometricCatalogue, pix_max: int, psf_w: float)\
            -> list[DetectorImageCatalogue]:
        """pipeline of generate image from astrometric catalogue

        Args:
            a: AstrometricCatalogue which contains list of 5 parameters of whole stars.
            t: array of Time.  Each element corresponds to orbit.
            w_list: array of WCSwId. WCSwId contains WCS object, orbit ID and exposure ID.
            pix_max: Maximum pixel number.
            psf_w: PSF width in pixel unit.

        Returns:
            A DetectorImageCatalogue object which contains DetectorImage objects of whole mission.

        """
        sky_positions_builder = MapOnTheSkyBuilder()
        sib = MapOnDetectorBuilder(9, pix_max, pix_max)
        dib = DetectorImageBuilder(pix_max, pix_max, psf_w)
        if not Path(self.__folder).exists():
            Path(self.__folder).mkdir()

        sky_positions = sky_positions_builder.from_astrometric_catalogue_2_list(a, self.__t)
        dic = []
        # loop of orbit
        for o in sky_positions:
            wl = self._get_effective_wcs_list(o)
            if len(wl) > 0:
                di = self._generate_one_hdu(dib, o, sib, wl)
            dic.append(DetectorImageCatalogue(di))
        return dic

    def _get_effective_wcs_list(self, o):
        wl = []
        for w in self.__w_list:
            if w.orbit_id == o.orbit_id:
                wl.append(w)
        return wl

    def _generate_one_hdu(self, dib, o, sib, wl):
        di = []
        # loop of exposure
        si = sib.from_on_tye_sky_position(o, wl)
        for j in range(len(wl)):
            di.append(dib.from_stellar_image(si[j]))
            di[j].hdu.header.extend(wl[j].wcs.to_fits()[0].header)
            di[j].hdu.header['DATE-OBS'] = str(self.__t[o.orbit_id])
            fname = "tmp" + str(o.orbit_id) + "_" + str(j) + ".fits"
            fpathname = Path(self.__folder, fname)
            di[j].hdu.writeto(str(fpathname), overwrite=True)
        return di

    def analysis(self, c: DetectorImageCatalogue, wcs: WCS, window_size: int = 9) -> AstrometricCatalogue:
        """pipeline of solve astrometric catalogue from detector images.

        Args:
            c: A DetectorImageCatalogue object which contains DetectorImage objects of whole mission.
            wcs:
            window_size: size of windows which is extracted from detector image.

        Returns:
            AstrometricCatalogue which contains list of 5 parameters of whole stars.
        """
        # TODO: wcs is not constant whole the mission.
        sib = MapOnDetectorBuilder(window_size, 1024, 1024)
        sky_positions_builder = MapOnTheSkyBuilder()
        acb = AstrometricCatalogueBuilder()

        cat = c.get_detector_images()
        cat.sort(key=lambda x: x.time)

        dic_list = []
        n = len(cat)
        t0 = 1 / 50
        di = [cat[0]]
        for i in range(1, n):
            if cat[i].time - cat[i-1].time < t0:
                di.append(cat[i])
            else:
                dic_list.append(DetectorImageCatalogue(di))
                di = [cat[i]]
        dic_list.append(DetectorImageCatalogue(di))

        # loop of orbit
        sky_positions = []
        for dic in dic_list:
            stellar_image_list = sib.from_detector_image_catalogue(wcs, dic)
            sky_positions.append(sky_positions_builder.from_stellar_image(stellar_image_list))
            # TODO. should be implement from list to object / outside of the loop of dic.
        return acb.from_on_the_sky_position(sky_positions)
