from raypy.utils.constants import *
from raypy.utils.vector3 import extract, rgb
import numpy as np
from functools import reduce as reduce


class Ray:
    """Info of the ray and the media it's travelling"""

    def __init__(self, origin, dir, depth, n, reflections, transmissions, diffuse_reflections):
        self.origin = origin  # the point where the ray comes from
        self.dir = dir  # direction of the ray
        self.depth = depth  # ray_depth is the number of the refrections + transmissions/refractions, starting at zero for camera rays
        self.n = n  # ray_n is the index of refraction of the media in which the ray is travelling

        # Instead of defining a index of refraction (n) for each wavelenght (computationally expensive) we aproximate defining the index of refraction
        # using a vec3 for red = 630 nm, green 555 nm, blue 475 nm, the most sensitive wavelenghts of human eye.

        # Index a refraction is a complex number.
        # The real part is involved in how much light is reflected and model refraction direction via Snell Law.
        # The imaginary part of n is involved in how much light is reflected and absorbed. For non-transparent materials like metals is usually between (0.1j,3j)
        # and for transparent materials like glass is  usually between (0.j , 1e-7j)

        self.reflections = reflections  # reflections is the number of the refrections, starting at zero for camera rays
        self.transmissions = transmissions  # transmissions is the number of the transmissions/refractions, starting at zero for camera rays
        self.diffuse_reflections = diffuse_reflections  # reflections is the number of the refrections, starting at zero for camera rays

    def extract(self, hit_check):
        return Ray(self.origin.extract(hit_check), self.dir.extract(hit_check), self.depth, self.n.extract(hit_check),
                   self.reflections, self.transmissions, self.diffuse_reflections)


class Hit:
    """Info of the ray-surface intersection"""

    def __init__(self, distance, orientation, material, collider, surface):
        self.distance = distance
        self.orientation = orientation
        self.material = material
        self.collider = collider
        self.surface = surface
        self.u = None
        self.v = None
        self.N = None
        self.point = None

    def get_uv(self):
        if self.u is None:  # this is for prevent multiple computations of u,v
            self.u, self.v = self.collider.assigned_primitive.get_uv(self)
        return self.u, self.v

    def get_normal(self):
        if self.N is None:  # this is for prevent multiple computations of normal
            self.N = self.collider.get_normal(self)
        return self.N


def get_ray_color(ray, scene):
    intersects = [c.intersect(ray.origin, ray.dir) for c in scene.collider_list]
    # intersects every ray with every collider of the scene
    distances, hit_orientation = zip(*intersects)
    # intersects is a list which holds the intersection information of every ray per collider
    # an intersection information holds the distance and the hit_orientation

    nearest = reduce(np.minimum, distances)
    # from all distances for each collider, take the distance to the nearest collider
    color = rgb(0., 0., 0.)
    zipped = zip(scene.collider_list, distances, hit_orientation)
    # create tuples with collider, the distances of the collider and the orientations
    # one object in zipped is: [collider, []: distances, []: orientations ]

    for (coll, dis, orient) in zipped:
        hit_check = (nearest != FARAWAY) & (dis == nearest)
        # check if ray intersects a collider and then check if the current collider is that collider

        if np.any(hit_check):
            hit_info = Hit(extract(hit_check, dis), extract(hit_check, orient),
                           material=coll.assigned_primitive.material, collider=coll,
                           surface=coll.assigned_primitive)

            cc = hit_info.material.get_color(scene, ray.extract(hit_check), hit_info)
            color += cc.place(hit_check)

    return color
