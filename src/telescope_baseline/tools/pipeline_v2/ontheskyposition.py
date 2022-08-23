from telescope_baseline.tools.pipeline_v2.skyposition import SkyPosition


class OnTheSkyPosition:
    """Data holder class of SkyPosition for every orbit.

    """
    def __init__(self, sky_positions: list[SkyPosition] = [], orbit_id: int = -1):
        """constructor

        Args:
            sky_positions: list of SkyPosition class object.
            orbit_id: orbit ID
        """
        self.__sky_positions = sky_positions
        self.__orbit_id = orbit_id

    @property
    def sky_positions(self):
        return self.__sky_positions

    @property
    def orbit_id(self):
        return self.__orbit_id
