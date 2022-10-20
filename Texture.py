from abc import ABC
import numpy as np

class Texture(ABC):
    def value(self) -> np.ndarray((3,1)):
        pass


class SolidColor(Texture):
    def __init__(self, r: float, g: float, b: float):
        self.r = r,
        self.g = g,
        self.b = b

    def value(self) -> np.ndarray((3, 1)):
        return np.array([[self.r], [self.g], [self.b]])
