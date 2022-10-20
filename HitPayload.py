from dataclasses import dataclass

import numpy as np

from Ray import Ray


@dataclass
class HitPayload:
    HitDistance: float = 0.0
    WorldPosition: np.ndarray = np.zeros((3, 1))
    WorldNormal: np.ndarray = np.zeros((3, 1))
    ObjectIndex: int = 0
    FrontFace: bool = True

    def set_face_normal(self, r: Ray, outward_normal: np.ndarray((3, 1))):
        self.FrontFace = np.dot(r.Direction.T, outward_normal)[0][0] < 0
        self.WorldNormal = outward_normal if self.FrontFace else -outward_normal
