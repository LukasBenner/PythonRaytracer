import numpy as np
from dataclasses import dataclass

@dataclass
class Sphere:
    Position: np.ndarray
    Radius: float