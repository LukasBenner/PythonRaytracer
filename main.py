from Camera import Camera
from Hittable import Hittable
from Sphere import Sphere
from Scene import Scene
import matplotlib.pyplot as plt
from Renderer import Renderer
from Material import *
import time

width = 600
height = 400
camPosition = np.array([[-4],[4],[2]])
camLookat = np.array([[0],[1],[0]])

cam = Camera(60.0, camPosition, camLookat, width, height, antiAliasing=False)
cam.CalculateRayDirections()

renderer = Renderer(width, height)

objects = list[Hittable]()
objects.append(Sphere(np.array([[0], [-1000], [0]]), 1000.0, np.array([[0.5], [0.5], [0.5]]), Material=Lambertian()))
objects.append(Sphere(np.array([[0], [1], [0]]), 1, np.array([[0.8], [0.2], [0]]), Material=Metal(0.2)))
objects.append(Sphere(np.array([[-2], [1], [0]]), 1.0, np.array([[0.8], [0.8], [0.8]]), Material=Dielectric(1.5)))
objects.append(Sphere(np.array([[-2], [1], [0]]), -0.95, np.array([[0.8], [0.8], [0.8]]), Material=Dielectric(1.5)))
objects.append(Sphere(np.array([[2], [1], [0]]), 1, np.array([[0.8], [0.2], [0.2]]), Material=Lambertian()))


scene = Scene(objects)

start = time.time()
renderer.RenderParallel(cam, scene)
end = time.time()

print("The time of execution of above program is :",
      (end-start) * 10**3, "ms")

image = np.flipud(renderer.image)
plt.imsave('image.png', image)
