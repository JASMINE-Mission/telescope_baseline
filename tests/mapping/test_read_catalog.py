def test_inout_detector():
    import pkg_resources           
    from telescope_baseline.mapping.read_catalog import read_jasmine_targets
    hdf=pkg_resources.resource_filename('telescope_baseline', 'data/cat.hdf')
    targets,l,b, hw=read_jasmine_targets(hdf)
    print(len(targets))
    
if __name__=="__main__":
    test_inout_detector()
