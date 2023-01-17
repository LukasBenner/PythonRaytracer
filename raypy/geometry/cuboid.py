import numpy as np
from ..utils.constants import *
from ..utils.vector3 import vec3
from .collider import Collider
from .primitive import Primitive

class Cuboid(Primitive):
    def __init__(self, center, material, width, height, length, shadow=True, ):
        super().__init__(center, material, shadow)
        self.width = width
        self.height = height
        self.length = length

        self.collider_list += [
            Cuboid_Collider(center=center, width=width, height=height, length=length, assigned_primitive=self)
        ]


class Cuboid_Collider(Collider):
    def __init__(self, width, height, length, **kwargs):
        super().__init__(**kwargs)

        self.leftBottom = self.center - vec3(width/2, height/2, length/2)
        self.rightTop = self.center + vec3(width/2, height/2, length/2)

        self.lb_local_basis = self.leftBottom
        self.rt_local_basis = self.rightTop

        self.width = width
        self.height = height
        self.length = length

        # basis vectors
        self.ax_w = vec3(1.,0.,0.)
        self.ax_h = vec3(0.,1.,0.)
        self.ax_l = vec3(0.,0.,1.)

        self.inverse_basis_matrix = np.array([[self.ax_w.x,       self.ax_h.x,         self.ax_l.x],
                                              [self.ax_w.y,       self.ax_h.y,         self.ax_l.y],
                                              [self.ax_w.z,       self.ax_h.z,         self.ax_l.z]])

        self.basis_matrix = self.inverse_basis_matrix.T

    def rotate(self, matrix, center):
        # rotate the basis of the cube
        self.ax_w = self.ax_w.matmul(matrix)
        self.ax_h = self.ax_h.matmul(matrix)
        self.ax_l = self.ax_l.matmul(matrix)

        self.inverse_basis_matrix = np.array([[self.ax_w.x,       self.ax_h.x,         self.ax_l.x],
                                              [self.ax_w.y,       self.ax_h.y,         self.ax_l.y],
                                              [self.ax_w.z,       self.ax_h.z,         self.ax_l.z]])
        self.basis_matrix = self.inverse_basis_matrix.T

        # adjust corners
        self.leftBottom = center + (self.leftBottom-center).matmul(matrix)
        self.rightTop = center + (self.rightTop-center).matmul(matrix)

        self.lb_local_basis = self.leftBottom.matmul(self.basis_matrix)
        self.rt_local_basis = self.rightTop.matmul(self.basis_matrix)

    def intersect(self, origin, direction):

        originBasis = origin.matmul(self.basis_matrix)
        directionBasis = direction.matmul(self.basis_matrix)

        frac = 1.0 / directionBasis
  
        # leftBottomBasis is the corner of AABB with minimal coordinates - left bottom, rightTopBasis is maximal corner
        t1 = (self.lb_local_basis.x - originBasis.x)*frac.x;
        t2 = (self.rt_local_basis.x - originBasis.x)*frac.x;
        t3 = (self.lb_local_basis.y - originBasis.y)*frac.y;
        t4 = (self.rt_local_basis.y - originBasis.y)*frac.y;
        t5 = (self.lb_local_basis.z - originBasis.z)*frac.z;
        t6 = (self.rt_local_basis.z - originBasis.z)*frac.z;

        tMin = np.maximum(np.maximum(np.minimum(t1, t2), np.minimum(t3, t4)), np.minimum(t5, t6))
        tMax = np.minimum(np.minimum(np.maximum(t1, t2), np.maximum(t3, t4)), np.maximum(t5, t6))

        # if tMax < 0, is intersecting, but the AABB behind
        # if tMin > tMax, doesn't intersect
        p1 = (tMax < 0) | (tMin > tMax)

        # if tmin < 0 then the ray origin is inside of the AABB and tmin is behind the start of the ray so tmax is the first intersection
        p2 = tMin < 0
        return np.select([p1,p2, True] , [FARAWAY , [tMax,  np.tile(UPDOWN, tMin.shape)] ,  [tMin,  np.tile(UPWARDS, tMin.shape)]])


    def get_normal(self, hit):
        P = (hit.point-self.center).matmul(self.basis_matrix)
        absP = vec3(1./self.width, 1./self.height, 1./self.length)*np.abs(P)
        Pmax = np.maximum(np.maximum(absP.x, absP.y), absP.z)
        P.x = np.where(Pmax == absP.x, np.sign(P.x),  0.)
        P.y = np.where(Pmax == absP.y, np.sign(P.y),  0.)
        P.z = np.where(Pmax == absP.z, np.sign(P.z),  0.)
        return P.matmul(self.inverse_basis_matrix)