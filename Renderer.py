import Utils
from Sphere import Sphere
from Camera import Camera
import numpy as np

class Renderer:
    def __init__(self, camera : Camera, width, height):
        self.cam = camera
        self.width = width
        self.height = height
        self.sphere = Sphere(np.array([[0], [0], [0]]), 1.0)


    def PerPixel(self, x: int, y: int) -> np.ndarray:

        rayDirection = self.cam.rayDirections[x + y * self.width]
        rayOrigin = self.cam.position
        origin = np.atleast_2d(rayOrigin).T - self.sphere.center

        # a * t² + b * t + c
        a = np.dot(rayDirection.T, rayDirection)
        b = 2.0 * np.dot(rayDirection.T, origin)
        c = np.dot(origin.T, origin) - np.square(self.sphere.radius)

        discriminant = np.square(b) - 4.0 * a * c
        if discriminant >= 0:
            minT = (-b - np.sqrt(discriminant)) / 2*a
            if(minT > 0):
                hitPoint = np.atleast_2d(rayOrigin).T + minT * rayDirection
                normal = Utils.normalize(hitPoint - self.sphere.center)
                return np.array([normal[0][0], normal[1][0], normal[2][0]]) * 0.5 + 0.5
        return np.array([0, 0, 0])