from abc import abstractmethod


class Collider:
    def __init__(self, assigned_primitive, center):
        self.assigned_primitive = assigned_primitive
        self.center = center

    @abstractmethod
    def intersect(self, origin, direction):
        pass

    @abstractmethod
    def get_normal(self, hit):
        pass
