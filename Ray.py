from dataclasses import dataclass

import numpy as np


@dataclass
class Ray:
    Origin: np.ndarray
    Direction: np.ndarray
