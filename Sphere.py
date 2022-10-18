import numpy as np
from dataclasses import dataclass

@dataclass
class Sphere:
    """Class for keeping track of an item in inventory."""
    center: np.ndarray
    radius: float