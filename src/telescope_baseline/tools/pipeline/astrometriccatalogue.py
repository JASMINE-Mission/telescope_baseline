import math

import numpy as np
from astropy.coordinates import get_sun
from scipy import optimize

from telescope_baseline.tools.pipeline.simnode import SimNode
from telescope_baseline.tools.pipeline.catalogue_entry import CatalogueEntry
import astropy.units as u


def fit_astrometry(parameter, ty, ls, lon, lat):
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
    lont = np.ndarray((len(ty)))
    latt = np.ndarray((len(ty)))
    residual = np.ndarray((len(ty)))
    for i in range(len(ty)):
        lont[i] = lon0 + (para * math.sin(ls[i] - lon0) + pm_lon_coslat * ty[i]) / math.cos(lat0)
        latt[i] = lat0 + (pm_lat * ty[i] - para * math.sin(lat0) * math.cos(ls[i] - lon0))
        residual[i] = (lon[i] - lont[i]) ** 2 + (lat[i] - latt[i]) ** 2
    return residual


class AstrometricCatalogue(SimNode):
    """AstrometricCatalogue class is the correction class of CatalogueEntry.

    The constructor is default constructor. After instantiate the class, entry is added by add_entry(c) method. The
     variable c is the CatalogueEntry object.

    Attributes:
        __catalogue: array of CatalogueEntry object.
        __result: It is needed for pass the result from calculate_ap_parameter to get_result

    """
    def __init__(self):
        super().__init__()
        self.__catalogue = []
        self.__result = []

    def accept(self, v):
        v.visit(self)

    def add_entry(self, c: CatalogueEntry):
        """add catalogue entry to the AstrometricCatalogue object.

        Args:
            c: CatalogueEntry object

        Returns:Non

        """
        self.__catalogue.append(c)

    def get_list(self):
        """

        Returns:The array of CatalogueEntry object.

        """
        return self.__catalogue

    def calculate_ap_parameters(self):
        """calculate astrometric parameter from child OnTheSkyPosition objects.

        Returns: Non
            result is saved to the attribute __result

        TODO: check stellar id, gather the input for leastsq function for the same array.
            Now the function assumes only one stars in child object and these are for the same stars.

        """
        t = []
        londata = []
        latdata = []
        ls = []
        ty = []
        for i in range(self.get_child_size()):
            c = self.get_child(i)
            t.append(c.get_time())
            londata.append(self.get_child(i).get_coord(0).barycentricmeanecliptic.lon.rad)
            latdata.append(self.get_child(i).get_coord(0).barycentricmeanecliptic.lat.rad)
            ls.append(get_sun(t[i]).geocentricmeanecliptic.lon.rad)
            ty.append(t[i].jyear)
        ls = np.array(ls)
        ty = np.array(ty)
        tc = (np.max(ty) + np.min(ty)) / 2
        ty = ty - tc
        parameter = [np.radians(266), np.radians(-5), 0., 0., np.radians(1 / 3600)]
        self.__result = optimize.leastsq(fit_astrometry, parameter, args=(ty, ls, londata, latdata))

    def get_parameters(self):
        """

        Returns: parameter array for 0th star.
        TODO: Need to handle multiple stars.

        """
        return self.__result

    def save(self, filename):
        """The method for save the catalogue to the file.

        Args:
            filename: The name of the file for saving data.

        Returns: Non

        """
        f = open(filename, 'w')
        for i in range(len(self.__catalogue)):
            f.write(str(self.__catalogue[i].id) + "," + str(self.__catalogue[i].ra) + "," +
                    str(self.__catalogue[i].dec) + "," + str(self.__catalogue[i].parallax / u.mas) + "," +
                    str(self.__catalogue[i].pm_ra * u.yr / u.mas) + "," +
                    str(self.__catalogue[i].pm_dec * u.yr / u.mas) + "\n")
        f.close()
