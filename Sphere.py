from typing import Tuple

import numpy as np
from dataclasses import dataclass

from HitPayload import HitPayload
from Material import Material
from Ray import Ray
from Hittable import Hittable

@dataclass
class Sphere(Hittable):
    Position: np.ndarray
    Radius: float
    Albedo: np.ndarray
    Material: Material

    def hit(self, ray: Ray, payload: HitPayload, t_min, t_max) -> tuple[HitPayload, bool]:
        origin = ray.Origin - self.Position
        # a * t² + b * t + c
        a = np.dot(ray.Direction.T, ray.Direction)
        b = 2.0 * np.dot(ray.Direction.T, origin)
        c = np.dot(origin.T, origin) - np.square(self.Radius)

        discriminant = np.square(b) - 4.0 * a * c

        if discriminant < 0:
            return payload, False

        closestT = (-b - np.sqrt(discriminant)) / (2 * a)

        if closestT > t_min and closestT < t_max:
            worldPosition = ray.Origin + closestT * ray.Direction
            outwardNormal = (worldPosition - self.Position) / self.Radius
            payload.set_face_normal(ray, outwardNormal)
            payload.WorldPosition = worldPosition
            payload.HitDistance = closestT
            return payload, True

        return payload, False
