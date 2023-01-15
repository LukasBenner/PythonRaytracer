import numpy as np

from raypy.geometry.collider import Collider
from raypy.geometry.primitive import Primitive
from raypy.utils.constants import *
from raypy.utils.vector3 import vec3


class Plane(Primitive):
    def __init__(self, center, material, width, height, u_axis, v_axis, shadow=True):
        super().__init__(center, material, shadow)
        self.collider_list = [PlaneCollider(self, center, u_axis, v_axis, width/2, height/2)]
        self.width = width   
        self.height = height
        self.bounded_sphere_radius = np.sqrt((width/2)**2 + (height/2)**2)


class PlaneCollider(Collider):
    def __init__(self, assigned_primitive, center, u_axis, v_axis, w, h, uv_shift=(0, 0)):
        super().__init__(assigned_primitive, center)
        self.normal = u_axis.cross(v_axis).normalize()
        self.w = w
        self.h = h
        self.u_axis = u_axis
        self.v_axis = v_axis
        self.uv_shift = uv_shift

    def intersect(self, origin, direction):
        # https://samsymons.com/blog/math-notes-ray-plane-intersection/
        nominator = self.normal.dot(self.center - origin)
        denominator = self.normal.dot(direction)
        denominator = np.where(denominator == 0., 1e-6, denominator)

        distance = nominator / denominator

        point = origin + direction * distance
        vec_in_plane = point - self.center

        u = self.u_axis.dot(vec_in_plane)
        v = self.v_axis.dot(vec_in_plane)
        # projection from vec_in_plane on u_axis and v_axis

        hit_inside = (np.fabs(u) <= self.w) & (np.fabs(v) <= self.h) & (distance > 0)
        # distance has to be > 0, so we only consider hits in the positive direction
        hit_UPWARDS = (denominator < 0)   # we hit the plane against its normal vector
        hit_UPDOWN = np.logical_not(hit_UPWARDS)    # we hit the plane in the direction of its normal vector

        pred1 = hit_inside & hit_UPWARDS
        pred2 = hit_inside & hit_UPDOWN
        pred3 = True
        return np.select([pred1, pred2, pred3], [[distance, np.tile(UPWARDS, distance.shape)], [distance, np.tile(UPDOWN, distance.shape)], FARAWAY])

    def get_normal(self, hit):
        return self.normal

    def rotate(self, M, center):
        self.u_axis = self.u_axis.matmul(M)
        self.v_axis = self.v_axis.matmul(M)
        self.normal = self.normal.matmul(M)
        self.center = center + (self.center - center).matmul(M)