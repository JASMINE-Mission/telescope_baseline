"""Example to count the number of the stars w/ Hw<12.5 by Kawata-san's basic mapping unit

"""

if __name__ == "__main__":
    import pkg_resources
    import numpy as np
    from telescope_baseline.mapping.aperture import lb_detector_unit
    from telescope_baseline.mapping.mapset import Lshape, inout_Lshape
    from telescope_baseline.mapping.read_catalog import read_jasmine_targets
    from telescope_baseline.mapping.plot_mapping import plot_targets

    each_width_mm = 19.52
    width_mm = 22.4
    EFL_mm = 4370.0
    l_center = -1.2
    b_center = 0.0
    PA_deg = 0.0

    hdf = pkg_resources.resource_filename('telescope_baseline', 'data/cat.hdf')
    targets, l, b, hw = read_jasmine_targets(hdf)
    # ans=inout_detector(targets,l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm,
    # EFL_mm=EFL_mm)

    # right L
    convexesset = Lshape(l_center, b_center, PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm,
                         left=1.0, top=-0.75)
    ans = inout_Lshape(targets, convexesset)

    # mid L
    l_center, b_center = lb_detector_unit("L", 1.5, l_center, b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    l_center, b_center = lb_detector_unit("B", 0.75, l_center, b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    convexesset = Lshape(l_center, b_center, PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm,
                         left=0.5)
    ans2 = inout_Lshape(targets, convexesset)
    ans = np.vstack([ans, ans2])

    # left L
    l_center, b_center = lb_detector_unit("L", 1.5, l_center, b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    convexesset = Lshape(l_center, b_center, PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm)
    ans2 = inout_Lshape(targets, convexesset)
    ans = np.vstack([ans, ans2])

    for i, ans_each in enumerate(ans):
        print("N in " + str(i) + "-th map=", np.sum(ans_each))
    print("N in total=", np.sum(np.max(ans, axis=0)))
    plot_targets(l, b, ans)
