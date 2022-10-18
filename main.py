from Camera import Camera
from Sphere import Sphere
from Scene import Scene
import numpy as np
import matplotlib.pyplot as plt
from Renderer import Renderer

width = 600
height = 300
camPosition = np.array([[0],[0],[3]])
camDirection = np.array([[0],[0],[-1]])

cam = Camera(45.0, camPosition, camDirection, width, height)
cam.CalculateRayDirections()

renderer = Renderer(width, height)

spheres = list()
spheres.append(Sphere(np.array([[-1], [0], [0]]), 0.5, np.array([[0.5], [1], [0]])))
spheres.append(Sphere(np.array([[1], [0], [0]]), 0.5, np.array([[1], [0], [0.5]])))
spheres.append(Sphere(np.array([[0], [-100.5], [0]]), 100.0, np.array([[0], [0.5], [0]])))

scene = Scene(spheres)

renderer.Render(cam, scene)

image = np.flipud(renderer.image)
plt.imsave('image.png', image)
