from dataclasses import dataclass
from Hittable import Hittable


@dataclass
class Scene:
    Objects : list[Hittable]