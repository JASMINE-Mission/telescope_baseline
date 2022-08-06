from telescope_baseline.tools.pipeline_v2.catalogentry import CatalogueEntry
from telescope_baseline.tools.pipeline_v2.ontheskyposition import OnTheSkyPosition


class AstrometricCatalogue:
    def __init__(self, catalogue_entries: list[CatalogueEntry] = []):
        self.__catalogue_entries = catalogue_entries

