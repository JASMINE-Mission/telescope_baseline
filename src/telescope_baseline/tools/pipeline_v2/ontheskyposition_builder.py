import math
from astropy.coordinates import get_sun, SkyCoord
from astropy.time import Time
from telescope_baseline.tools.pipeline_v2.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline_v2.ontheskyposition import OnTheSkyPosition
from telescope_baseline.tools.pipeline_v2.skyposition import SkyPosition
from telescope_baseline.tools.pipeline_v2.stella_image import StellarImage


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


class OnTheSkyPositionBuilder:
    def __init__(self):
        pass

    def from_astrometric_catalogue_2_list(self, a: AstrometricCatalogue, t: list[Time]) -> list[OnTheSkyPosition]:
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
                sky_positions.append(SkyPosition(i, j, coord, c.mag, time))
            osp0 = OnTheSkyPosition(sky_positions, j)
            osp.append(osp0)
        return osp

    def from_stellar_image(self, sttelar_image: StellarImage) -> OnTheSkyPosition:
        skypositions = sttelar_image.get_sky_positions()
        return OnTheSkyPosition(skypositions)

