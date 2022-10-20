import numpy as np
from dataclasses import dataclass
from Material import Material
from Ray import Ray
from Hittable import Hittable

@dataclass
class Sphere(Hittable):
    Position: np.ndarray
    Radius: float
    Albedo: np.ndarray
    Material: Material

    def hit(self, ray: Ray) -> float:
        origin = ray.Origin - self.Position
        # a * t² + b * t + c
        a = np.dot(ray.Direction.T, ray.Direction)
        b = 2.0 * np.dot(ray.Direction.T, origin)
        c = np.dot(origin.T, origin) - np.square(self.Radius)

        discriminant = np.square(b) - 4.0 * a * c

        if discriminant < 0:
            return -1.0
        return (-b - np.sqrt(discriminant)) / (2 * a)
