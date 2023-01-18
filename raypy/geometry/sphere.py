import numpy as np

from .primitive import Primitive
from .collider import Collider

from raypy.utils.constants import *


class Sphere(Primitive):
    def __init__(self, center, material, radius, shadow=True):
        super().__init__(center, material, shadow)
        self.collider_list += [SphereCollider(assigned_primitive=self, center=center, radius=radius)]
        self.bounded_sphere_radius = radius

    def get_uv(self, hit):
        return hit.collider.get_uv(hit)


class SphereCollider(Collider):
    def __init__(self,  radius, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius

    def intersect(self, origin, direction):
        b = 2 * direction.dot(origin - self.center)
        c = self.center.square_length() + origin.square_length() - 2 * self.center.dot(origin) - (self.radius * self.radius)
        discriminant = (b ** 2) - (4 * c)
        # we will handle the case discriminant < 0 later
        # We can't just exit when discriminant is < 0 because we are doing matrix calculations to calculate all ray intersections at once
        sq = np.sqrt(np.maximum(0, discriminant))
        h0 = (-b - sq) / 2
        h1 = (-b + sq) / 2
        h = np.where((h0 > 0) & (h0 < h1), h0, h1)
        intersectionPoint = (origin + direction * h)
        surfaceNormal = ((intersectionPoint - self.center) * (1. / self.radius))
        ## calculate if the normal and the ray direction point against each other or in the same direction
        normalDirection = surfaceNormal.dot(direction)

        pred1 = (discriminant > 0) & (h > 0) & (normalDirection > 0)
        pred2 = (discriminant > 0) & (h > 0) & (normalDirection < 0)
        pred3 = True

        # return an array with hit distance and the hit orientation
        # because we did some matrix multiplications, we now have to select the correct distances
        return np.select([pred1, pred2, pred3],
                         [[h, np.tile(UPDOWN, h.shape)], [h, np.tile(UPWARDS, h.shape)], FARAWAY])

    def get_normal(self, hit):
        return (hit.point - self.center) / self.radius