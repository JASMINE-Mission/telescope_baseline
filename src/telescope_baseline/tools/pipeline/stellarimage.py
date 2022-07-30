from astropy.nddata import NDData
from photutils import extract_stars, EPSFBuilder
from telescope_baseline.tools.pipeline.simnode import SimNode
from photutils.detection import find_peaks
from astropy.table import Table


class OnDetectorPosition:
    """Hold position on detector, id, and magnitude

    """
    def __init__(self, n, x, y, m):
        self.__id = n
        self.__x = x
        self.__y = y
        self.__mag = m

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def id(self):
        return self.__id

    @property
    def mag(self):
        return self.__mag


class StellarImage(SimNode):
    """Hold position list in detector coordinate.

    """
    def __init__(self, wcs):
        """Constructor

        Args:
            wcs: world coordinate system of FOV center.

        TODO:
            * maximum pixel number is fixed to 4000 in this implementation. It will be flexible.

        """
        super().__init__()
        self.__wcs = wcs
        self.__position_list = []
        self.__pix_max = 4000
        self.__e_psf_stars = None
        self.__e_psf_model = None
        self.__window_size = 9  # window size

    def accept(self, v):
        v.visit(self)

    def world_to_pixel(self):
        """Calculate position in detector coordinate

        Returns: None

        TODO:
            * This class support only galactic coordinate in wcs. It should be more flexible.
            * This implementation not support the gap between detectors.
            * In __position_list x[i][2], number of photon should be flexible, is now assumed to be 3000 and const.

        """
        if "GLON" not in self.__wcs.wcs.ctype[0]:
            print("Coordinate system " + self.__wcs.wcs.ctype[0] + " is not supported")
            raise ValueError
        tmp = []
        self.__position_list = []
        parent_list = self.get_parent_list()
        for i in range(len(parent_list)):
            tmp.append([parent_list[i].coord.galactic.l.deg, parent_list[i].coord.galactic.b.deg])
        tmp = self.__wcs.wcs_world2pix(tmp, 0)
        for i in range(len(tmp)):
            if not(tmp[i][0] < 0 or tmp[i][1] < 0 or tmp[i][0] > self.__pix_max or tmp[i][1] > self.__pix_max):
                c = OnDetectorPosition(i, tmp[i][0], tmp[i][1], 3000)
                self.__position_list.append(c)
        #  for revert conversion use self.__wcs.wcs_pix2world(pix_array, 0)

    def pixel_to_world(self):
        tmp = []
        for i in range(len(self.__position_list)):
            sky = self.__wcs.pixel_to_world(self.__position_list[i].x, self.__position_list[i].y)
            tmp.append([self.__position_list[i].id, sky, self.__position_list[i].mag])
        return tmp

    def add_position(self, pos_list):
        """ List of stellar positions

        Args:
            pos_list: ndarray of array (x, y, Nph) where x and y is the position in the pixel coordinate, and Nph is
             number of photons.

        Returns:

        """
        self.__position_list = pos_list

    def get_list(self):
        """ Get observable stellar positions in detector coordinate

        Returns: position list.

        """
        return self.__position_list

    def extract(self):
        """ extract stellar image from the fits data.

        Returns:

        """
        _data = self._child[0].get_hdu().data
        peaks_tbl = find_peaks(_data, threshold=200.)
        half_size = (self.__window_size - 1) / 2
        x = peaks_tbl['x_peak']
        y = peaks_tbl['y_peak']
        mask = ((x > half_size) & (x < (_data.shape[1] - 1 - half_size)) & (y > half_size) &
                (y < (_data.shape[0] - 1 - half_size)))
        stars_tbl = Table()
        stars_tbl['x'] = x[mask]
        stars_tbl['y'] = y[mask]
        nddata = NDData(data=_data)
        self.__e_psf_stars = extract_stars(nddata, stars_tbl, size=self.__window_size)

    def to_photon_num(self):
        """ convert to number of photons

        Returns:
    TODO: Should implement
        """
        pass

    def construct_e_psf(self):
        """ construct effective psf model and fit center with the model

        Returns:

        """
        e_psf_builder = EPSFBuilder(oversampling=4, maxiters=3, progress_bar=True)
        es = self.__e_psf_stars
        self.__e_psf_model, self.__e_psf_stars = e_psf_builder(es)

    def x_match(self):
        """ cross match and add id

        Returns:
    TODO: should implement.
        """
        pass

    def make_list(self):
        self.__position_list = []
        i = 0
        for s in self.__e_psf_stars.all_stars:
            self.__position_list.append(OnDetectorPosition(i, s.center[0], s.center[1], 0))
        return self.__position_list
