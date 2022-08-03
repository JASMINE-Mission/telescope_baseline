from telescope_baseline.tools.pipeline.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
from telescope_baseline.tools.pipeline.ontheskypositions import OnTheSkyPositions
from telescope_baseline.tools.pipeline.stellarimage import StellarImage
from telescope_baseline.tools.pipeline.visitor import SimVisitor


class Analysis(SimVisitor):
    """ Visitor class for analysis

    """
    def visit_di(self, obj: DetectorImage):
        try:
            obj.load()
        except FileNotFoundError:
            print('file not found.')

    def visit_si(self, obj: StellarImage):
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)
            obj.extract()
            obj.to_photon_num()
            obj.construct_e_psf()
            obj.x_match()
            obj.make_list()

    def visit_os(self, obj: OnTheSkyPositions):
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)
        obj.solve_distortion()
        obj.map_to_the_sky()

    def visit_ap(self, obj: AstrometricCatalogue):
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)
        obj.calculate_ap_parameters()
