from telescope_baseline.tools.pipeline_v2.skyposition import SkyPosition


class OnTheSkyPosition:
    def __init__(self, sky_positions: list[SkyPosition] = [], orbit_id: int = -1):
        self.__sky_positions = sky_positions
        self.__orbit_id = orbit_id

    @property
    def sky_positions(self):
        return self.__sky_positions

    @property
    def orbit_id(self):
        return self.__orbit_id
