import numpy as np
import pytest
from astropy.time import Time
from telescope_baseline.tools.pipeline.astrometric_catalogue_builder import lsf_fit_function_for_astrometric_parameters


def test_lsf_fit_function_for_astrometric_parameter():
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
    parameter = [np.radians(266), np.radians(-5), 0., 0., np.radians(1 / 3600)]
    residual = lsf_fit_function_for_astrometric_parameters(parameter, t, londata, latdata)
    for i in range(residual.size):
        residual[i] == pytest.approx(0.00030231, 1e-5)
