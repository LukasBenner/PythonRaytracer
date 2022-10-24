import numpy as np

from HitPayload import HitPayload
from Hittable import Hittable
from Ray import Ray

from dataclasses import dataclass

@dataclass()
class RotateY(Hittable):
    def __init__(self, p: Hittable, angle: float):
        self.object = p
        radians = np.deg2rad(angle)
        self.sinTheta = np.sin(radians)
        self.cosTheta = np.cos(radians)
        self.Material = p.Material


    def hit(self, ray: Ray, payload: HitPayload, t_min, t_max) -> tuple[HitPayload, bool]:
        origin = np.copy(ray.Origin)
        direction = np.copy(ray.Direction)

        origin[0][0] = self.cosTheta * ray.Origin[0][0] - self.sinTheta * ray.Origin[2][0]
        origin[2][0] = self.sinTheta * ray.Origin[0][0] + self.cosTheta * ray.Origin[2][0]

        direction[0][0] = self.cosTheta * ray.Direction[0][0] - self.sinTheta * ray.Direction[2][0]
        direction[2][0] = self.sinTheta * ray.Direction[0][0] + self.cosTheta * ray.Direction[2][0]

        rotatedRay = Ray(origin, direction)

        payload, success = self.object.hit(rotatedRay, payload, t_min, t_max)

        if not success:
            return payload, False

        hitPoint = payload.WorldPosition
        normal = payload.WorldNormal

        hitPoint[0][0] = self.cosTheta * payload.WorldPosition[0][0] + self.sinTheta * payload.WorldPosition[2][0]
        hitPoint[2][0] = - self.sinTheta * payload.WorldPosition[0][0] + self.cosTheta * payload.WorldPosition[2][0]

        normal[0][0] = self.cosTheta * payload.WorldNormal[0][0] + self.sinTheta * payload.WorldNormal[2][0]
        normal[2][0] = - self.sinTheta * payload.WorldNormal[0][0] + self.cosTheta * payload.WorldNormal[2][0]

        payload.WorldPosition = hitPoint
        payload.set_face_normal(rotatedRay, normal)

        return payload, True
