import numpy as np
from dataclasses import dataclass
from Material import Material

@dataclass
class Sphere:
    Position: np.ndarray
    Radius: float
    Albedo: np.ndarray
    Material: Material
