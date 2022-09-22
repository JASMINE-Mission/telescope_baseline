
# MPS_rect-jhk.py
# Rectangular shape JASMINE Galactic Centre survey region.
# Finer dithering to cover the whole JASMINE region similar number of times
# and at the different position in the detector.
# use Hw = 0.9J + 0.1H - 0.06*(J-H)**2

import numpy as np
import h5py

if __name__ == "__main__":
    import pkg_resources
    import matplotlib.pyplot as plt
    from telescope_baseline.mapping.read_catalog import read_jasmine_targets_jhk
    from telescope_baseline.mapping.mapset import ditheringmap, inout_convexesset
    from telescope_baseline.mapping.plot_mapping import plot_n_targets, hist_n_targets, plot_ae_targets, hist_ae_targets, convert_to_convexes, plot_convexes
    # size of one detector
    each_width_mm = 19.52
    # the size of one detector + gap.
    width_mm = 22.4
    EFL_mm = 4370.0
    l_center = 0.7
    b_center = 0.6
    # size of the Galactic centre survey
    dl_gcs = 0.7+1.4
    db_gcs = 1.2
    PA_deg = 0.0
    # from the output of "number of dither l, b below.
    # in the case of dithering_width_mm = 0.05*mm_deg
    Ndither = [52, 34]
    # in the case of dithering_width_mm = 0.01*mm_deg
    # Ndither = [264, 174]
    gap_width_mm = width_mm - each_width_mm
    # make gap_width_mm smaller
    # gap_width_mm *= 0.8
    print(' gap width (mm)=', gap_width_mm)
    # deg vs mm
    mm_deg = EFL_mm*np.pi/180.0
    deg_mm = 1.0/mm_deg
    print(' 1 deg is ', mm_deg, ' mm')
    # dithering width (deg) -> (mm)
    dithering_width_mm = 0.05*mm_deg
    # dithering_width_mm = 0.01*mm_deg
    print('dithering width (mm) =', dithering_width_mm)

    # shift the starting point further by the size of one detector
    l_center += (each_width_mm+0.5*gap_width_mm-dithering_width_mm)*deg_mm
    b_center += (each_width_mm+0.5*gap_width_mm-dithering_width_mm)*deg_mm
    print(' starting central point (l, b) =', l_center, b_center)
    print(' size of one detector and gap (deg) =', each_width_mm*deg_mm,
          gap_width_mm*deg_mm)
    add_dither_deg = (2.0*width_mm-gap_width_mm-dithering_width_mm)*deg_mm
    print('additional size to dither =', add_dither_deg)
    print('number of dither l, b=',
          (add_dither_deg+dl_gcs)*mm_deg/dithering_width_mm,
          (add_dither_deg+db_gcs)*mm_deg/dithering_width_mm)

    hdf = pkg_resources.resource_filename('telescope_baseline',
                                          'data/cat_jhk_hw12.5.hdf')
    targets, l, b, jmag, hmag, ksmag = read_jasmine_targets_jhk(hdf)
    hw = 0.9*jmag+0.1*hmag-0.06*((jmag-hmag)**2)
    # plot CMR
    plt.scatter(jmag-hmag, hw, s=0.01)
    plt.ylim(15.0, 1.0)
    plt.show()
    # compute the scaling depending on the number of photon
    Nstar = 10**(hw/-2.5)/10**(12.5/-2.5)
    # square region
    convexesset = ditheringmap(l_center, b_center, PA_deg,
                               dithering_width_mm=dithering_width_mm,
                               Ndither=Ndither,
                               width_mm=width_mm,
                               each_width_mm=each_width_mm,
                               EFL_mm=EFL_mm, left=1.0, top=-0.75)

    print(' shape of the final convexesset =', np.shape(convexesset))

    pos = convert_to_convexes(convexesset)
    plot_convexes(l, b, pos)

    # check inout dithering map
    ans = inout_convexesset(targets, convexesset)

    # count number
    # number of observation for each star after covering the whole fields
    nans = np.sum(ans, axis=0)
    plot_n_targets(l, b, nans, cmap="CMRmap_r")
    hist_n_targets(nans)

    # S/N computing, Kawata-san needs to correct the below.
    scale = 1.0
    # number of small frames per the Galactic centre field.
    nsf_per_gcf = np.shape(convexesset)[0]
    print(' number of small fields to cover the whole field =', nsf_per_gcf)
    # astrometric accuracy per exposure (micro arcsec per frame)
    ac = 6000
    norbits = 6000  # number of orbits used for the GC survey in 3 years
    nex_per_sf = 20  # number of exposure per small frame
    nsf_per_orb = 8  # number of small frames per orbit.
    # number of orbit required to cover the whole Gf survey area.
    norb_gcf = nsf_per_gcf/nsf_per_orb
    print(' number of orbits to cover the whole GC field =', norb_gcf)
    scale = nex_per_sf*(norbits/norb_gcf)
    final_ac = np.zeros_like(nans)
    final_ac[nans > 0] = ac/np.sqrt(nans[nans > 0]*scale) \
        / np.sqrt(Nstar[nans > 0])
    # set the worst accuracy of 999
    final_ac[nans <= 0] = 999.999

    plot_ae_targets(l, b, final_ac, cmap="CMRmap_r")
    hist_ae_targets(final_ac)

    # save the data
    with h5py.File("MPS_rect.h5", "w") as f:
        dsetl = f.create_dataset("l", data=l)
        dsetb = f.create_dataset("b", data=b)
        dsethw = f.create_dataset("hw", data=hw)
        dsetjmag = f.create_dataset("Jmag", data=jmag)
        dsethmag = f.create_dataset("Hmag", data=hmag)
        dsetksmag = f.create_dataset("Ksmag", data=ksmag)
        dsetnans = f.create_dataset("nans", data=nans)
        dsetfac = f.create_dataset("final_ac", data=final_ac)
