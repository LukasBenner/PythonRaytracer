from abc import ABC
from Ray import Ray
from dataclasses import dataclass


@dataclass
class Hittable(ABC):
    def hit(self, ray: Ray) -> float:
        pass
