from Camera import Camera
from Sphere import Sphere
from Scene import Scene
import numpy as np
import matplotlib.pyplot as plt
from Renderer import Renderer
from Material import *

width = 600
height = 300
camPosition = np.array([[0],[0],[2.5]])
camDirection = np.array([[0],[0],[-1]])

cam = Camera(60.0, camPosition, camDirection, width, height)
cam.CalculateRayDirections()

renderer = Renderer(width, height)

spheres = list()
spheres.append(Sphere(np.array([[-1.5], [0], [0]]), 0.5, np.array([[0.5], [1], [0]]), Material=Lambertian()))
spheres.append(Sphere(np.array([[1.5], [0], [0]]), 0.5, np.array([[0.5], [1], [1]]), Material=Lambertian()))
spheres.append(Sphere(np.array([[0], [0], [0]]), 0.5, np.array([[1], [0], [0]]), Material=Metal()))
spheres.append(Sphere(np.array([[0], [-100.5], [0]]), 100.0, np.array([[0], [0.5], [0]]), Material=Lambertian()))

scene = Scene(spheres)

renderer.Render(cam, scene)

image = np.flipud(renderer.image)
plt.imsave('image.png', image)
