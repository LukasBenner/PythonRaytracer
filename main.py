from Camera import Camera
import numpy as np
import matplotlib.pyplot as plt

width = 800
height = 400

cam = Camera(60.0, 0.1, 100.0, width, height)
cam.CalculateView()
cam.PerspectiveProjectionMatrix()
cam.CalculateRayDirections()

image = np.zeros((height, width, 3))

for y in range(0, height):
    for x in range(0, width):
        print("progress: %d/%d" % (y + 1, height))
        ray = cam.rayDirections[x + y * width]
        color = np.array([ray[0][0], ray[1][0], 0]) * 0.5 + 0.5
        image[y,x] = np.clip(color, 0, 1)

image = np.flipud(image)
plt.imsave('image.png', image)