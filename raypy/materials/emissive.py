from raypy.materials.material import Material
from raypy.textures.texture import SolidColor


class Emissive(Material):
    def __init__(self, color,):
        super().__init__()
        self.texture_color = SolidColor(color)


    def get_color(self, scene, ray, hit):
        return self.texture_color.get_color(hit)