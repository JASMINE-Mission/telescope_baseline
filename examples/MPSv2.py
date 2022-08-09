import numpy as np
from telescope_baseline.mapping.aperture import lb_detector_unit, four_square_convexes, inout_four_square_convexes, ang_detector_unit, lb2ang, ang2lb


from matplotlib import patches



if __name__ == "__main__":
    import pkg_resources           
    from telescope_baseline.mapping.read_catalog import read_jasmine_targets
    from telescope_baseline.mapping.mapset import ditheringmap, inout_convexesset
    from telescope_baseline.mapping.plot_mapping import plot_targets, plot_n_targets, hist_n_targets, plot_ae_targets, hist_ae_targets, convert_to_convexes, plot_convexes
    import matplotlib.pyplot as plt
    import numpy as np
    import tqdm
    each_width_mm=19.52
    width_mm=22.4
    EFL_mm=4370.0
    l_center=0.6
    b_center=0.3
    PA_deg=0.0
    Ndither=[50,20]
    gap_width_mm=width_mm - each_width_mm
    
    hdf=pkg_resources.resource_filename('telescope_baseline', 'data/cat_hw14.5.hdf')
    targets,l,b,hw=read_jasmine_targets(hdf)
    Nstar=10**(hw/-2.5)/10**(12.5/-2.5)
    convexesset=ditheringmap(l_center,b_center,PA_deg, dithering_width_mm=gap_width_mm, Ndither=Ndither,
                             width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=1.0,top=-0.75)

    pos=convert_to_convexes(convexesset)
    plot_convexes(l,b,pos)

    #check inout dithering map
    ans=inout_convexesset(targets,convexesset)

    #count number 
    nans=np.sum(ans,axis=0) #number of obs    
    plot_n_targets(l,b,nans,cmap="CMRmap_r")    
    hist_n_targets(nans)


    # S/N computing, Kawata-san needs to correct the below.
    scale=1.0 
    ac=6000 # micro arcsec per frame
    final_ac=ac/np.sqrt(nans*scale)       
    plot_ae_targets(l,b,final_ac,cmap="CMRmap_r")
    hist_ae_targets(final_ac)

