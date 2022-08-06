from telescope_baseline.tools.pipeline_v2.skyposition import SkyPosition


class OnTheSkyPosition:
    def __init__(self, sky_positions: list[SkyPosition] = []):
        self.__sky_positions = sky_positions

    @property
    def sky_positions(self):
        return self.__sky_positions
