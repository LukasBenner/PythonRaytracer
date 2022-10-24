import time

import matplotlib.pyplot as plt

from Box import Box
from Camera import Camera
from Hittable import Hittable
from Material import *
from Renderer import Renderer
from Scene import Scene
from Sphere import Sphere
from Texture import *
from Rect import *

width = 600
height = 600
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
objects.append(XZRect(213, 343, -332, -227, 553, light)) #light
objects.append(Box(np.array([[130],[0],[-230]]), np.array([[295],[165],[-65]]), red))
objects.append(Box(np.array([[265],[0],[-460]]), np.array([[430],[300],[-295]]), green))

scene = Scene(objects)

start = time.time()
renderer.RenderParallel(cam, scene)
end = time.time()

print("The time of execution of above program is :",
      (end - start) * 10 ** 3, "ms")

image = np.flipud(renderer.image)
plt.imsave('image.png', image)
