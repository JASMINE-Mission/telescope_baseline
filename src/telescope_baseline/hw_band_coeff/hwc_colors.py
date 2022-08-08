
import numpy as np
import glob
from scipy import interpolate
from multiprocessing import Pool

import os

import pkgutil
from io import BytesIO

#-- load spectra files here
def load_spectra(file_path):
    """load spectra files

    Args:
        path to dir including spectra files

    Returns:
        loaded spectral data
    """
    return np.loadtxt(file_path, comments='#', dtype='f8').T

def loadspec_map_multi(dir_spectra=None):
    """function for multiprocessing of load_spectra

    Args:
        dir including spectral files

    Returns:
        spectral data in array
    """
    if (dir_spectra is None):
        ds = pkgutil.get_data('telescope_baseline', 'data/spectra')
        dir_spectra     = BytesIO(ds)

    spectra_files = sorted(glob.glob(dir_spectra+"/*"))
    p   = Pool(os.cpu_count())
    data_spec   = p.map(load_spectra, spectra_files) # map で並列読み込み
    p.close()
    return data_spec


def cal_photon(input_arrays):
    """calculate photon counts for each filter and spectra

    Args:
        list including (stellar spectra, filter function,
        and extinction factor (Av))

    Returns:
        relative photon counts
    """
    spectra_array,filter_func,Av    = input_arrays

    ff  = interpolate.interp1d(x=filter_func[1],\
                               y=filter_func[2],kind="cubic")

    spec_narrow     = spectra_array[:,((filter_func[1,0]<spectra_array[0])&\
                                       (spectra_array[0]<filter_func[1,-1]))]

    transmit_f  = ff(spec_narrow[0])*spec_narrow[1] #transmitted flux
    dx          = np.diff(spec_narrow[0])

    extinction  =  10** (-1*A_lambda(Av, spec_narrow[0,:-1])/2.5)
    photon      = np.sum(transmit_f[:-1] * dx * spec_narrow[0,:-1] * extinction)

    return photon

def calphoton_map_multi(data_spec, filter_func, Av):
    """function for multiprocessing of cal_photon

    Args:
        data_spec   : (multiple) spectral data in array
        filter_func : filter function
        Av          : extinction factor

    Returns:
        relative photon counts in array
    """
    data_array  = [(x,filter_func,Av) for x in data_spec]
    xlen    = len(filter_func)
    ylen    = len(data_spec)

    p   = Pool(os.cpu_count())

    data_photon = p.map(cal_photon, data_array)
    p.close()
    data_photon = np.array(data_photon, dtype='f8')

    return data_photon

def load_filter(fl_J=None, fl_H=None):
    """load filter functions

    Args:
        fl_J    : path to Jband filter dat file
        fl_H    : path to Hband filter dat file

        * wavelength and filter efficiency must be
          set in 2nd and 3rd columns,respectively.
          wavelength must be expressed in micron unit.

    Returns:
        fltJ    : J band filter func
        fltH    : H band filter func
    """
    #fl_J    = "./filter/J_filter.dat"
    #fl_H    = "./filter/H_filter.dat"

    if (fl_J is None):
        fj  = pkgutil.get_data('telescope_baseline', 'data/filter/J_filter.dat')
        fl_J    = BytesIO(fj)
    if (fl_H is None):
        fh  = pkgutil.get_data('telescope_baseline', 'data/filter/H_filter.dat')
        fl_H    = BytesIO(fh)

    fltJ    = np.loadtxt(fl_J, comments="#", dtype='f8').T
    fltH    = np.loadtxt(fl_H, comments="#", dtype='f8').T
    fltJ[1] = fltJ[1]*1e4 #mic -> angstrom
    fltH[1] = fltH[1]*1e4

    return fltJ,fltH

def Hw_func(lower, upper):
    """Hw band with box function

    Args:
        lower: lower limit of filter wavelength (in angstrom)
        upper: upper limit of filter wavelength (in angstrom)

    Returns:
        filter function with box

    """
    lw  = lower #angstrom
    up  = upper #
    nd  = 150 #number of data

    x   = np.linspace(lw-1000, up+1000, nd)
    y   = np.where((lw <= x)&(x <= up),1.,0.)
    index   = np.linspace(1,nd,nd)
    Hw  = np.array((index,x,y))

    return Hw

def A_lambda(Av, x):
    """extinction value in a given wavelength (angstrom)

    Args:
        Av  : Extinction in V-band
        x   : wavelength (angstrom)

    Returns:
        extinction val in a given wavelength

    """
    Ak_Av   = 0.112
    Ak      = Ak_Av*Av
    coeff   = 5.2106*(x**(-2.112))

    return coeff*Ak


def A_lambda_linear(Av, x):
    """extinction value in a given wavelength (angstrom)

    Args:
        Av  : Extinction in V-band
        x   : wavelength (angstrom)

    Returns:
        extinction val in a given wavelength

    """
    Aj_Av   = 0.282
    Ak_Av   = 0.112

    Aj  = Aj_Av*Av
    Ak  = Ak_Av*Av

    return ((x-12000)*Ak + (20000-x)*Aj)/(20000 - 12000)


def load_specA0V(spec_a0v=None):
    """load spectral data of A0V star

    Args:
        file path

    Returns:
        spectral data

    """
    if (spec_a0v is None):
        sa  = pkgutil.get_data('telescope_baseline', 'data/spectra/uka0v.dat')
        spec_a0v    = BytesIO(sa)
    spectra     = np.loadtxt(spec_a0v, comments='#', dtype='f8').T
    return spectra


def cal_colordata(dir_spec, J_filter, H_filter, Hw_l, Hw_u, Av_ar):
    """calculate color data points (Hw-H) and (J-H)

    Args:
        dir_spec:   dir including spectral data
        J_filter:   file of J-band filter function
        H_filter:   file of H-band filter function
        Hw_l:       lower wavelength limit of Hw
        Hw_u:       upper wavelength limit of Hw
        Av_ar:      extinction factor in V-band

    Returns:
        list of colors (Hw-H) and (J-H) in dictionary type
    """

    # load spectra file names
    data_spec   = loadspec_map_multi(dir_spec)

    # set range of Hw band
    fil_Hw  = Hw_func(Hw_l, Hw_u) #

    # zero magnitude spectra
    spec_a0v    = load_specA0V(dir_spec+'/uka0v.dat')
    fil_J,fil_H = load_filter(J_filter, H_filter)

    p_Jo    = cal_photon([spec_a0v, fil_J, 0])
    p_Ho    = cal_photon([spec_a0v, fil_H, 0])
    p_Hwo   = cal_photon([spec_a0v, fil_Hw, 0])


    lst_Hw_H     = []
    lst_J_H      = []
    for Av in Av_ar: # -- roop for Av
        p_J     = calphoton_map_multi(data_spec, fil_J, Av)
        p_H     = calphoton_map_multi(data_spec, fil_H, Av)
        p_Hw    = calphoton_map_multi(data_spec, fil_Hw, Av)

        rel_J   = -2.5*(np.log10(p_J) - np.log10(p_Jo))
        rel_H   = -2.5*(np.log10(p_H) - np.log10(p_Ho))
        rel_Hw  = -2.5*(np.log10(p_Hw) - np.log10(p_Hwo))

        J_H     = rel_J  - rel_H
        Hw_H    = rel_Hw - rel_H

        lst_Hw_H.append(Hw_H)
        lst_J_H.append(J_H)

    result  = {"Hw-H": lst_Hw_H,
               "J-H": lst_J_H}

    return  result
