from astropy.io import fits

from telescope_baseline.tools.pipeline_v2.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline_v2.detectorimagecatalogue import DetectorImageCatalogue
from telescope_baseline.tools.pipeline_v2.ondetectorposition import OnDetectorPosition
from telescope_baseline.tools.pipeline_v2.ontheskyposition import OnTheSkyPosition
from telescope_baseline.tools.pipeline_v2.skyposition import SkyPosition
from telescope_baseline.tools.pipeline_v2.stellaimage import StellarImage
from astropy.wcs import WCS
import numpy as np
from scipy import optimize
from astropy.coordinates import get_sun, SkyCoord
import math
from astropy.time import Time

from telescope_baseline.tools.pipeline_v2.wcswid import WCSwId


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


class Pipeline:
    def simulation(self, a: AstrometricCatalogue, t: list[Time], wlist: list[WCSwId], pix_max: int, psf_w: float)\
            -> DetectorImageCatalogue:
        otsps = self._simulation_astrometric_catalogue_2_on_the_sky_position(a, t)

        sii = []
        for i in range(len(otsps)):
            otsp = otsps[i]
            si = self._simulation_on_the_sky_position_2_stellar_images(i, otsp, pix_max, wlist)
            sii.append(si)
        # sii[orbit][exposure]: StellarImage
        for i in range(len(sii)):
            for j in range(len(sii[i])):
                dp = sii[i][j].detector_posotions
                a = np.random.uniform(0.0, 10.0, (pix_max, pix_max))
                for s in range(len(dp)):
                    for k in range(int(dp[s].mag)):
                        xp = int(psf_w * np.random.randn() + dp[s].y + 0.5)
                        yp = int(psf_w * np.random.randn() + dp[s].x + 0.5)
                        if 0 <= xp < pix_max and 0 <= yp < pix_max:
                            a[xp][yp] += 1
                hdu = fits.PrimaryHDU()
                hdu.data = a
                hdu.writeto("tmp" + str(i) + "_" + str(j) + ".fits", overwrite=True)
        return DetectorImageCatalogue()

    def _simulation_on_the_sky_position_2_stellar_images(self, i, otsp, pix_max, wlist):
        sky_positions = otsp.sky_positions
        wl = []
        for j in range(len(wlist)):
            if wlist[j].orbit_id == i:
                wl.append(wlist[j])
        si = []
        if len(wl) > 0:
            for j in range(len(wl)):
                if "GLON" not in wl[j].wcs.wcs.ctype[0]:
                    print("Coordinate system " + wl[j].wcs.wcs.ctype[0] + " is not supported")
                    raise ValueError
                tmp = []
                for k in range(len(sky_positions)):
                    tmp.append([sky_positions[k].coord.galactic.l.deg, sky_positions[j].coord.galactic.b.deg])
                tmp = wl[j].wcs.wcs_world2pix(tmp, 0)
                a = []
                for k in range(len(tmp)):
                    print(tmp[k])
                    if not (tmp[k][0] < 0 or tmp[k][1] < 0 or tmp[k][0] > pix_max or tmp[k][1] > pix_max):
                        a.append(OnDetectorPosition(k, tmp[k][0], tmp[k][1], 3000, sky_positions[0].datetime))
                si.append(StellarImage(wl[j].wcs, window_size=9, detector_positions=a))
        return si

    def _simulation_astrometric_catalogue_2_on_the_sky_position(self, a: AstrometricCatalogue, t: list[Time])\
            -> list[OnTheSkyPosition]:
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
            osp.append(OnTheSkyPosition(sky_positions))
        return osp

    def analysis(self, c: DetectorImageCatalogue, wcs: WCS, window_size: int = 9) -> AstrometricCatalogue:
        # TODO: wcs is not constant whole the mission.
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
        result = optimize.leastsq(lsf_fit_function_for_astrometric_parameters, parameter, args=(t, londata, latdata))
        return AstrometricCatalogue(result)

    def _analysis_sttelar_image_2_on_the_sky_position(self, sttelar_image):
        skypositions = sttelar_image.get_sky_positions()
        otsp = OnTheSkyPosition(skypositions)
        return otsp

    def _analysys_detecotr_catalog_2_stellar_image(self, c, wcs, window_size):
        position_list = []
        for di in c.get_detector_images():
            position_list.extend(di.get_on_detector_positions(window_size))
        return StellarImage(wcs, window_size, position_list)
