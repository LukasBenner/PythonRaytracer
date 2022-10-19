import Utils
from Camera import Camera
import numpy as np
from Scene import Scene
from dataclasses import dataclass


@dataclass
class Ray:
    Origin: np.ndarray
    Direction: np.ndarray


@dataclass
class HitPayload:
    HitDistance: float = 0.0
    WorldPosition: np.ndarray = np.zeros((1, 3, 1))
    WorldNormal: np.ndarray = np.zeros((1, 3, 1))
    ObjectIndex: int = 0
    FrontFace: bool = True

    def set_face_normal(self, r: Ray, outward_normal: np.ndarray((3,1))):
        self.FrontFace = np.dot(r.Direction.T, outward_normal) < 0
        self.WorldNormal = outward_normal if self.FrontFace else -outward_normal


class Renderer:
    def __init__(self, width, height):
        self.cam = None
        self.scene = None
        self.width = width
        self.height = height
        self.image = None

    def Render(self, cam: Camera, scene: Scene):

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
        sampledColor = np.array([[0], [0], [0]])
        rayOrigin = self.cam.Position

        for sample in range(0, self.cam.numberSamples):

            rayDirection = self.cam.rayDirections[x + y * self.width][sample]

            ray = Ray(rayOrigin, rayDirection)
            color = np.array([[0], [0], [0]])
            multiplier = 1.0

            bounces = 10

            for i in range(0, bounces):

                hitPayload = self.TraceRay(ray)

                if hitPayload.HitDistance < 0.0:
                    skyColor = np.array([[0.678], [0.847], [0.901]])
                    color = color + skyColor * multiplier
                    break

                sphere = self.scene.Spheres[hitPayload.ObjectIndex]

                sphereColor = sphere.Albedo
                color = color + sphereColor * multiplier

                multiplier = multiplier * 0.5

                ray.Origin = hitPayload.WorldPosition + hitPayload.WorldNormal * 0.0001

                #diffuse
                target = ray.Origin + hitPayload.WorldNormal + Utils.randomUnitVector()
                ray.Direction = target - ray.Origin
                #reflective
                #ray.Direction = Utils.reflect(ray.Direction, hitPayload.WorldNormal)

            sampledColor = sampledColor + color

        return Utils.toColor(sampledColor / self.cam.numberSamples)

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
            if closestT > 0.001 and closestT < hitDistance:
                hitDistance = closestT
                closestSphere = i

        if closestSphere < 0:
            return self.Miss(ray)

        return self.ClosestHit(ray, hitDistance, closestSphere)

    def ClosestHit(self, ray: Ray, hitDistance, objectIndex):

        payload = HitPayload()

        closestSphere = self.scene.Spheres[objectIndex]

        payload.ObjectIndex = objectIndex
        payload.HitDistance = hitDistance

        worldPosition = ray.Origin + hitDistance * ray.Direction
        outwardNormal = (worldPosition - closestSphere.Position) / closestSphere.Radius
        payload.set_face_normal(ray, outwardNormal)
        payload.WorldPosition = worldPosition

        return payload

    def Miss(self, ray: Ray):
        return HitPayload(-1.0)
