import Utils
from Sphere import Sphere
from Camera import Camera
import numpy as np
from Scene import Scene
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
    def __init__(self, width, height):
        self.cam = None
        self.scene = None
        self.width = width
        self.height = height
        self.image = None

    def Render(self, cam: Camera, scene : Scene):

        self.cam = cam
        self.scene = scene
        self.image = np.zeros((self.height, self.width, 3))

        for y in range(0, self.height):
            for x in range(0, self.width):
                color = self.PerPixel(x, y)
                color = np.clip(color, 0.0, 1.0)
                self.image[y, x] = color
            print("progress: %d/%d" % (y + 1, self.height))



    def PerPixel(self, x: int, y: int) -> np.ndarray:

        rayDirection = self.cam.rayDirections[x + y * self.width]
        rayOrigin = self.cam.Position
        ray = Ray(rayOrigin, rayDirection)

        color = np.array([[0], [0], [0]])
        multiplier = 1.0

        hitPayload = self.TraceRay(ray)

        if hitPayload.HitDistance < 0.0:
            skyColor = np.array([[0], [0], [0]])
            color = color + skyColor * multiplier
            return Utils.toColor(color)


        lightSource = np.array([[2],[2],[2]])

        sphere = self.scene.Spheres[hitPayload.ObjectIndex]

        lightDir = Utils.normalize(sphere.Position - lightSource)
        lightIntensity = np.max(np.dot(hitPayload.WorldNormal.T, -lightDir), 0)

        sphereColor = sphere.Albedo
        sphereColor = sphereColor * lightIntensity
        color = color + sphereColor * multiplier

        multiplier = multiplier * 0.77
        return Utils.toColor(color)

    def TraceRay(self, ray: Ray):
        closestSphere = -1
        hitDistance = float("inf")

        for i in range(0, len(self.scene.Spheres)):
            sphere = self.scene.Spheres[i]
            origin = ray.Origin - sphere.Position

            # a * t² + b * t + c
            a = np.dot(ray.Direction.T, ray.Direction)
            b = 2.0 * np.dot(ray.Direction.T, origin)
            c = np.dot(origin.T, origin) - np.square(sphere.Radius)

            discriminant = np.square(b) - 4.0 * a * c

            if discriminant < 0:
                continue

            closestT = (-b - np.sqrt(discriminant)) / (2 * a)
            if (closestT > 0 and closestT < hitDistance):
                hitDistance = closestT
                closestSphere = i

        if closestSphere < 0:
            return self.Miss(ray)

        return self.ClosestHit(ray, hitDistance, closestSphere)

    def ClosestHit(self, ray: Ray, hitDistance, objectIndex):

        closestSphere = self.scene.Spheres[objectIndex]

        origin = ray.Origin - closestSphere.Position
        worldPosition = origin + ray.Direction * hitDistance
        worldNormal = Utils.normalize(worldPosition)

        worldPosition = worldPosition + closestSphere.Position

        return HitPayload(hitDistance, worldPosition, worldNormal, objectIndex)

    def Miss(self, ray: Ray):
        return HitPayload(-1.0)
