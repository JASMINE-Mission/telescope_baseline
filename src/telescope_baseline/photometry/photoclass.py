import numpy as np
from astropy import units as u
from telescope_baseline.tools.mission.parameters import Parameters

class InstClass(object):
    """Class for Instrumental Setting used in exocounts, matched to InstClass in exocounts but using Parameters."""
    def __init__(self):
        
        par = Parameters.get_instance()    
        self.lamb = (par.long_wavelength_limit + par.short_wavelength_limit) / 2.0 * u.m
        self.dlam = (par.long_wavelength_limit - par.short_wavelength_limit) * u.m
        self.dtel = par.effective_pupil_diameter*u.m
        self.dstel = par.aperture_inner_diameter*u.m
        self.throughput = par.total_efficiency
        self.ndark = par.dark_current/u.s  # nd
        self.nread = par.read_out_noise  # nr
        self.fullwell = par.full_well_electron
        self.fgtel = 0.0  # foreground from a telescope
        self.fgatm = 0.0  # foreground from atmosphere


class TargetClass(object):
    """Class for Astronomical Targets."""

    def __init__(self):
        self.teff = None
        self.rstar = None
        self.d = None
        self.name = 'No Name'
        self.contrast = 1
        
class ObsClass(object):
    """Class for Observational Procedure."""

    def __init__(self, Inst, Target):

        self.inst = Inst
        self.target = Target
        
        # INPUTS
        self.mu = None
        self.texposure = None  # th
        self.tframe = None  # tr
        self.napix = None
        self.effnpix = None  # conversion for the brightest pixel
        self.fgaperture = None  # for foreground noise
        ####OUTPUTS####
        self.nphoton_exposure = None
        self.nphoton_frame = None
        self.flux = None
        self.photonf = None

        self.sign = None
        self.sigd = None
        self.sigr = None
        self.sign_relative = None
        self.sigd_relative = None
        self.sigr_relative = None

        self.sat = False  # Saturation

    def update(self):
        """Update status."""
        self.calc_noise()

        try:
            self.nphoton_brightest = self.nphoton_frame/self.effnpix
            if self.nphoton_brightest > self.inst.fullwell:
                self.sat = True
            else:
                self.sat = False
        except:
            self.sat = False

    def calc_noise(self):
        """compute noises."""
        from exocounts import nstar
        nstar.Nstar(self.inst, self.target, self)
        ppm = 1.e6
        ndframe = self.texposure.to(u.s)*self.inst.ndark

        try:
            self.sigd = np.sqrt(self.mu*self.napix*ndframe)
            self.sigd_relative = self.sigd/self.nphoton_exposure*ppm
        except:
            self.sigd = None
            self.sigd_relative = None

        try:
            self.sigr = np.sqrt(
                self.mu*self.napix*self.texposure.to(u.s)/self.tframe)*self.inst.nread
            self.sigr_relative = self.sigr/self.nphoton_exposure*ppm
        except:
            self.sigr = None
            self.sigr_relative = None

        # foreground
        try:
            self.nphoton_foreground = (self.fgaparture*(self.inst.fgtel+self.inst.fgatm)*self.inst.dlam *
                                       self.texposure*(self.inst.dtel/2.0)**2*np.pi*self.inst.throughput).to(1)
        except:
            self.nphoton_foreground = None


