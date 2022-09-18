import math
from astropy.coordinates import get_sun, SkyCoord
from astropy.time import Time
from astropy.wcs import WCS

from telescope_baseline.tools.pipeline.astrometric_catalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.map_on_the_sky import MapOnTheSky
from telescope_baseline.tools.pipeline.position_on_the_sky import PositionOnTheSky
from telescope_baseline.tools.pipeline.map_on_detector import MapOnDetector


def position_at_certain_time(coord: SkyCoord, t: Time):
    lat0 = coord.barycentricmeanecliptic.lat.rad
    lon0 = coord.barycentricmeanecliptic.lon.rad
    # TODO: unit of distance and proper motion is assumed to be 'pc' and 'mas/yr' respectively.  It should be checked.
    para = 1 / coord.distance.value * 4.848136e-6  # const is conversion ratio from as to rad.
    pm_lon_coslat = coord.barycentricmeanecliptic.pm_lon_coslat.value * 4.848136e-9
    pm_lat = coord.barycentricmeanecliptic.pm_lat.value * 4.848136e-9
    ls = get_sun(t).geocentricmeanecliptic.lon.rad
    ty = t.jyear - coord.obstime.jyear
    lont = lon0 + (para * math.sin(ls - lon0) + pm_lon_coslat * ty) / math.cos(lat0)
    latt = lat0 + (pm_lat * ty - para * math.sin(lat0) * math.cos(ls - lon0))
    return lont, latt


class MapOnTheSkyBuilder:
    """Builder class for OnTheSkyPosition

    """
    def __init__(self, wcs: WCS):
        self.__wcs = wcs

    def get_sky_positions(self, mod: MapOnDetector):
        ret = []
        for position in mod.positions_on_detector:
            sky = self.__wcs.pixel_to_world(position.x, position.y)
            # TODO: Consideration is needed how ids are set.
            ret.append(PositionOnTheSky(position.exposure_id, sky, position.mag, position.datetime))
        return ret

    def from_astrometric_catalogue_2_list(self, a: AstrometricCatalogue, t: list[Time]) -> list[MapOnTheSky]:
        """method for build from AstrometricCatalogue to the list of OnTheSkyPosition

        Args:
            a: AstrometricCatalogue
            t: list of Time

        Returns:

        """
        catalogue = a.get_catalogue()
        n = len(t)
        osp = []
        for j in range(n):
            time = t[j]
            sky_positions = []
            for i in range(len(catalogue)):
                c = catalogue[i]
                l, b = position_at_certain_time(c.coord, time)
                coord = SkyCoord(lat=b, lon=l, unit=('rad', 'rad'), frame='barycentricmeanecliptic')
                sky_positions.append(PositionOnTheSky(i, coord, c.mag, time))  # index i is needed here
            osp0 = MapOnTheSky(j, sky_positions)  # index j is needed here
            osp.append(osp0)
        return osp

    def from_map_on_detector(self, map_on_detector_list: list[MapOnDetector]) -> MapOnTheSky:
        """method for build from StellarImage(detector coordinate) class to OnTheSkyPosition

        Args:
            map_on_detector_list:

        Returns:

        """
        skypositions = []
        for si in map_on_detector_list:
            skypositions.extend(self.get_sky_positions(si))
        # TODO Get the ID of the star and optimize the SIP for the same star at the same position in the sky.
        return MapOnTheSky(positions_on_the_sky=skypositions)
