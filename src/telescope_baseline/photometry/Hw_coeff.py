#!/usr/bin/env python

import numpy as np
import sys
from matplotlib import pyplot as plt
import glob
import pandas as pd
import os
from multiprocessing import Pool
from astropy import units as u
import pkgutil
import pkg_resources
from io import BytesIO
from scipy import interpolate
from scipy.optimize import minimize


def load_stellar_spectra(file_path):
    """Load stellar spectra.

    Args:
       file_path: path to the spectrum file

    Returns:
       spectral data
    """
    ascii_data = pkgutil.get_data(
        'telescope_baseline', 'data/spectra/'+file_path)
    return np.loadtxt(BytesIO(ascii_data), comments='#', dtype='f8').T


def read_map_multi(spectra_all):
    """Read multiple spectra in parallel.

    Args:
        all spectral info

    Returns:
        spectral data
    """
    p = Pool(os.cpu_count())
    data_spec = p.map(load_stellar_spectra, spectra_all)
    p.close()
    return data_spec


def cal_photon(input_arrays):
    """compute photons.

    Args:
        input_array:

    Returns:
        photon count?
    """
    # 1.透過関数をsplineで関数化.
    # 2.透過関数とFluxを波長を乗じて積分し、光子数に換算.
    # 3.最終的に比の計算を行うため、各係数は無視.
    spectra_array, filter_func, Av = input_arrays

    ff = interpolate.interp1d(x=filter_func[1],
                              y=filter_func[2], kind='cubic')

    spec_narrow = spectra_array[:, ((filter_func[1, 0] < spectra_array[0]) &
                                    (spectra_array[0] < filter_func[1, -1]))]

    transmit_f = ff(spec_narrow[0])*spec_narrow[1]  # transmitted flux
    dx = np.diff(spec_narrow[0])

    extinction = 10 ** (-1*A_lambda(Av, spec_narrow[0, :-1])/2.5)
    photon = np.sum(transmit_f[:-1] * dx * spec_narrow[0, :-1] * extinction)

    return photon


def calphoton_map_multi(data_spec, filter_func, Av):
    """compute photon for multiple dataset.

    Args:
        data_spec:
        filter_func:
        Av:

    Returns:
        photon?
    """

    data_array = [(x, filter_func, Av) for x in data_spec]
    xlen = len(filter_func)
    ylen = len(data_spec)

    p = Pool(os.cpu_count())

    data_photon = p.map(cal_photon, data_array)
    p.close()
    data_photon = np.array(data_photon, dtype='f8')

    return data_photon


def load_filter():
    """Load filters.

    Returns:
        Jband filter
        Hbandfilter
    """

    fl_J = pkgutil.get_data('telescope_baseline', 'data/filter/J_filter.dat')
    fl_H = pkgutil.get_data('telescope_baseline', 'data/filter/H_filter.dat')
    fltJ = np.loadtxt(BytesIO(fl_J), comments='#', dtype='f8').T
    fltH = np.loadtxt(BytesIO(fl_H), comments='#', dtype='f8').T
    fltJ[1] = fltJ[1]*1e4  # mic -> angstrom
    fltH[1] = fltH[1]*1e4

    return fltJ, fltH


def set_range_Hw_band(lower, upper):
    """set range of Hw band

    Args:
        lower: lower wavelength in the unit of angstrom
        upper: upper wavelength in the unit of angstrom

    Returns:
        Hw
    """

    lw = lower
    up = upper
    nd = 150  # number of data
    x = np.linspace(lw-1000, up+1000, nd)
    y = np.where((lw <= x) & (x <= up), 1., 0.)
    index = np.linspace(1, nd, nd)
    Hw = np.array((index, x, y))

    return Hw


def A_lambda(Av, x):
    """calculate A lambda.

    Args:
        Av: Av
        x: x

    Returns:
        A_lambda

    """
    Ak_Av   = 0.112
    Ak      = Ak_Av*Av
    x_um    = x*1e-4
    coeff   = 5.2106*(x_um**(-2.112))

    return coeff*Ak

def A_lambda_linear(Av, x):
    """calculate A lambda with linear law.

    Args:
        Av: Av
        x: x

    Returns:
        A_lambda

    """
    Aj_Av = 0.282
    Ak_Av = 0.112

    Aj = Aj_Av*Av
    Ak = Ak_Av*Av

    return ((x-12000)*Ak + (20000-x)*Aj)/(20000 - 12000)


def quad_func(x, args):
    a = args[0]
    b = args[1]
    return a*x**2 + b*x


def least_sq(coeff, *args):
    x, y = args
    chi2 = np.sum(np.square(quad_func(x, coeff)-y))**0.5
    return chi2


def read_spectra_all():
    """Read all stellar spectra

    Returns:
        all spectra

    """
    speclist = pkg_resources.resource_filename('telescope_baseline', 'data/speclist.txt')
    f = open(speclist, "r")
    spectra_all = f.readlines()
    f.close()
    spectra_all = [s.replace('\n', '') for s in spectra_all]
    return spectra_all


def calc_zero_magnitude_spectra(fil_J, fil_H, fil_Hw):
    """zero magnitude spectra

    Args:
        fil_J:
        fil_H:
        fil_Hw:

    Returns:
        zero magnitude of J?
        zero magnitude of H?
        zero magnitude of Hw?

    """

    uka0v = pkgutil.get_data('telescope_baseline', 'data//spectra/uka0v.dat')
    spec_a0v = np.loadtxt(BytesIO(uka0v), comments='#', dtype='f8').T
    p_Jo = cal_photon([spec_a0v, fil_J, 0])
    p_Ho = cal_photon([spec_a0v, fil_H, 0])
    p_Hwo = cal_photon([spec_a0v, fil_Hw, 0])
    return p_Jo, p_Ho, p_Hwo


def calc_color_arrays(data_spec, fil_J, fil_H, fil_Hw, p_Jo, p_Ho, p_Hwo):
    """compute colors

    Args:
        data_spec:
        fil_J:
        fil_H:
        fil_Hw:
        p_Jo: zero magnitude of J?
        p_Ho:  zero magnitude of H?
        p_Hwo:  zero magnitude of Hw?

    Returns:
        ar_J_H: J-H array
        ar_Hw_H: Hw-H array
        Av array used

    """
    Av_ar = np.linspace(0, 60, 5)
    ar_Hw_H = []
    ar_J_H = []
    A_arr = []
    for Av in Av_ar:  # -- roop for Av
        p_J = calphoton_map_multi(data_spec, fil_J, Av)
        p_H = calphoton_map_multi(data_spec, fil_H, Av)
        p_Hw = calphoton_map_multi(data_spec, fil_Hw, Av)

        rel_J = -2.5*(np.log10(p_J) - np.log10(p_Jo))
        rel_H = -2.5*(np.log10(p_H) - np.log10(p_Ho))
        rel_Hw = -2.5*(np.log10(p_Hw) - np.log10(p_Hwo))

        J_H = rel_J - rel_H
        Hw_H = rel_Hw - rel_H

        ar_Hw_H.append(Hw_H)
        ar_J_H.append(J_H)
        A_arr.append(Av)

    return ar_J_H, ar_Hw_H, A_arr


def calc_colors(ar_J_H, ar_Hw_H):
    """
    Args:
       ar_J_H: J-H array
       ar_Hw_H: Hw-H array

    Returns:
       colors
    """
    return (np.ravel(np.array(ar_J_H)), np.ravel(np.array(ar_Hw_H)))


def compute_Hw_relation(Hw_l, Hw_u):
    """compute Hw - (H, J-H) relation

    Args:
       Hw_l: lower limit of passband in angstrom
       Hw_u: upper limit of passband in angstrom

    Returns:
       minimize instance
       sigma
       colors
       J-H array
       Hw-H array
       fitting residuals
    """
    return _compute_Hw_relation(Hw_l, Hw_u, read_spectra_all())


def _compute_Hw_relation(Hw_l, Hw_u, spectra_all):
    data_spec = read_map_multi(spectra_all)
    fil_Hw = set_range_Hw_band(Hw_l, Hw_u)
    fil_J, fil_H = load_filter()
    p_Jo, p_Ho, p_Hwo = calc_zero_magnitude_spectra(fil_J, fil_H, fil_Hw)
    ar_J_H, ar_Hw_H, Av_arr = calc_color_arrays(data_spec, fil_J, fil_H, fil_Hw, p_Jo, p_Ho, p_Hwo)
    colors = calc_colors(ar_J_H, ar_Hw_H)
    x0 = [1., 0.8]
    res = minimize(least_sq, x0, args=colors, method='Nelder-Mead', tol=1e-11)
    residuals = colors[1] - quad_func(colors[0], res.x)
    sigma = np.std(residuals)
    result = {'x0': res.x[0],
              'x1': res.x[1],
              'std': sigma,
              'chi2': res.fun}
    print(result)
    return res, sigma, colors, ar_J_H, ar_Hw_H, residuals


def plot_Hwfit(Hw_l, Hw_u, res, sigma, colors, ar_J_H, ar_Hw_H, residuals):
    """plot Hw fitting results

    Args:
       Hw_l: lower limit of passband in angstrom
       Hw_u: upper limit of passband in angstrom
       res:minimize instance
       sigma:sigma
       colors:colors
       ar_J_H:J-H array
       ar_Hw_H:Hw-H array
       residuals:fitting residuals

    """
    a_str = str('{:.5f}'.format(res.x[0]))
    b_str = str('{:.5f}'.format(res.x[1]))
    pl_txt1 = '$y$ = '+a_str+' $x^2$ + '+b_str+' $x$'
    pl_txt2 = str('{:.2f}'.format(Hw_l*1e-4)) + '\u03bcm < $Hw$ < ' \
        + str('{:.2f}'.format(Hw_u*1e-4) + '\u03bcm')

    x_pl = np.linspace(min(colors[0]), max(colors[0]), 1000)
    y_pl = quad_func(x_pl, res.x)

    plt.figure(figsize=(5, 5.5))
    ax0 = plt.subplot2grid((5, 1), (0, 0), rowspan=4)
    ax1 = plt.subplot2grid((5, 1), (4, 0), rowspan=1, sharex=ax0)
    ax0.grid(color='gray', ls=':', lw=0.5)
    ax1.grid(color='gray', ls=':', lw=0.5)
    for i in range(len(ar_J_H)):
        ax0.scatter(ar_J_H[i], ar_Hw_H[i], s=5)  # , label='Av = '+str(Av_arr[i]))

    ax0.plot(x_pl, y_pl, ls='--', c='black', lw=1)
    ax0.text(x_pl[int((len(x_pl)*0.3))], y_pl[int((len(y_pl)*0.1))],
             pl_txt1, fontsize=12)
    ax0.text(x_pl[int((len(x_pl)*0.4))], y_pl[int((len(y_pl)*0.05))],
             pl_txt2, fontsize=12)

    ax0.set_ylabel('$Hw - H$', fontsize=15)
    ax0.legend(fontsize=10, loc='upper left')
    ax0.plot(x_pl, y_pl, ls='--', c='black', lw=1)

    ax1.scatter(colors[0], residuals, s=5, c='gray')
    ax1.set_xlabel('$J - H$', fontsize=15)
    plt.subplots_adjust(hspace=.0)
    plt.savefig('Hwcolor_'+str(int(Hw_l)) + '_' +
                str(int(Hw_u))+'.png', dpi=200)
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        Hw_l = float(sys.argv[1])
        Hw_u = float(sys.argv[2])
    else:
        print(
            'usage) [Hw lower] [Hw upper]')
        print(
            'ex) '+sys.argv[0]+' 9000 15000')

    res, sigma, colors, ar_J_H, ar_Hw_H, residuals = compute_Hw_relation(Hw_l, Hw_u)
    plot_Hwfit(Hw_l, Hw_u, res, sigma, colors, ar_J_H, ar_Hw_H, residuals)