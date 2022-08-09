from exocounts import exocounts
from exocounts import convmag
from astropy import constants as const
from astropy import units as u
import numpy as np
from telescope_baseline.photometry.photoclass import InstClass, ObsClass, TargetClass
from telescope_baseline.tools.mission.parameters import Parameters

#parameter setting
par=Parameters.get_instance()
par.set_aperture_diameter(0.36)
par.set_quantum_efficiency(0.7)
par.set_short_wavelength_limit(1.0e-6)
print("Is this OK? -> average_telescope_throughput=", par.average_telescope_throughput)
cpix=1.7

inst=InstClass()
target=TargetClass()
target.teff = 3000.0*u.K #K
target.rstar = 0.2*const.R_sun #Rsolar
target.d=16.0*u.pc 

obs=ObsClass(inst,target) 
obs.texposure = 0.0833*u.h #cadence [hour]
obs.tframe = 12.5*u.s  #time for one frame [sec]
obs.napix = 15 # number of the pixels in aperture 
obs.mu = 1 
S=cpix*cpix*np.pi #core size
obs.effnpix = S/3.0 #3 is an approx. increment factor of PSF
obs.mu = 1 
obs.target = target
obs.update()

print("=========================")
print("saturation?",obs.sat)
print("dark [ppm]=",obs.sigd)
print("readout [ppm]=",obs.sigr)
print("photon [ppm]=",obs.sign)
print("=========================")
print("photon relative=",obs.sign_relative)


seven_sigma_percent=np.sqrt(1.0/obs.nphoton_exposure)*1e2*7.0
roundvalue=np.round(seven_sigma_percent,2)
print("7 sigma per exposure = ",seven_sigma_percent)

criterion = 0.2 #percent  per exposure
if roundvalue > criterion:
    raise ValueError("Current setting is not suitable for exoplanet survey!")
else:
    print("We can do the exoplanet survey!")
