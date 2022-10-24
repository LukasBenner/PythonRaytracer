from HitPayload import HitPayload
from Hittable import Hittable
from Material import Material
from Ray import Ray
from dataclasses import dataclass, field
import numpy as np

from Rect import XYRect, XZRect, YZRect


@dataclass(order=True)
class Box(Hittable):
    p0: np.ndarray((3,1))
    p1: np.ndarray((3,1))
    Material: Material
    sides: list = field(init=False)

    def __post_init__(self):
        self.sides = list[Hittable]()
        self.sides.append(XYRect(self.p0[0][0], self.p1[0][0],
                                 self.p0[1][0], self.p1[1][0],
                                 self.p1[2][0], self.Material))
        self.sides.append(XYRect(self.p0[0][0], self.p1[0][0],
                                 self.p0[1][0], self.p1[1][0],
                                 self.p0[2][0], self.Material))

        self.sides.append(XZRect(self.p0[0][0], self.p1[0][0],
                                 self.p0[2][0], self.p1[2][0],
                                 self.p1[1][0], self.Material))
        self.sides.append(XZRect(self.p0[0][0], self.p1[0][0],
                                 self.p0[2][0], self.p1[2][0],
                                 self.p0[1][0], self.Material))

        self.sides.append(YZRect(self.p0[1][0], self.p1[1][0],
                                 self.p0[2][0], self.p1[2][0],
                                 self.p1[0][0], self.Material))
        self.sides.append(YZRect(self.p0[1][0], self.p1[1][0],
                                 self.p0[2][0], self.p1[2][0],
                                 self.p0[0][0], self.Material))

    def hit(self, ray: Ray, payload: HitPayload, t_min, t_max) -> tuple[HitPayload, bool]:
        hitDistance = payload.HitDistance
        overallSuccess = False

        for i in range(0, len(self.sides)):
            object = self.sides[i]

            payload, success = object.hit(ray, payload, t_min, hitDistance)

            if success:
                overallSuccess = True
                hitDistance = payload.HitDistance

        return payload, overallSuccess