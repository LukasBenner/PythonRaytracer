import Utils
from Sphere import Sphere
from Camera import Camera
import numpy as np
from dataclasses import dataclass


@dataclass
class HitPayload:
    HitDistance: float = 0.0
    WorldPosition: np.ndarray = np.zeros((1, 3, 1))
    WorldNormal: np.ndarray = np.zeros((1, 3, 1))
    ObjectIndex: int = 0


@dataclass
class Ray:
    Origin: np.ndarray
    Direction: np.ndarray

class Renderer:
    def __init__(self, camera : Camera, width, height):
        self.cam = camera
        self.width = width
        self.height = height


    def PerPixel(self, x: int, y: int) -> np.ndarray:

        rayDirection = self.cam.rayDirections[x + y * self.width]
        rayOrigin = self.cam.position
        ray = Ray(rayOrigin, rayDirection)

        color = np.array([0,0,0])
        multiplier = 1.0

        hitPayload = self.TraceRay(ray)

        if hitPayload.HitDistance < 0.0:
            skyColor = np.array([0.0, 0.0, 0.0])
            color = color + skyColor * multiplier
            return color

        normal = hitPayload.WorldNormal

        color = np.array([normal[0][0], normal[1][0], normal[2][0]])
        color = np.clip(color, 0.0, 1.0)
        return color



    def TraceRay(self, ray: Ray):
        closestSphere = -1
        hitDistance = float("inf")

        sphere = Sphere(np.array([[0], [0], [0]]), 1.0)

        origin = ray.Origin - sphere.position

        # a * t² + b * t + c
        a = np.dot(ray.Direction.T, ray.Direction)
        b = 2.0 * np.dot(ray.Direction.T, origin)
        c = np.dot(origin.T, origin) - np.square(sphere.radius)

        discriminant = np.square(b) - 4.0 * a * c

        if discriminant < 0:
            return self.Miss(ray)

        closestT = (-b - np.sqrt(discriminant)) / (2 * a)
        if (closestT > 0 and closestT < hitDistance):
            hitDistance = closestT

            return self.ClosestHit(ray, hitDistance, closestSphere)


    def ClosestHit(self, ray: Ray, hitDistance, objectIndex):


        closestSphere = Sphere(np.array([[0], [0], [0]]), 1.0)

        origin = ray.Origin - closestSphere.position
        worldPosition = origin + ray.Direction * hitDistance
        worldNormal = Utils.normalize(worldPosition)

        worldPosition = worldPosition + closestSphere.position

        return HitPayload(hitDistance, worldPosition, worldNormal, objectIndex)

    def Miss(self, ray:Ray):
        return HitPayload(-1.0)