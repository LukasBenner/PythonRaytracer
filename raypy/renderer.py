from alive_progress import alive_bar

from raypy.ray import get_ray_color
from PIL import Image
import numpy as np
from raypy.utils import color_functions as cf
from raypy.utils.vector3 import rgb


class Renderer():
    def __init__(self, scene):
        self.samples = 10
        self.scene = scene

    def render(self, samples: int):
        self.samples = samples

        color = rgb(0.,0.,0.)
        with alive_bar(total=self.samples) as bar:
            for i in range(self.samples):
                ray = self.scene.camera.get_ray(self.scene.n)
                color += get_ray_color(ray, self.scene)
                bar()

            color = color / self.samples

        color = cf.sRGB_linear_to_sRGB(color.to_array())

        img_RGB = []
        width = self.scene.camera.screen_width
        height = self.scene.camera.screen_height
        for c in color:
            # create an image layer from every rgb channel
            img_RGB += [Image.fromarray((255 * np.clip(c, 0, 1).reshape((height, width))).astype(np.uint8), "L")]

        img = Image.merge("RGB", img_RGB)
        return img
