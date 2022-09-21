import array
import math

import numpy as np
from astropy.coordinates import get_sun
from astropy.time import core
from scipy import optimize

from telescope_baseline.tools.pipeline.astrometric_catalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.map_on_the_sky import MapOnTheSky


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
    solar_longitude = get_sun(core.Time(t)).geocentricmeanecliptic.lon.rad
    time_julian_year = core.Time(t).jyear
    time_center = (np.max(time_julian_year) + np.min(time_julian_year)) / 2
    time_julian_year = time_julian_year - time_center
    lont = lon0 + (para * np.sin(solar_longitude - lon0) + pm_lon_coslat * time_julian_year) / np.cos(lat0)
    latt = lat0 + (pm_lat * time_julian_year - para * np.sin(lat0) * np.cos(solar_longitude - lon0))
    residual = (lon - lont) ** 2 + (lat - latt) ** 2
    return residual


class AstrometricCatalogueBuilder:
    """Builer class for AstrometricCatalogue

    """
    def __init__(self):
        pass

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
    def from_on_the_sky_position(otsp: list[MapOnTheSky]):
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
