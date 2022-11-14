import math

from telescope_baseline.tools.psf.psf import Psf
import numpy as np
from typing import Tuple
from scipy.special import jv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class PsfDonut(Psf):
    def __init__(self, wave_length: float, focal_length: float, obscuration_ratio: float):
        self.__obscuration_ratio = obscuration_ratio
        self.__focal_length = focal_length
        self.__wave_length = wave_length

    def _psf(self, r: float):
        fac = 2 * math.pi * r / self.__wave_length / self.__focal_length
        i0 = fac * fac / 8.86
        xi = r * fac
        if xi == 0.0:
            tmp = 1.0
        else:
            tmp = (2 * jv(1, xi) / xi - 2 * self.__obscuration_ratio * jv(1,self.__obscuration_ratio * xi) / xi)\
                  / (1 - self.__obscuration_ratio * self.__obscuration_ratio)
        return i0 * tmp * tmp

    def value(self, center_x: float, center_y: float) -> Tuple[float, float]:
        return center_x, center_y

if __name__ == '__main__':
    psf = PsfDonut(1.3e-6, 4.3, 0.35)
    fig = plt.figure(figsize = (10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel("x", size = 15)
    ax.set_ylabel("y", size = 15)
    ax.set_zlabel("j0(x**2+y**2)", size = 14)