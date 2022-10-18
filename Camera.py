import numpy as np
import Utils


class Camera:
    def __init__(self, verticalFOV, position, forwardDirection, vpWidth, vpHeight):
        self.verticalFOV = verticalFOV
        self.viewPortWidth = vpWidth
        self.viewPortHeight = vpHeight
        self.forwardDirection = forwardDirection
        self.position = position

        self.neaClip = 0.1
        self.farClip = 100.0
        self.rayDirections = np.array(0)
        self.projection = np.array({1})
        self.inverseProjection = np.array({1})
        self.view = np.array({1})
        self.inverseView = np.array({1})

        self.__calculatePerspectiveProjectionMatrix()
        self.__calculateView()



    def __calculatePerspectiveProjectionMatrix(self):
        q = 1 / np.tan(np.radians(self.verticalFOV * 0.5))
        a = q / (self.viewPortWidth / self.viewPortHeight)
        b = (self.farClip + self.neaClip) / (self.neaClip - self.farClip)
        c = (2 * self.neaClip * self.farClip) / (self.neaClip - self.farClip)
        self.projection = np.array([[a, 0, 0, 0],
                                    [0, q, 0, 0],
                                    [0, 0, b, c],
                                    [0, 0, -1, 0]])
        self.inverseProjection = np.linalg.inv(self.projection)


    def __lookAt(self, eye: np.ndarray, center: np.ndarray, up: np.ndarray) -> np.ndarray:
        zaxis = Utils.normalize(eye - center)
        xaxis = Utils.normalize(np.cross(up, zaxis))
        yaxis = np.cross(zaxis, xaxis)

        return np.array([
            [xaxis[0], xaxis[1], xaxis[2], -np.dot(xaxis, eye)],
            [yaxis[0], yaxis[1], yaxis[2], -np.dot(yaxis, eye)],
            [zaxis[0], zaxis[1], zaxis[2], -np.dot(zaxis, eye)],
            [0, 0, 0, 1]
        ])

    def __calculateView(self):
        self.view = self.__lookAt(self.position, self.position + self.forwardDirection, np.array([0, 1, 0]))
        self.inverseView = np.linalg.inv(self.view)

    def CalculateRayDirections(self):
        self.rayDirections = np.ndarray((int(self.viewPortWidth * self.viewPortHeight), 3, 1))
        for y in range(0, int(self.viewPortHeight)):
            for x in range(0, int(self.viewPortWidth)):
                coord = np.array([float(x) / float(self.viewPortWidth), float(y) / float(self.viewPortHeight)])
                coord = coord * 2.0 - 1.0  # map to -1 - 1

                target = np.matmul(self.inverseProjection, np.array([[coord[0], coord[1], 1, 1]]).T)
                normalized = Utils.normalize(target[:3] / target[3])
                rayDirection = np.matmul(self.inverseView,
                                         np.array([[normalized[0][0], normalized[1][0], normalized[2][0], 0]]).T)
                self.rayDirections[(x + y * int(self.viewPortWidth))] = np.array(
                    [rayDirection[0], rayDirection[1], rayDirection[2]])
