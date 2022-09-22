

# sql_cat_jhk.py
# script to get the JASMINE catalogue from Kyoto U. server obd.

import psycopg2 as sql
import pandas as pd

login = {
    'host': 'localhost',
    'port': 15432,
    'database': 'jasmine',
    'user': 'jasmine',
    'password': 'jasmine',
}
query = """
    SELECT ra, dec, phot_j_mag, phot_h_mag, phot_ks_mag, glon, glat
    FROM merged_sources
    WHERE ((0.9*phot_j_mag+0.1*phot_h_mag-0.06*(POWER(phot_j_mag-phot_h_mag,2)))
           < 12.5)
    AND (glon BETWEEN -2.0 AND 2.0)
    AND (glat BETWEEN -1.2 AND 1.2);
"""
connection = sql.connect(**login)
dat = pd.read_sql(sql=query, con=connection)
print(dat)
dat.to_hdf("cat_jhk_hw12.5.hdf", 'key', mode='w', complevel=5)
