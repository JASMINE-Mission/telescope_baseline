import pytest
from astropy.coordinates import SkyCoord
from astropy.time import Time
from telescope_baseline.tools.pipeline.astrometric_catalogue_builder import AstrometricCatalogueBuilder
from telescope_baseline.tools.pipeline.map_on_the_sky import MapOnTheSky
from telescope_baseline.tools.pipeline.position_on_the_sky import PositionOnTheSky


def test_from_on_the_sky_position1():
    # TODO. multiple star is needed for the test.
    t = [Time('2000-01-01 00:00:00.0'), Time('2000-02-01 00:00:00.0'), Time('2000-03-01 00:00:00.0'),
         Time('2000-04-01 00:00:00.0'), Time('2000-05-01 00:00:00.0'), Time('2000-06-01 00:00:00.0'),
         Time('2000-07-01 00:00:00.0'), Time('2000-08-01 00:00:00.0'), Time('2000-09-01 00:00:00.0'),
         Time('2000-10-01 00:00:00.0'), Time('2000-11-01 00:00:00.0'), Time('2000-12-01 00:00:00.0'),
         Time('2001-01-01 00:00:00.0')]
    londata = [4.657229292609037, 4.657231613943884, 4.6572328740589235, 4.657232905752553, 4.657231693733922,
               4.657229540136522, 4.657227130343018, 4.657224922535985, 4.65722356203127, 4.6572234180551595,
               4.657224576568599, 4.657226710038408, 4.657229355524401]
    latdata = [-0.09662669750312813, -0.09662682006310001, -0.0966270232593704, -0.09662727212328368,
               -0.09662747861779832, -0.09662760274710183, -0.0966276096289789, -0.09662749965491312,
               -0.09662729760688273, -0.09662706177588641, -0.09662684008417984, -0.09662670773667688,
               -0.09662669894287566]
    latdata2 = [-0.19662669750312813, -0.19662682006310001, -0.1966270232593704, -0.19662727212328368,
               -0.19662747861779832, -0.19662760274710183, -0.1966276096289789, -0.19662749965491312,
               -0.19662729760688273, -0.19662706177588641, -0.19662684008417984, -0.19662670773667688,
               -0.19662669894287566]
    builder = AstrometricCatalogueBuilder()
    o = []
    for i in range(len(t)):
        s = PositionOnTheSky(1, SkyCoord(lon=londata[i], lat=latdata[i], unit=('rad', 'rad'),
                                         frame='barycentricmeanecliptic'), 3000, t[i])
        o.append(MapOnTheSky(positions_on_the_sky=[s]))
    for i in range(len(t)):
        s = PositionOnTheSky(2, SkyCoord(lon=londata[i], lat=latdata2[i], unit=('rad', 'rad'),
                                         frame='barycentricmeanecliptic'), 3000, t[i])
        o.append(MapOnTheSky(positions_on_the_sky=[s]))
    a2 = builder.from_on_the_sky_position(o)

    coord = a2.get_catalogue()
    # TODO: need to fix proper motion check. Windows and Linux give different answer.
    assert 4.657 < coord[0][0][0] < 4.658
    assert -0.1 < coord[0][0][1] < -0.09
    assert 4.8e-6 < coord[0][0][4] < 4.9e-6
    assert 4.657 < coord[1][0][0] < 4.658
    assert -0.2 < coord[1][0][1] < -0.19
    assert 4.5e-6 < coord[1][0][4] < 4.6e-6