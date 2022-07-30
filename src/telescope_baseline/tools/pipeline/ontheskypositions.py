from telescope_baseline.tools.pipeline.simnode import SimNode


class SkyPosition:
    """class of hold instantaneous stellar characteristics.

    """
    def __init__(self, num, coord, mag):
        """Constructor

        Args:
            num: ID
            coord: coordinate
            mag: magnitude
        """
        self.__id = num
        self.__coord = coord
        self.__mag = mag

    @property
    def id(self):
        return self.__id

    @property
    def ra(self):
        return self.__coord.gcrs.ra.deg

    @property
    def dec(self):
        return self.__coord.gcrs.dec.deg

    @property
    def coord(self):
        return self.__coord

    @property
    def mag(self):
        return self.__mag


class OnTheSkyPositions(SimNode):
    """Data class of instantaneous stellar positions at a certain time

    """
    def __init__(self, time=None):
        """Constructor

        Args:
            time: astropy.time.Time object which specify the time of this data set.
        """
        super().__init__()
        self.__time = time
        self.__sky_positions = []

    def add_entry(self, obj: SkyPosition):
        """Add instantaneous position data.

        Args:
            obj: SkyPosition object

        Returns:None

        """
        self.__sky_positions.append(obj)

    def set_on_the_sky_list(self):
        """Calculate sky coordinate from astrometric parameters

        Returns: None

        """
        catalogue = self.get_parent_list()
        self.__sky_positions = [None for _ in range(len(catalogue))]
        for i in range(len(catalogue)):
            c = catalogue[i]
            c1 = c.coord.apply_space_motion(new_obstime=self.__time)
            self.__sky_positions[i] = SkyPosition(c.id, c1, c.mag)

    def get_coord(self, i):
        return self.__sky_positions[i].coord

    def get_time(self):
        """ get time

        Returns:time which is held in this class instance.

        """
        return self.__time

    def get_list(self):
        """

        Returns: list of instantaneous stellar position list.

        """
        return self.__sky_positions

    def get(self, i):
        """

        Args:
            i: ID

        Returns: instantaneous stellar position object wish ID = i.

        """
        return self.__sky_positions[i]

    def solve_distortion(self):
        """

        Returns:
        TODO: Should implement.
        """
        pass

    def map_to_the_sky(self):
        """

        Returns:
        TODO: should implement.
        """
        a = []
        for i in range(self.get_child_size()):
            for j in range(len(self._child[i].pixel_to_world())):
                a.append(self._child[i].pixel_to_world()[j])
        if self.get_child_size() > 0:
            self.__sky_positions = []
            for i in range(len(a)):
                self.__sky_positions.append(SkyPosition(a[i][0], a[i][1], a[i][2]))

    def accept(self, v):
        v.visit(self)
