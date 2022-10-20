from abc import ABC

from HitPayload import HitPayload
from Ray import Ray
from dataclasses import dataclass


@dataclass
class Hittable(ABC):
    def hit(self, ray: Ray, payload: HitPayload, t_min, t_max) -> tuple[HitPayload, bool]:
        pass
