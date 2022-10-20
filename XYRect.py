from dataclasses import dataclass

import numpy as np

from HitPayload import HitPayload
from Hittable import Hittable
from Material import Material
from Ray import Ray


@dataclass(order=True)
class XYRect(Hittable):
    x0: float
    x1: float
    y0: float
    y1: float
    k: float
    Material: Material

    def hit(self, ray: Ray, payload: HitPayload, t_min, t_max) -> (HitPayload, bool):
        distance: float = (self.k - ray.Origin[2][0]) / ray.Direction[2][0]

        x = ray.Origin[0][0] + distance * ray.Direction[0][0]
        y = ray.Origin[1][0] + distance * ray.Direction[1][0]
        if self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1:
            outwardNormal = np.array([[0], [0], [1]])
            worldPosition = ray.Origin + distance * ray.Direction
            payload.set_face_normal(ray, outwardNormal)
            payload.HitDistance = distance
            payload.WorldPosition = worldPosition
            return payload, True
        else:
            return payload, False
