from telescope_baseline.tools.pipeline_v2.catalogentry import CatalogueEntry


class AstrometricCatalogue:
    def __init__(self, catalogue_entries: list[CatalogueEntry] = []):
        self.__catalogue_entries = catalogue_entries

    def get_catalogue(self) -> list[CatalogueEntry]:
        return self.__catalogue_entries
