from astropy.wcs import WCS

from telescope_baseline.tools.pipeline.astrometric_catalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.astrometric_catalogue_builder import AstrometricCatalogueBuilder
from telescope_baseline.tools.pipeline.detector_image_catalogue import DetectorImageCatalogue
from telescope_baseline.tools.pipeline.map_on_detector_builder import MapOnDetectorBuilder
from telescope_baseline.tools.pipeline.map_on_the_sky_builder import MapOnTheSkyBuilder


class Analysis:
    def __init__(self):
        pass

    def do(self, c: DetectorImageCatalogue, wcs: WCS, window_size: int = 9) -> AstrometricCatalogue:
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
        sky_positions_builder = MapOnTheSkyBuilder(wcs)
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
