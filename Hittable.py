from abc import ABC
from dataclasses import dataclass

from HitPayload import HitPayload
from Ray import Ray


@dataclass
class Hittable(ABC):
    def hit(self, ray: Ray, payload: HitPayload, t_min, t_max) -> tuple[HitPayload, bool]:
        pass
