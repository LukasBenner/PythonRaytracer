from abc import abstractmethod


class Material:
    def __init__(self):
        pass

    def get_normal(self, hit):
        collider_normal = hit.collider.get_normal(hit)
        return collider_normal * hit.orientation

    @abstractmethod
    def get_color(self, scene, ray, hit):
        pass