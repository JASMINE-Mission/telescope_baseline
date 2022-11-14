from telescope_baseline.tools.psf.psf import Psf
import numpy as np
from typing import Tuple


class PsfGauss(Psf):
    def __init__(self, width: float):
        self.__width = width

    def value(self, center_x: float, center_y: float) -> Tuple[float, float]:
        return self.__width * np.random.randn() + center_x, self.__width * np.random.randn() + center_y


if __name__ == '__main__':
    psf = PsfGauss()
    x = []
    y = []
    for i in range(10000):
        xx, yy= psf.value(0.0, 0.0)
        x.append(xx)
        y.append(yy)

    xn = np.array(x)
    yn = np.array(y)

    print(np.mean(xn))
    print(np.std(xn))
    print(np.mean(yn))
    print(np.std(yn))
