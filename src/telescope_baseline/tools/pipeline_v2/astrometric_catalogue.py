from telescope_baseline.tools.pipeline_v2.catalog_entry import CatalogueEntry


class AstrometricCatalogue:
    """Data holder class for astrometric catalogue.

    Attributes:
        catalogue_entries: list of CatalogueEntry which is 5 parameter list for one star.

    """
    def __init__(self, catalogue_entries: list[CatalogueEntry] = []):
        """Constructor

        Args:
            catalogue_entries: list of CatalogueEntry
        """
        self.__catalogue_entries = catalogue_entries

    def get_catalogue(self) -> list[CatalogueEntry]:
        """

        Returns: array of CatalogueEntry

        """
        return self.__catalogue_entries
