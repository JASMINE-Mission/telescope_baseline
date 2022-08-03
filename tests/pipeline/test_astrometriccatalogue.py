from astropy.coordinates import SkyCoord
from astropy.time import Time
from telescope_baseline.tools.pipeline.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.ontheskypositions import OnTheSkyPositions, SkyPosition


def test_calculate_ap_parameters():
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
    a = AstrometricCatalogue()
    o = []
    for i in range(len(t)):
        o.append(OnTheSkyPositions(t[i]))
        o[i].add_entry(SkyPosition(1, SkyCoord(lon=londata[i], lat=latdata[i], unit=('rad', 'rad'),
                                               frame='barycentricmeanecliptic'), 12.5))
        a.add_child(o[i])
    a.calculate_ap_parameters()
    result = a.get_parameters()

    assert(abs(result[0][0] - 4.657228194950601) < 1e-7)
    assert(abs(result[0][1] + 0.09662715320481664) < 1e-7)
    assert(abs(result[0][2]) < 1e-7)
    assert(abs(result[0][3]) < 1e-7)
    assert(abs(result[0][4] - 4.84813681109536e-06) < 1e-7)
