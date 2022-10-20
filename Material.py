import abc
import numpy as np
import Utils
from HitPayload import HitPayload
from Ray import Ray


class Material(abc.ABC):
    def scatter(self, albedo, rayIn: Ray, hitPayload: HitPayload) -> (Ray, np.ndarray((3,1)), bool):
        pass

class Lambertian(Material):
    def scatter(self, albedo, rayIn: Ray, hitPayload: HitPayload) -> (Ray, np.ndarray((3,1)), bool):
        scatter_direction = hitPayload.WorldNormal + Utils.randomUnitVector()

        if Utils.near_zero(scatter_direction):
            scatter_direction = hitPayload.WorldNormal

        attenuation = albedo
        scattered = Ray(hitPayload.WorldPosition, scatter_direction)

        return scattered, attenuation, True

class Metal(Material):
    def __init__(self, fuzziness):
        self.fuzziness = fuzziness if fuzziness < 1.0 else 1.0
    def scatter(self, albedo, rayIn: Ray, hitPayload: HitPayload) -> (Ray, np.ndarray((3, 1)), bool):
        reflected = Utils.reflect(rayIn.Direction, hitPayload.WorldNormal)
        scattered = Ray(hitPayload.WorldPosition, reflected + self.fuzziness * Utils.randomInUnitSphere())
        attenuation = albedo
        success = np.dot(scattered.Direction.T, hitPayload.WorldNormal) > 0
        return scattered, attenuation, success


class Dielectric(Material):

    def __init__(self, indexOfRefraction):
        self.ir = indexOfRefraction

    def scatter(self, albedo, rayIn: Ray, hitPayload: HitPayload) -> (Ray, np.ndarray((3, 1)), bool):
        attenuation = np.array([[1.0],[1.0],[1.0]])
        refractionRate = 1.0/self.ir if hitPayload.FrontFace else self.ir

        unitDirection = Utils.normalize(rayIn.Direction)
        cos_theta = np.fmin(np.dot(-unitDirection.T, hitPayload.WorldNormal), 1.0)
        sin_theta = np.sqrt(1.0 - np.square(cos_theta))

        cannot_refract = refractionRate * sin_theta > 1.0

        if cannot_refract or self.__reflectance(cos_theta, refractionRate) > Utils.randomDouble():
            direction = Utils.reflect(unitDirection, hitPayload.WorldNormal)
        else:
            direction = Utils.refract(unitDirection, hitPayload.WorldNormal, refractionRate)

        scattered = Ray(hitPayload.WorldPosition, direction)
        return scattered, attenuation, True


    def __reflectance(self, cosine, ref_idx):
        r0 = (1-ref_idx) / (1+ref_idx)
        r0 = np.square(r0)
        return r0 + (1-r0) * np.power((1-cosine), 5)