import time

import matplotlib.pyplot as plt

from Camera import Camera
from Hittable import Hittable
from Material import *
from Renderer import Renderer
from Scene import Scene
from Sphere import Sphere
from Texture import *
from XYRect import XYRect

width = 600
height = 400
camPosition = np.array([[26], [3], [6]])
camLookat = np.array([[0], [2], [0]])

cam = Camera(20.0, camPosition, camLookat, width, height, antiAliasing=True)
cam.CalculateRayDirections()

renderer = Renderer(width, height)

objects = list[Hittable]()
objects.append(Sphere(np.array([[0], [-1000], [0]]), 1000.0, Material=Lambertian(0.5, 0.5, 0.5)))
objects.append(Sphere(np.array([[0], [2], [0]]), 2, Material=Metal(0.8, 0.2, 0, 0.2)))
difflight = DiffuseLight(SolidColor(4, 4, 4))
objects.append(XYRect(3, 5, 1, 3, -2, difflight))

scene = Scene(objects)

start = time.time()
renderer.RenderParallel(cam, scene)
end = time.time()

print("The time of execution of above program is :",
      (end - start) * 10 ** 3, "ms")

image = np.flipud(renderer.image)
plt.imsave('image.png', image)
