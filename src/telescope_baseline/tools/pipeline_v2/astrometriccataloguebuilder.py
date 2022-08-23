import math

import numpy as np
from astropy.coordinates import get_sun
from scipy import optimize

from telescope_baseline.tools.pipeline_v2.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline_v2.ontheskyposition import OnTheSkyPosition


def lsf_fit_function_for_astrometric_parameters(parameter, t, lon, lat):
    """ fitting function for leastsq function

    Args:
        parameter: array for [lon0, lat0, pm_lon_coslat, pm_lat, para]
        t: array of astropy.time.Time object of each observation.
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
    lont = np.ndarray((np.size(ty)))
    latt = np.ndarray((np.size(ty)))
    residual = np.ndarray((len(ty)))
    for i in range(len(ty)):
        lont[i] = lon0 + (para * math.sin(ls[i] - lon0) + pm_lon_coslat * ty[i]) / math.cos(lat0)
        latt[i] = lat0 + (pm_lat * ty[i] - para * math.sin(lat0) * math.cos(ls[i] - lon0))
        residual[i] = (lon[i] - lont[i]) ** 2 + (lat[i] - latt[i]) ** 2
    return residual


class AstrometricCatalogueBuilder:
    """Builer class for AstrometricCatalogue

    """
    def __init__(self):
        pass

    def from_on_the_sky_position(self, otsp: list[OnTheSkyPosition]):
        """Class for build AstrometricCatalogue from the list of OnTheSkyPosition

        Args:
            otsp: list of OnTheSkyPosition

        Returns:AstrometriCatalogue

        """
        sid = []
        for o in otsp:
            spl = o.sky_positions
            for s in spl:
                sid.append(s.stellar_id)
        sid = list(set(sid))
        result = []
        for s in sid:
            t = []
            londata = []
            latdata = []
            for o in otsp:
                tmpt, tmplon, tmplat = self._add_individual_observation(o, s)
                t.extend(tmpt)
                londata.extend(tmplon)
                latdata.extend(tmplat)
            parameter = [np.radians(266), np.radians(-5), 0., 0., np.radians(1 / 3600)]
            result.append(optimize.leastsq(lsf_fit_function_for_astrometric_parameters, parameter,
                                           args=(t, londata, latdata)))
        return AstrometricCatalogue(result)

    def _add_individual_observation(self, o, s):
        tmpt = []
        tmplon = []
        tmplat = []
        for ss in o.sky_positions:
            if s == ss.stellar_id:
                tmpt.append(ss.datetime)
                tmplon.append(ss.coord.barycentricmeanecliptic.lon.rad)
                tmplat.append(ss.coord.barycentricmeanecliptic.lat.rad)
        return tmpt, tmplon, tmplat
