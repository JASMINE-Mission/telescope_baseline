from abc import ABCMeta, abstractmethod
from typing import Tuple


class Psf(metaclass=ABCMeta):
    @abstractmethod
    def value(self, x: float, y: float) -> Tuple[float, float]:
        pass
