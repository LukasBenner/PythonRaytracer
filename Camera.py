import numpy as np
import Utils


class Camera:
    def __init__(self, verticalFOV, position, lookat, vpWidth, vpHeight):
        self.verticalFOV = verticalFOV
        self.viewPortWidth = vpWidth
        self.viewPortHeight = vpHeight
        self.lookat = lookat
        self.Position = position
        self.numberSamples = 9

        self.neaClip = 0.1
        self.farClip = 100.0
        self.rayDirections = None
        self.projection = np.array({1})
        self.inverseProjection = np.array({1})
        self.view = np.array({1})
        self.inverseView = np.array({1})

        self.__calculatePerspectiveProjectionMatrix()
        self.__calculateView()


    def __lookAt(self, eye: np.ndarray, center: np.ndarray, up: np.ndarray) -> np.ndarray:
        zaxis = Utils.normalize(eye - center)
        xaxis = Utils.normalize(np.cross(up, zaxis, axis=0))
        yaxis = np.cross(zaxis, xaxis, axis=0)

        translx= -np.dot(xaxis.T, eye)[0][0]
        transly = -np.dot(xaxis.T, eye)[0][0]
        translz = -np.dot(xaxis.T, eye)[0][0]

        return np.array([
            [xaxis[0][0], xaxis[1][0], xaxis[2][0], translx],
            [yaxis[0][0], yaxis[1][0], yaxis[2][0], transly],
            [zaxis[0][0], zaxis[1][0], zaxis[2][0], translz],
            [0, 0, 0, 1]])


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


    def __calculateView(self):
        self.view = self.__lookAt(self.Position, self.lookat, np.array([[0], [1], [0]]))
        self.inverseView = np.linalg.inv(self.view)

    def CalculateRayDirections(self):
        self.rayDirections = np.ndarray((int(self.viewPortWidth * self.viewPortHeight), self.numberSamples, 3, 1))
        for y in range(0, int(self.viewPortHeight)):
            for x in range(0, int(self.viewPortWidth)):
                sampledRays = np.empty((self.numberSamples, 3, 1))
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        offsetX = float(i) / 3.0
                        offsetY = float(j) / 3.0
                        coord = np.array([(float(x) + offsetX) / float(self.viewPortWidth), (float(y) + offsetY) / float(self.viewPortHeight)])
                        coord = coord * 2.0 - 1.0  # map to -1 - 1

                        target = np.matmul(self.inverseProjection, np.array([[coord[0], coord[1], 1, 1]]).T)
                        normalized = Utils.normalize(target[:3] / target[3])
                        rayDirection = np.matmul(self.inverseView,
                                                 np.array([[normalized[0][0], normalized[1][0], normalized[2][0], 0]]).T)

                        sampledRays[(i+1)*3+j+1] = np.array([rayDirection[0], rayDirection[1], rayDirection[2]])

                self.rayDirections[(x + y * int(self.viewPortWidth))] = sampledRays

