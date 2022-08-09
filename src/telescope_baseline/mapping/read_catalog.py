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
        
    dat=pd.read_hdf(hdffile)
    ra=dat["ra"].values
    dec=dat["dec"].values
    hw=dat["phot_hw_mag"].values
    c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
    phi=c.galactic.l.radian
    theta=np.pi/2.0-c.galactic.b.radian
    l=c.galactic.l.degree
    b=c.galactic.b.degree
    l[l>180]=l[l>180]-360
    return np.array([theta,phi]),l,b, hw


