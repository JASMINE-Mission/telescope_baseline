"""pixelfunc Borrowed from Healpy GPL-2.0 license, https://github.com/healpy/

"""
import numpy as np
def lonlat2thetaphi(lon, lat):
    """Transform longitude and latitude (deg) into co-latitude and longitude (rad)
    Args:
        lon : int or array-like. Longitude in degrees
        lat : int or array-like, Latitude in degrees
    Returns:
        theta, phi : float, scalar or array-like, The co-latitude and longitude in radians
    """
    return np.pi / 2.0 - np.radians(lat), np.radians(lon)


def thetaphi2lonlat(theta, phi):
    """Transform co-latitude and longitude (rad) into longitude and latitude (deg)
    Args:
        theta : int or array-like, Co-latitude in radians
        phi : int or array-like, Longitude in radians
    Returns:
        lon, lat : float, scalar or array-like, The longitude and latitude in degrees
    """
    return np.degrees(phi), 90.0 - np.degrees(theta)

def vec2ang(vectors, lonlat=False):
    """vec2ang: vectors [x, y, z] -> theta[rad], phi[rad], Borrowed from Healpy GPL-2.0 license, https://github.com/healpy/
    Args:
        vectors : float, array-like
          the vector(s) to convert, shape is (3,) or (N, 3)
        lonlat : bool, optional, If True, return angles will be longitude and latitude in degree, otherwise, angles will be co-latitude and longitude in radians (default)
    Returns:
        theta, phi : float, tuple of two arrays. the co-latitude and longitude in radians
    """
    vectors = vectors.reshape(-1, 3)
    dnorm = np.sqrt(np.sum(np.square(vectors), axis=1))
    theta = np.arccos(vectors[:, 2] / dnorm)
    phi = np.arctan2(vectors[:, 1], vectors[:, 0])
    phi[phi < 0] += 2 * np.pi
    if lonlat:
        return thetaphi2lonlat(theta, phi)
    else:
        return theta, phi

def ang2vec(theta, phi, lonlat=False):
    """ang2vec : convert angles to 3D position vector, Borrowed from Healpy GPL-2.0 license, https://github.com/healpy/
    Args:
        theta : float, scalar or arry-like, co-latitude in radians measured southward from north pole (in [0,pi]).
        phi : float, scalar or array-like. longitude in radians measured eastward (in [0, 2*pi]).
        lonlat : bool, If True, input angles are assumed to be longitude and latitude in degree, otherwise, they are co-latitude and longitude in radians.
    Returns:
        vec : float, array, if theta and phi are vectors, the result is a 2D array with a vector per row otherwise, it is a 1D array of shape (3,)
    """
    if lonlat:
        theta, phi = lonlat2thetaphi(theta, phi)
    check_theta_valid(theta)
    sintheta = np.sin(theta)
    return np.array([sintheta * np.cos(phi), sintheta * np.sin(phi), np.cos(theta)]).T

def check_theta_valid(theta):
    """Raises exception if theta is not within 0 and pi"""
    theta = np.asarray(theta)
    if not ((theta >= 0).all() and (theta <= np.pi + 1e-5).all()):
        raise ValueError("THETA is out of range [0,pi]: theta="+str(theta))
