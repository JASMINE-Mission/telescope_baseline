import numpy as np
from io import StringIO
import pandas as pd
from astropy import constants as const
from astropy import units as u
import pkgutil
from io import BytesIO


def get_magdict(maglist=None):
    """get magnitude information list

    Args:
       external magnitude information list (optional)

    Returns:
       infromation table of maglist

    """
    magdict = {}
    if maglist is None:
        mn = pkgutil.get_data('telescope_baseline', 'data/mag.list')
        maglist = pd.read_csv(BytesIO(mn), delimiter=',')
    return maglist


def get_flux(band, mag, magdict):
    """compute flux (per-wavelength form, f_lambda) from mag

    Args:
       band: band symbol (J,H, etc..)
       mag: magnitude
       maglist: infromation table of maglist

    Returns:
       flux (per-wavelength form, f_lambda) with the unit of astropy

    """

    mask = magdict['band'] == band
    a = float(magdict['a'][mask].values[0])
    flux = 10**(a - 0.4*mag)*u.erg/u.s/(u.cm)**2/u.micron
    return flux


def get_mag(band, flux, magdict):
    """compute mag from flux (per-wavelength form, f_lambda)

    Args:
       band: band symbol (J,H, etc..)
       flux: flux (per-wavelength form, f_lambda) with the unit of astropy
       maglist: infromation table of maglist

    Returns:
       mag: magnitude

    """
    mask = magdict['band'] == band
    a = float(magdict['a'][mask].values[0])
    fluxcgs = flux.to(u.erg/u.s/(u.cm)**2/u.micron).value
    mag = 2.5*(a - np.log10(fluxcgs))

    return mag
