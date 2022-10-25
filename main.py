import time

import matplotlib.pyplot as plt

from Box import Box
from Camera import Camera
from FlipFace import FlipFace
from Material import *
from Renderer import Renderer
from RotateY import RotateY
from Scene import Scene
from Texture import *
from Rect import *

if __name__ == "__main__":

      width = 100
      height = 100
      camPosition = np.array([[278], [278], [800]])
      camLookat = np.array([[278], [278], [0]])


      cam = Camera(40.0, camPosition, camLookat, width, height)

      renderer = Renderer(width, height)

      red = Lambertian(.65, .05, .05)
      white = Lambertian(.73, .73, .73)
      green = Lambertian(.12, .45, .15)
      light = DiffuseLight(SolidColor(15,15,15))

      objects = list[Hittable]()
      objects.append(YZRect(0, 555, -555, 0, 0, green)) #left
      objects.append(YZRect(0, 555, -555, 0, 555, red)) #right
      objects.append(XZRect(0, 555, -555, 0, 0, white)) #floor
      objects.append(XZRect(0, 555, -555, 0, 555, white)) #ceiling
      objects.append(XYRect(0, 555, 0, 555, -555, white)) #back
      objects.append(FlipFace(XZRect(213, 343, -332, -227, 553, light))) #light
      box1 = Box(np.array([[130],[0],[-230]]), np.array([[295],[165],[-65]]), red)
      box2 = Box(np.array([[265],[0],[-460]]), np.array([[430],[300],[-295]]), green)
      objects.append(RotateY(box1, 15))
      objects.append(RotateY(box2, -18))

      scene = Scene(objects)

      start = time.time()
      # renderer.Render(cam, scene, background)
      renderer.RenderParallel(cam, scene)
      end = time.time()

      print("The time of execution of above program is :",
            (end - start) * 10 ** 3, "ms")

      image = np.flipud(renderer.image)
      plt.imsave('image.png', image)
