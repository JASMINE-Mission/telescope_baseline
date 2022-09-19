def test_inout_detector():
    import pkg_resources
    from telescope_baseline.mapping.read_catalog import read_jasmine_targets
    hdf = pkg_resources.resource_filename('telescope_baseline', 'data/cat.hdf')
    targets, l, b, hw = read_jasmine_targets(hdf)
    print(len(targets))

    from telescope_baseline.mapping.read_catalog import read_jasmine_targets_jhk
    hdf_jhk = pkg_resources.resource_filename(
      'telescope_baseline', 'data/cat_jhk_hw12.5.hdf')
    targets_jhk, l, b, jmag, hmag, ksmag = read_jasmine_targets_jhk(hdf_jhk)
    print(len(targets_jhk))


if __name__ == "__main__":
    test_inout_detector()
