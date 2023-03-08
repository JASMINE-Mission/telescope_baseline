def galactic_coordinate_to_detector_chip_coordinate(l,
                                               b,
                                               l_chip_center,
                                               b_chip_center,
                                               PA_deg,
                                               each_width_mm=19.52,
                                               EFL_mm=4370.0,
                                               npixels=1300):
    """checking if targets are in or out four square convexes

    Args:
        l: galactic coordinate, l (deg)
        b: galacitic coordinate, b (deg)
        l_chip_center: chip center of galactic coordinate, l (deg)
        b_chip_center: chip center of galactic coordinate, b (deg)
        PA_deg: position angle in deg
        each_width_mm: the chip width in the unit of mm
        EFL_mm: effective focal length in the unit of mm
        
    Returns:
        detector chip coordinate X, detector chip coordinate Y
    """

    return
