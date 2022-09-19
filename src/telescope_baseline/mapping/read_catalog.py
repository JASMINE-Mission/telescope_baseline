import numpy as np
import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord


def read_jasmine_targets(hdffile):
    """Read JASMINE catalog

        Args:
            hdffile: HDF (ra,dec, ...)

        Returns:
            targets coordinate list (in radian), l in deg, b in deg, Hw


        Notes:
            HDF file can be generated using jasmine_catalog, for instance, by the following example.

        Examples:

            >>> import psycopg2 as sql
            >>> import pandas as pd
            >>> login = {
            >>> 'host': 'localhost',
            >>> 'port': 15432,
            >>> 'database': 'jasmine',
            >>> 'user': 'jasmine',
            >>> 'password': 'jasmine',
            >>> }
            >>> query = "SELECT ra, dec, phot_hw_mag FROM merged_sources WHERE phot_hw_mag < 12.5;"
            >>> connection = sql.connect(**login)
            >>> dat = pd.read_sql(sql=query, con=connection)
            >>> dat.to_hdf("cat.hdf", 'key', mode='w', complevel=5)

    """

    dat = pd.read_hdf(hdffile)
    ra = dat["ra"].values
    dec = dat["dec"].values
    hw = dat["phot_hw_mag"].values
    c = SkyCoord(ra=ra * u.degree, dec=dec * u.degree, frame='icrs')
    phi = c.galactic.l.radian
    theta = np.pi / 2.0 - c.galactic.b.radian
    l = c.galactic.l.degree
    b = c.galactic.b.degree
    l[l > 180] = l[l > 180] - 360
    return np.array([theta, phi]), l, b, hw


def read_jasmine_targets_jhk(hdffile):
    """Read JASMINE catalog

        Args:
            hdffile: HDF (ra,dec, J, H, K)

        Returns:
            targets coordinate list (in radian), l in deg, b in deg, J, H, K mag

        Notes:
            HDF file can be generated using jasmine_catalog, for instance, by the following example, using the Hw definition (as of 10/09/2022) Hw = 0.9J+0.1H-0.06(J-H)^2

        Examples:

            >>> import psycopg2 as sql
            >>> import pandas as pd
            >>> login = {
            >>> 'host': 'localhost',
            >>> 'port': 15432,
            >>> 'database': 'jasmine',
            >>> 'user': 'jasmine',
            >>> 'password': 'jasmine',
            >>> }
            >>> query = "SELECT ra, dec, SELECT ra, dec, phot_j_mag, phot_h_mag, phot_k_mag FROM merged_sources WHERE (0.9*phot_j_mag+0.1*phot_h_mag-0.06*((phot_j_mag-phot_h_mag)**2) < 12.5) AND (glon BETWEEN -2.0 AND 1.3) AND (glat BETWEEN -1.2 AND 1.2);"
            >>> connection = sql.connect(**login)
            >>> dat = pd.read_sql(sql=query, con=connection)
            >>> dat.to_hdf("cat.hdf", 'key', mode='w', complevel=5)

            or use telescope_baseline/src/telescope_baseline/data/sql_cat_jhk_hw125.py

    """

    dat = pd.read_hdf(hdffile)
    ra = dat["ra"].values
    dec = dat["dec"].values
    jmag = dat["phot_j_mag"].values
    hmag = dat["phot_h_mag"].values
    ksmag = dat["phot_ks_mag"].values
    c = SkyCoord(ra=ra * u.degree, dec=dec * u.degree, frame='icrs')
    phi = c.galactic.l.radian
    theta = np.pi / 2.0 - c.galactic.b.radian
    l = c.galactic.l.degree
    b = c.galactic.b.degree
    l[l > 180] = l[l > 180] - 360
    return np.array([theta, phi]), l, b, jmag, hmag, ksmag
