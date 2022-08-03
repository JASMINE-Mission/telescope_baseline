from telescope_baseline.tools.pipeline.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
from telescope_baseline.tools.pipeline.ontheskypositions import OnTheSkyPositions
from telescope_baseline.tools.pipeline.stellarimage import StellarImage
from telescope_baseline.tools.pipeline.visitor import SimVisitor


class Simulation(SimVisitor):
    """Visitor class for generate pseudo data.

    Pipeline processing is realized by Visitor. Simulation will be done from Astrometric catalogue downward to detector
     image, direction opposite to analysis. This is inherited from SimVisitor class in visitor.py.  This class
     implements visit_di, visit_si, visit_os and visit_ap methods, which is defined abstract methods in the super-class.

    TODO: in visit_di, if output list is empty, raise exception.

    """
    def visit_di(self, obj: DetectorImage):
        if obj.has_parent():
            obj.get_parent_list()
        # raise exception if the list is empty
        obj.make_image()  # generate fits
        obj.make_fits()
        obj.save_fits()

    def visit_si(self, obj: StellarImage):
        if obj.has_parent():
            obj.world_to_pixel()
        for ii in range(obj.get_child_size()):
            obj.get_child(ii).accept(self)

    def visit_os(self, obj: OnTheSkyPositions):
        if obj.has_parent():
            obj.get_parent_list()
            obj.set_on_the_sky_list()
        for ii in range(obj.get_child_size()):
            obj.get_child(ii).accept(self)

    def visit_ap(self, obj: AstrometricCatalogue):
        # non operation
        for ii in range(obj.get_child_size()):
            obj.get_child(ii).accept(self)
