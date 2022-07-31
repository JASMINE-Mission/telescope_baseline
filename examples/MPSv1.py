if __name__ == "__main__":
    import pkg_resources           
    from telescope_baseline.mapping.read_catalog import read_jasmine_targets
    from telescope_baseline.mapping.plot_mapping import plot_targets, plot_n_targets, hist_n_targets, plot_ae_targets, hist_ae_targets, convert_to_convexes
    from telescope_baseline.mapping.mapset import fillgap_large_frame, inout_fillgap_large_frame
    import matplotlib.pyplot as plt
    import numpy as np
    import tqdm
    each_width_mm = 19.52
    width_mm = 22.4
    EFL_mm = 4370.0
    l_center = -1.2
    b_center = 0.0
    PA_deg = 0.0

    hdf = pkg_resources.resource_filename('telescope_baseline', 'data/cat_hw14.5.hdf')
    targets, l, b, hw = read_jasmine_targets(hdf)
    Nstar = 10 ** (hw / -2.5) / 10 ** (12.5 / -2.5)
    
    Ng = 11
    dizLmax = 1.5
    grid = np.linspace(-dizLmax, dizLmax, Ng)
    dummy_array = np.ones((Ng, Ng))
    gx = (grid[:, np.newaxis] * dummy_array).flatten()
    gy = (grid[np.newaxis, :]*dummy_array).flatten()

    nans = np.zeros_like(hw)
    pos = []
    for i in tqdm.tqdm(range(0, Ng * Ng)):
        fillgap_large_convexes = fillgap_large_frame(l_center, b_center, PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=gx[i], top=gy[i])
        ans = inout_fillgap_large_frame(targets, fillgap_large_convexes)
        nans_each = np.sum(ans, axis=(0, 1, 2))
        nans = nans + nans_each
        pos.append(fillgap_large_convexes)

    Nlargeframe = 4  # # of large frames to fill gaps
    Nlshape = 3  # # of Lshapes to construct the large frames
    accuracy_per_oneframe = 6000  # uas
    scale = 50.0 * accuracy_per_oneframe / Nlargeframe / Nlshape / (Ng * Ng)
    
    print("Nobs=", len(nans[nans > 0]))
    ac = 6000  # micro arcsec per frame
    
    final_ac = ac / np.sqrt(nans * scale) / np.sqrt(Nstar)
    print(np.shape(l), np.shape(b), np.shape(final_ac))
    
    plot_ae_targets(l, b, final_ac, cmap="CMRmap_r")
    hist_ae_targets(final_ac)

    pos = convert_to_convexes(pos)
    plot_n_targets(l, b, scale*nans, pos=pos, cmap="CMRmap_r")
    plot_n_targets(l, b, scale*nans, cmap="CMRmap_r", outfile="nno.png")
    hist_n_targets(scale*nans)
