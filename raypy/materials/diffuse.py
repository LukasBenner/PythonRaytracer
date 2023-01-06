import numpy as np

from raypy.random import CosinePdf, SphericalCapsPdf, MixedPdf
from raypy.materials.material import Material
from raypy.textures.texture import Texture, SolidColor
from raypy.utils.vector3 import vec3, rgb
from raypy.ray import get_ray_color, Ray


class Diffuse(Material):
  def __init__(self, diff_color, diffuse_rays = 20, ambient_weight = 0.5, **kwargs):
        super().__init__(**kwargs)

        if isinstance(diff_color, vec3):
            self.diff_texture = SolidColor(diff_color)
        elif isinstance(diff_color, Texture):
            self.diff_texture = diff_color

        self.diffuse_rays = diffuse_rays
        self.max_diffuse_reflections = 2
        self.ambient_weight = ambient_weight

  def get_color(self, scene, ray, hit):
      hit.point = (ray.origin + ray.dir * hit.distance) # intersection point
      diff_color = self.diff_texture.get_color(hit)

      N = hit.material.get_normal(hit)  

      color = rgb(0.,0.,0.)

      if ray.diffuse_reflections < 1:

          nudged = hit.point + N * .000001
          N_repeated = N.repeat(self.diffuse_rays)

          if ray.n.shape() == 1:
              n_repeated = ray.n
          else:
              n_repeated = ray.n.repeat(self.diffuse_rays)

          nudged_repeated = nudged.repeat(self.diffuse_rays)

          size = N.shape()[0] * self.diffuse_rays

          pdf1 = CosinePdf(size, N_repeated)
          pdf2 = SphericalCapsPdf(size, nudged_repeated, scene.importance_sampled_list)
          s_pdf = None
          if scene.importance_sampled_list == []:
              s_pdf = CosinePdf(size, N_repeated)
          else:
              s_pdf = MixedPdf(size, pdf1, pdf2, self.ambient_weight)

          ray_dir = s_pdf.generate()
          PDF_val = s_pdf.value(ray_dir)

          s_direction = np.clip(ray_dir.dot(N_repeated),0.,1.) / (np.pi)
          
          color_direction = get_ray_color(
            Ray(nudged_repeated, ray_dir, 
              ray.depth + 1, 
              n_repeated, 
              ray.reflections + 1, 
              ray.transmissions, 
              ray.diffuse_reflections + 1), 
            scene)
          color_temp = color_direction * s_direction  / PDF_val  #  diff_color/np.pi = Lambertian BRDF
          color += diff_color * color_temp.reshape(N.shape()[0], self.diffuse_rays).mean(axis = 1)

          return color

      elif ray.diffuse_reflections < self.max_diffuse_reflections:
          """
          when ray.diffuse_reflections > 1 we just call one diffuse ray to solve rendering equation (otherwise is too slow)
          """
          
          nudged = hit.point + N * .000001
          size = N.shape()[0] 
          s_pdf = None
          pdf1 = CosinePdf(size, N)
          pdf2 = SphericalCapsPdf(size, nudged, scene.importance_sampled_list)

          if scene.importance_sampled_list == []:
              s_pdf = CosinePdf(size, N)
          else:
              s_pdf = MixedPdf(size, pdf1, pdf2, self.ambient_weight)

          ray_dir = s_pdf.generate()
          PDF_val = s_pdf.value(ray_dir)

          s_direction = np.clip(N.dot(ray_dir),0.,1.)
          color_temp = diff_color * get_ray_color(Ray(nudged, ray_dir, ray.depth + 1, ray.n, ray.reflections + 1, ray.transmissions, ray.diffuse_reflections + 1), scene)
          color = color_temp * s_direction  / PDF_val / (np.pi) 

          return color

      else:
          return color