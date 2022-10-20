from Camera import Camera
from Sphere import Sphere
from Scene import Scene
import matplotlib.pyplot as plt
from Renderer import Renderer
from Material import *
import time

width = 600
height = 400
camPosition = np.array([[0],[2],[5]])
camLookat = np.array([[0],[1],[0]])

cam = Camera(60.0, camPosition, camLookat, width, height, antiAliasing=False)
cam.CalculateRayDirections()

renderer = Renderer(width, height)

spheres = list()
spheres.append(Sphere(np.array([[0], [-1000], [0]]), 1000.0, np.array([[0.5], [0.5], [0.5]]), Material=Lambertian()))
spheres.append(Sphere(np.array([[0], [1], [0]]), 1, np.array([[0], [0], [0]]), Material=Dielectric(1.5)))
spheres.append(Sphere(np.array([[-2], [1], [0]]), 1, np.array([[0.8], [0.8], [0.8]]), Material=Metal(0.0)))
spheres.append(Sphere(np.array([[2], [1], [0]]), 1, np.array([[0.8], [0.2], [0.2]]), Material=Lambertian()))


scene = Scene(spheres)

start = time.time()
renderer.RenderParallel(cam, scene)
end = time.time()

print("The time of execution of above program is :",
      (end-start) * 10**3, "ms")

image = np.flipud(renderer.image)
plt.imsave('image.png', image)
