import numpy as np

import Utils


class Onb:

    def __init__(self):
        self.axis = np.zeros((3, 3, 1))

    def u(self):
        return self.axis[0]

    def v(self):
        return self.axis[1]

    def w(self):
        return self.axis[2]

    def local(self, a: float, b: float, c: float):
        return a * self.u() + b * self.v() + c * self.w()

    def localVec3(self, vec3: np.ndarray((3,1))):
        return vec3[0][0] * self.u() + vec3[1][0] * self.v() + vec3[2][0] * self.w()

    def buildFromW(self, n: np.ndarray((3,1))):
        self.axis[2] = Utils.normalize(n)
        a = np.array([[0], [1], [0]]) if np.fabs(self.w()[0][0]) > 0.9 else np.array([[1], [0], [0]])
        self.axis[1] = Utils.normalize(np.cross(self.w(), a, axis=0))
        self.axis[0] = np.cross(self.w(), self.v(), axis=0)