from abc import ABC
from aabb import aabb
from Ray import Ray
from dataclasses import dataclass


@dataclass
class Hittable(ABC):
    def boundingBox(self) -> (aabb, bool):
        pass

    def hit(self, ray: Ray) -> float:
        pass
