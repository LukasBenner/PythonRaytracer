from Camera import Camera
import numpy as np
import matplotlib.pyplot as plt
from Renderer import Renderer

width = 600
height = 300
camPosition = np.array([0,0,3])
camDirection = np.array([0,0,-1])

cam = Camera(60.0, camPosition, camDirection, width, height)
cam.CalculateRayDirections()

image = np.zeros((height, width, 3))
renderer = Renderer(cam, width, height)

for y in range(0, height):
    for x in range(0, width):
        ray = cam.rayDirections[x + y * width]
        image[y,x] = renderer.PerPixel(x, y)
    print("progress: %d/%d" % (y + 1, height))

image = np.flipud(image)
plt.imsave('image.png', image)
