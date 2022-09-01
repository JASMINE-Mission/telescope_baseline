import math

import numpy as np
from astropy.coordinates import get_sun
from scipy import optimize

from telescope_baseline.tools.pipeline_v2.astrometric_catalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline_v2.map_on_the_sky import MapOnTheSky


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
    for time in t:
        ls.append(get_sun(time).geocentricmeanecliptic.lon.rad)
        ty.append(time.jyear)
    ls = np.array(ls)
    ty = np.array(ty)
    tc = (np.max(ty) + np.min(ty)) / 2
    ty = ty - tc
    lont = np.ndarray((np.size(ty)))
    latt = np.ndarray((np.size(ty)))
    residual = np.ndarray((len(ty)))
    for i in range(len(ty)):
        lont = lon0 + (para * math.sin(ls[i] - lon0) + pm_lon_coslat * ty[i]) / math.cos(lat0)
        latt = lat0 + (pm_lat * ty[i] - para * math.sin(lat0) * math.cos(ls[i] - lon0))
        residual[i] = (lon[i] - lont) ** 2 + (lat[i] - latt) ** 2
    return residual


class AstrometricCatalogueBuilder:
    """Builer class for AstrometricCatalogue

    """
    def __init__(self):
        pass

    @staticmethod
    def from_on_the_sky_position(otsp: list[MapOnTheSky]):
        """Class for build AstrometricCatalogue from the list of OnTheSkyPosition

        Args:
            otsp: list of OnTheSkyPosition

        Returns:AstrometriCatalogue

        """
        sid = []
        # TODO. to optimize loop.  Use dictionary etc.
        for o in otsp:
            spl = o.positions_on_the_sky
            for s in spl:
                sid.append(s.stellar_id)
        sid = list(set(sid))
        result = []
        for s in sid:
            latdata, londata, t = AstrometricCatalogueBuilder._time_seriese_of_individual_star(otsp, s)
            # TODO. Input appropriate initial value for least square.
            parameter = [np.radians(266), np.radians(-5), 0., 0., np.radians(1 / 3600)]
            result.append(optimize.leastsq(lsf_fit_function_for_astrometric_parameters, parameter,
                                           args=(t, londata, latdata)))
        return AstrometricCatalogue(result)


    @staticmethod
    def _update_dic(dic, position_on_the_sky):
        tupple = ([], [], [])
        if position_on_the_sky.stellar_id in dic:
            tupple = dic[position_on_the_sky.stellar_id]
        else:
            dic[position_on_the_sky.stellar_id] = tupple
        tupple[0].append(position_on_the_sky.datetime)
        tupple[1].append(position_on_the_sky.coord.barycentricmeanecliptic.lon.rad)
        tupple[2].append(position_on_the_sky.coord.barycentricmeanecliptic.lat.rad)


    @staticmethod
    def from_on_the_sky_position_2(otsp: list[MapOnTheSky]):
        dic = {}
        for map_on_the_sky in otsp:
            for position_on_the_sky in map_on_the_sky.positions_on_the_sky:
                AstrometricCatalogueBuilder._update_dic(dic, position_on_the_sky)
        result = []
        for t, londata, latdata in dic.values():
            # TODO. Input appropriate initial value for least square.
            parameter = [np.radians(266), np.radians(-5), 0., 0., np.radians(1 / 3600)]
            result.append(optimize.leastsq(lsf_fit_function_for_astrometric_parameters, parameter,
                                           args=(t, londata, latdata)))
        return AstrometricCatalogue(result)

    @staticmethod
    def _time_seriese_of_individual_star(otsp, s):
        t = []
        londata = []
        latdata = []
        for o in otsp:
            tmpt, tmplon, tmplat = AstrometricCatalogueBuilder._add_individual_observation(o, s)
            t.extend(tmpt)
            londata.extend(tmplon)
            latdata.extend(tmplat)
        return latdata, londata, t

    @staticmethod
    def _add_individual_observation(o, s):
        tmpt = []
        tmplon = []
        tmplat = []
        for ss in o.positions_on_the_sky:
            if s == ss.stellar_id:
                tmpt.append(ss.datetime)
                tmplon.append(ss.coord.barycentricmeanecliptic.lon.rad)
                tmplat.append(ss.coord.barycentricmeanecliptic.lat.rad)
        return tmpt, tmplon, tmplat
