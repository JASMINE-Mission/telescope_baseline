from abc import ABCMeta, abstractmethod


class SimVisitor(metaclass=ABCMeta):
    """Abstract Visitor class for simulation and analysis.

    Object structure is represented in SimComponent class and sub classes, which are implemented as Composite.
    """
    from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
    from telescope_baseline.tools.pipeline.stellarimage import StellarImage
    from telescope_baseline.tools.pipeline.ontheskypositions import OnTheSkyPositions
    from telescope_baseline.tools.pipeline.astrometriccatalogue import AstrometricCatalogue

    def visit(self, obj):
        """visit method of simulation and analysis.

        Since dynamic type resolution is not possible in Python, this function has a role of switching the functions
        to be called by the argument type where it is implemented by using overloading in the Visitor pattern usually.
        If an unsupported type is given, an exception will be raised.  Please refer the document YY-024 for Visitor
        implementation by Python.

        Args:
            obj: Object of subclass of SimComponent.

        Returns:
            void
        """
        from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
        from telescope_baseline.tools.pipeline.stellarimage import StellarImage
        from telescope_baseline.tools.pipeline.ontheskypositions import OnTheSkyPositions
        from telescope_baseline.tools.pipeline.astrometriccatalogue import AstrometricCatalogue
        if isinstance(obj, DetectorImage):
            self.visit_di(obj)
        elif isinstance(obj, StellarImage):
            self.visit_si(obj)
        elif isinstance(obj, OnTheSkyPositions):
            self.visit_os(obj)
        elif isinstance(obj, AstrometricCatalogue):
            self.visit_ap(obj)
        else:
            raise DataTypeException

    @abstractmethod
    def visit_di(self, obj: DetectorImage):
        """The visit function that is called when an obj is an instance of the DetectorImage class.

        Args:
            obj (DetectorImage): an instance of DetectorImage

        Returns:void

        """
        pass

    @abstractmethod
    def visit_si(self, obj: StellarImage):
        """The visit function that is called when an obj is an instance of the StellarImage class.

        Args:
            obj (StellarImage): an instance of StellarImage

        Returns:void

        """
        pass

    @abstractmethod
    def visit_os(self, obj: OnTheSkyPositions):
        """The visit function that is called when an obj is an instance of the OnTheSkyCoordinate class.

        Args:
            obj (OnTheSkyPosition): an instance of OnTheSkyCoordinate

        Returns:void

        """
        pass

    @abstractmethod
    def visit_ap(self, obj: AstrometricCatalogue):
        """The visit function that is called when an obj is an instance of the AstrometricParameter class.

        Args:
            obj (AstrometricCatalogue): an instance of AstrometricParameter

        Returns:void

        """
        pass


class DataTypeException(Exception):
    """Exception if the argument of visit function is not the subclass of SimComponent.

    """

    def __init__(self):
        pass

    def __str__(self):
        return "Data Type Exception"
