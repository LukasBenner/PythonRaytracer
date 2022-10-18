import numpy as np
from dataclasses import dataclass

@dataclass
class Sphere:
    position: np.ndarray
    radius: float