import numpy as np
from Ray import Ray


class aabb:
    def __init__(self, a: np.ndarray((3,1)), b: np.ndarray((3,1))):
        self.minimum = a
        self.maximum = b

    def hit(self, r: Ray, t_min: float, t_max: float) -> bool:
        for a in range(0, 3):
            invD = 1.0 / r.Direction[a][0]
            t0 = (self.minimum[a][0] - r.Origin[a][0]) * invD
            t1 = (self.maximum[a][0] - r.Origin[a][0]) * invD
            if invD < 0.0:
                t0, t1 = t1, t0  # swap variables
            t_min = t0 if t0 > t_min else t_min
            t_max = t1 if t1 < t_max else t_max
            if t_max <= t_min:
                return False
        return True