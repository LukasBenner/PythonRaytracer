from raypy.utils.vector3 import vec3
import numpy as np


class Primitive:
    def __init__(self, center, material, max_ray_depth=1, shadow=True):
        self.center = center
        self.material = material
        self.shadow = shadow
        self.collider_list = []
        self.max_ray_depth = max_ray_depth

    def rotate(self, theta, u: vec3):
        u = u.normalize()
        theta = theta / 180 * np.pi
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)

        matrix = np.array([
            [cos_theta + u.x * u.x * (1 - cos_theta), u.x * u.y * (1 - cos_theta) - u.z * sin_theta,
             u.x * u.z * (1 - cos_theta) + u.y * sin_theta],
            [u.y * u.x * (1 - cos_theta) + u.z * sin_theta, cos_theta + u.y ** 2 * (1 - cos_theta),
             u.y * u.z * (1 - cos_theta) - u.x * sin_theta],
            [u.z * u.x * (1 - cos_theta) - u.y * sin_theta, u.z * u.y * (1 - cos_theta) + u.x * sin_theta,
             cos_theta + u.z * u.z * (1 - cos_theta)]
        ])
        for c in self.collider_list:
            c.rotate(matrix, self.center)
