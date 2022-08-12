from telescope_baseline.tools.pipeline_v2.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline_v2.detectorimagecatalogue import DetectorImageCatalogue
from telescope_baseline.tools.pipeline_v2.ontheskyposition import OnTheSkyPosition
from telescope_baseline.tools.pipeline_v2.stellaimage import StellarImage
from astropy.wcs import WCS
import numpy as np
from scipy import optimize
from astropy.coordinates import get_sun
import math


def fit_astrometry(parameter, t, lon, lat):
    """ fitting function for leastsq function

    Args:
        parameter: array for [lon0, lat0, pm_lon_coslat, pm_lat, para]
        ty: array for type in year unit
        ls: solar longitude
        lon: observation result of ecliptic longitude in radian
        lat: observation result of ecliptic latitude in radian

    Returns: Updated parameter array.

    TODO: Need trade off between leastsq and least_square.

    """
    lon0 = parameter[0]
    lat0 = parameter[1]
    pm_lon_coslat = parameter[2]
    pm_lat = parameter[3]
    para = parameter[4]
    ls = []
    ty = []
    for i in range(len(t)):
        ls.append(get_sun(t[i]).geocentricmeanecliptic.lon.rad)
        ty.append(t[i].jyear)
    ls = np.array(ls)
    ty = np.array(ty)
    tc = (np.max(ty) + np.min(ty)) / 2
    ty = ty - tc
    lont = np.ndarray((len(ty)))
    latt = np.ndarray((len(ty)))
    residual = np.ndarray((len(ty)))
    for i in range(len(ty)):
        lont[i] = lon0 + (para * math.sin(ls[i] - lon0) + pm_lon_coslat * ty[i]) / math.cos(lat0)
        latt[i] = lat0 + (pm_lat * ty[i] - para * math.sin(lat0) * math.cos(ls[i] - lon0))
        residual[i] = (lon[i] - lont[i]) ** 2 + (lat[i] - latt[i]) ** 2
    return residual

class Pipeline:
    def simulation(self, a: AstrometricCatalogue) -> DetectorImageCatalogue:
        return DetectorImageCatalogue()

    def analysis(self, c: DetectorImageCatalogue, wcs: WCS, window_size: int = 9) -> AstrometricCatalogue:
        sttelar_image = self._analysys_detecotr_catalog_2_stellar_image(c, wcs, window_size)
        otsp = self._analysis_sttelar_image_2_on_the_sky_position(sttelar_image)
        return self._analysis_on_the_sky_position_2_astrometric_catalogue(otsp)

    def _analysis_on_the_sky_position_2_astrometric_catalogue(self, otsp):
        t = []
        londata = []
        latdata = []
        for i in range(len(otsp.sky_positions)):
            sp = otsp.sky_positions[i]
            t.append(sp.datetime)
            print(sp.datetime)
            londata.append(sp.coord.barycentricmeanecliptic.lon.rad)
            latdata.append(sp.coord.barycentricmeanecliptic.lat.rad)
        parameter = [np.radians(266), np.radians(-5), 0., 0., np.radians(1 / 3600)]
        # TODO: result should be the attributes of AstrometricCatalogue.
        result = optimize.leastsq(fit_astrometry, parameter, args=(t, londata, latdata))
        return AstrometricCatalogue()

    def _analysis_sttelar_image_2_on_the_sky_position(self, sttelar_image):
        skypositions = sttelar_image.get_sky_positions()
        otsp = OnTheSkyPosition(skypositions)
        return otsp

    def _analysys_detecotr_catalog_2_stellar_image(self, c, wcs, window_size):
        position_list = []
        for di in c.get_detector_images():
            position_list.extend(di.get_on_detector_positions(window_size))
        return StellarImage(wcs, window_size, position_list)