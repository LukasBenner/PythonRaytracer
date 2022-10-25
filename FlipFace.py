from HitPayload import HitPayload
from Hittable import Hittable
from Ray import Ray
from Material import Material

import numpy as np
from dataclasses import dataclass, field

@dataclass()
class FlipFace(Hittable):
    Object: Hittable
    Material: Material = field(init=False)


    def __post_init__(self):
        self.Material = self.Object.Material

    def hit(self, ray: Ray, payload: HitPayload, t_min, t_max) -> tuple[HitPayload, bool]:
        payload, success = self.Object.hit(ray, payload, t_min, t_max)

        if not success:
            return payload, False

        payload.FrontFace = not payload.FrontFace

        return payload, True
