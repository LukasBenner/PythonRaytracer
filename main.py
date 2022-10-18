from Camera import Camera
import numpy as np
import matplotlib.pyplot as plt
from Renderer import Renderer

width = 600
height = 300
camPosition = np.array([[0],[0],[3]])
camDirection = np.array([[0],[0],[-1]])

cam = Camera(60.0, camPosition, camDirection, width, height)
cam.CalculateRayDirections()

renderer = Renderer(width, height)

renderer.Render(cam)

image = np.flipud(renderer.image)
plt.imsave('image.png', image)
