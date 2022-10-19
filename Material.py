import abc
import numpy as np
import Utils
from Renderer import HitPayload, Ray

class Material(abc.ABC):
    def scatter(self, albedo, rayIn: Ray, hitPayload: HitPayload) -> (Ray, np.ndarray((3,1)), bool):
        pass

class Lambertian(Material):
    def scatter(self, albedo, rayIn: Ray, hitPayload: HitPayload) -> (Ray, np.ndarray((3,1)), bool):
        scatter_direction = hitPayload.WorldNormal + Utils.randomUnitVector()

        if Utils.near_zero(scatter_direction):
            scatter_direction = hitPayload.WorldNormal

        return Ray(hitPayload.WorldPosition, scatter_direction), albedo, True

class Metal(Material):
    def scatter(self, albedo, rayIn: Ray, hitPayload: HitPayload) -> (Ray, np.ndarray((3, 1)), bool):
        reflected = Utils.reflect(rayIn.Direction, hitPayload.WorldNormal)
        scattered = Ray(hitPayload.WorldPosition, reflected)
        attenuation = albedo
        success = np.dot(scattered.Direction.T, hitPayload.WorldNormal) > 0
        return scattered, attenuation, success