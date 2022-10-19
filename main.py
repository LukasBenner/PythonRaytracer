from Camera import Camera
from Sphere import Sphere
from Scene import Scene
import matplotlib.pyplot as plt
from Renderer import Renderer
from Material import *

width = 480
height = 270
camPosition = np.array([[0],[0],[2]])
camLookat = np.array([[0],[0],[0]])

cam = Camera(60.0, camPosition, camLookat, width, height)
cam.CalculateRayDirections()

renderer = Renderer(width, height)

spheres = list()
spheres.append(Sphere(np.array([[0], [-100.5], [0]]), 100.0, np.array([[0.5], [0.5], [0.5]]), Material=Lambertian()))
spheres.append(Sphere(np.array([[0], [0], [0]]), 0.5, np.array([[0], [0.5], [0]]), Material=Lambertian()))
spheres.append(Sphere(np.array([[-1], [0], [0]]), 0.5, np.array([[0.8], [0.8], [0.8]]), Material=Metal()))


scene = Scene(spheres)

renderer.Render(cam, scene)

image = np.flipud(renderer.image)
plt.imsave('image.png', image)
