import numpy as np
from raypy.utils.vector3 import vec3
from abc import abstractmethod

def random_in_unit_sphere(shape):
    #https://mathworld.wolfram.com/SpherePointPicking.html
    phi = np.random.rand(shape)*2*np.pi
    u = 2.*np.random.rand(shape) - 1.
    r = np.sqrt(1-u**2)
    return vec3( r*np.cos(phi),  r*np.sin(phi), u)


class PDF:
    """Probability density function"""
    @abstractmethod
    def value(self,ray_dir):
        """get probability density function value at direction ray_dir"""
        pass

    @abstractmethod
    def generate(self):
        """generate random ray  directions according the probability density function"""
        pass


class CosinePdf(PDF):
    """Probability density Function"""

    def __init__(self, shape, normal):
        self.shape = shape
        self.normal = normal

    def value(self, ray_dir):
        return np.clip(ray_dir.dot(self.normal), 0., 1.) / np.pi
        # for diffuse materials, the scattering PDF is cos(θ) / pi
        # which is the same as ray_dir.dot(normal) / pi

    def generate(self):
        ax_w = self.normal
        a = vec3.where(np.abs(ax_w.x) > 0.9, vec3(0, 1, 0), vec3(1, 0, 0))
        ax_v = ax_w.cross(a).normalize()
        ax_u = ax_w.cross(ax_v)

        phi = np.random.rand(self.shape) * 0.5 * np.pi
        theta = np.random.rand(self.shape) * 2 * np.pi

        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta)
        z = np.cos(phi)

        return ax_u * x + ax_v * y + ax_w * z