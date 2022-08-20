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
    p.join()
    return data_spec


def cal_photon(input_arrays):
    """compute photons.

    Args:
        input_arrays:

    Returns:
        photon count?
    """
    # 1.透過関数をsplineで関数化.
    # 2.透過関数とFluxを波長を乗じて積分し、光子数に換算.
    # 3.最終的に比の計算を行うため、各係数は無視.
    spectra_array, filter_func, av = input_arrays

    ff = interpolate.interp1d(x=filter_func[1],
                              y=filter_func[2], kind='cubic')

    spec_narrow = spectra_array[:, ((filter_func[1, 0] < spectra_array[0]) &
                                    (spectra_array[0] < filter_func[1, -1]))]

    transmit_f = ff(spec_narrow[0])*spec_narrow[1]  # transmitted flux
    dx = np.diff(spec_narrow[0])

    extinction = 10 ** (-1 * a_lambda(av, spec_narrow[0, :-1]) / 2.5)
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
    p.join()
    data_photon = np.array(data_photon, dtype='f8')

    return data_photon


def load_filter():
    """Load filters.

    Returns:
        Jband filter
        Hbandfilter
    """

    fl_j = pkgutil.get_data('telescope_baseline', 'data/filter/J_filter.dat')
    fl_h = pkgutil.get_data('telescope_baseline', 'data/filter/H_filter.dat')
    fltj = np.loadtxt(BytesIO(fl_j), comments='#', dtype='f8').T
    flth = np.loadtxt(BytesIO(fl_h), comments='#', dtype='f8').T
    fltj[1] = fltj[1]*1e4  # mic -> angstrom
    flth[1] = flth[1]*1e4

    return fltj, flth


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
    hw = np.array((index, x, y))

    return hw


def a_lambda(av, x):
    """calculate A lambda.

    Args:
        av: Av
        x: x

    Returns:
        A_lambda

    """
    ak_av = 0.112
    ak = ak_av * av
    x_um = x * 1e-4
    coeff = 5.2106 * (x_um ** (-2.112))

    return coeff * ak

def a_lambda_linear(av, x):
    """calculate A lambda with linear law.

    Args:
        av: Av
        x: x

    Returns:
        A_lambda

    """
    aj_av = 0.282
    ak_av = 0.112

    aj = aj_av * av
    ak = ak_av * av

    return ((x-12000) * ak + (20000 - x) * aj) / (20000 - 12000)


def quad_func(x, args):
    a = args[0]
    b = args[1]
    return a * x ** 2 + b * x


def least_sq(coeff, *args):
    x, y = args
    chi2 = np.sum(np.square(quad_func(x, coeff) - y)) ** 0.5
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


def calc_zero_magnitude_spectra(fil_j, fil_h, fil_hw):
    """zero magnitude spectra

    Args:
        fil_j:
        fil_h:
        fil_hw:

    Returns:
        zero magnitude of J?
        zero magnitude of H?
        zero magnitude of Hw?

    """

    uka0v = pkgutil.get_data('telescope_baseline', 'data//spectra/uka0v.dat')
    spec_a0v = np.loadtxt(BytesIO(uka0v), comments='#', dtype='f8').T
    p_jo = cal_photon([spec_a0v, fil_j, 0])
    p_ho = cal_photon([spec_a0v, fil_h, 0])
    p_hwo = cal_photon([spec_a0v, fil_hw, 0])
    return p_jo, p_ho, p_hwo


def calc_color_arrays(data_spec, fil_j, fil_h, fil_hw, p_jo, p_ho, p_hwo):
    """compute colors

    Args:
        data_spec:
        fil_j:
        fil_h:
        fil_hw:
        p_jo: zero magnitude of J?
        p_ho:  zero magnitude of H?
        p_hwo:  zero magnitude of Hw?

    Returns:
        ar_J_H: J-H array
        ar_Hw_H: Hw-H array
        Av array used

    """
    av_ar = np.linspace(0, 60, 5)
    ar_hw_h = []
    ar_j_h = []
    a_arr = []
    for av in av_ar:  # -- roop for Av
        p_j = calphoton_map_multi(data_spec, fil_j, av)
        p_h = calphoton_map_multi(data_spec, fil_h, av)
        p_hw = calphoton_map_multi(data_spec, fil_hw, av)

        rel_j = -2.5*(np.log10(p_j) - np.log10(p_jo))
        rel_h = -2.5*(np.log10(p_h) - np.log10(p_ho))
        rel_hw = -2.5*(np.log10(p_hw) - np.log10(p_hwo))

        j_h = rel_j - rel_h
        hw_h = rel_hw - rel_h

        ar_hw_h.append(hw_h)
        ar_j_h.append(j_h)
        a_arr.append(av)

    return ar_j_h, ar_hw_h, a_arr


def calc_colors(ar_j_h, ar_hw_h):
    """
    Args:
       ar_j_h: J-H array
       ar_hw_h: Hw-H array

    Returns:
       colors
    """
    return np.ravel(np.array(ar_j_h)), np.ravel(np.array(ar_hw_h))


def compute_hw_relation(hw_l, hw_u):
    """compute Hw - (H, J-H) relation

    Args:
       hw_l: lower limit of passband in angstrom
       hw_u: upper limit of passband in angstrom

    Returns:
       minimize instance
       sigma
       colors
       J-H array
       Hw-H array
       fitting residuals
    """
    return _compute_hw_relation(hw_l, hw_u, read_spectra_all())


def _compute_hw_relation(hw_l, hw_u, spectra_all):
    data_spec = read_map_multi(spectra_all)
    fil_hw = set_range_Hw_band(hw_l, hw_u)
    fil_j, fil_h = load_filter()
    p_jo, p_ho, p_hwo = calc_zero_magnitude_spectra(fil_j, fil_h, fil_hw)
    ar_j_h, ar_hw_h, av_arr = calc_color_arrays(data_spec, fil_j, fil_h, fil_hw, p_jo, p_ho, p_hwo)
    colors = calc_colors(ar_j_h, ar_hw_h)
    x0 = [1., 0.8]
    res = minimize(least_sq, x0, args=colors, method='Nelder-Mead', tol=1e-11)
    residuals = colors[1] - quad_func(colors[0], res.x)
    sigma = np.std(residuals)
    result = {'x0': res.x[0],
              'x1': res.x[1],
              'std': sigma,
              'chi2': res.fun}
    print(result)
    return res, sigma, colors, ar_j_h, ar_hw_h, residuals


def plot_hwfit(hw_l, hw_u, res, sigma, colors, ar_j_h, ar_hw_h, residuals):
    """plot Hw fitting results

    Args:
       hw_l: lower limit of passband in angstrom
       hw_u: upper limit of passband in angstrom
       res:minimize instance
       sigma:sigma
       colors:colors
       ar_j_h:J-H array
       ar_hw_h:Hw-H array
       residuals:fitting residuals

    """
    a_str = str('{:.5f}'.format(res.x[0]))
    b_str = str('{:.5f}'.format(res.x[1]))
    pl_txt1 = '$y$ = ' + a_str + ' $x^2$ + ' + b_str + ' $x$'
    pl_txt2 = str('{:.2f}'.format(hw_l * 1e-4)) + '\u03bcm < $Hw$ < ' \
              + str('{:.2f}'.format(hw_u * 1e-4) + '\u03bcm')

    x_pl = np.linspace(min(colors[0]), max(colors[0]), 1000)
    y_pl = quad_func(x_pl, res.x)

    plt.figure(figsize=(5, 5.5))
    ax0 = plt.subplot2grid((5, 1), (0, 0), rowspan=4)
    ax1 = plt.subplot2grid((5, 1), (4, 0), rowspan=1, sharex=ax0)
    ax0.grid(color='gray', ls=':', lw=0.5)
    ax1.grid(color='gray', ls=':', lw=0.5)
    for i in range(len(ar_j_h)):
        ax0.scatter(ar_j_h[i], ar_hw_h[i], s=5)  # , label='Av = '+str(Av_arr[i]))

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
    plt.savefig('Hwcolor_' + str(int(hw_l)) + '_' +
                str(int(hw_u)) + '.png', dpi=200)
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        hw_l = float(sys.argv[1])
        hw_u = float(sys.argv[2])
    else:
        print(
            'usage) [Hw lower] [Hw upper]')
        print(
            'ex) '+sys.argv[0]+' 9000 15000')

    res, sigma, colors, ar_j_h, ar_hw_h, residuals = compute_hw_relation(hw_l, hw_u)
    plot_hwfit(hw_l, hw_u, res, sigma, colors, ar_j_h, ar_hw_h, residuals)
