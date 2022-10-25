import multiprocessing as mp
from contextlib import closing

import numpy as np

import Utils
from Camera import Camera
from HitPayload import HitPayload
from Ray import Ray
from Scene import Scene


def _init(shared_arr_):
    # The shared array pointer is a global variable so that it can be accessed by the
    # child processes. It is a tuple (pointer, dtype, shape).
    global shared_arr
    shared_arr = shared_arr_


def shared_to_numpy(shared_arr, dtype, shape):
    """Get a NumPy array from a shared memory buffer, with a given dtype and shape.
    No copy is involved, the array reflects the underlying shared buffer."""
    return np.frombuffer(shared_arr, dtype=dtype).reshape(shape)


def create_shared_array(dtype, shape):
    """Create a new shared array. Return the shared array pointer, and a NumPy array view to it.
    Note that the buffer values are not initialized.
    """
    dtype = np.dtype(dtype)
    # Get a ctype type from the NumPy dtype.
    cdtype = np.ctypeslib.as_ctypes_type(dtype)
    # Create the RawArray instance.
    temp = np.prod(shape)
    shared_arr = mp.RawArray(cdtype, int(temp))
    # Get a NumPy array view.
    arr = shared_to_numpy(shared_arr, dtype, shape)
    return shared_arr, arr


class Renderer:
    def __init__(self, width, height):
        self.cam = None
        self.scene = None
        self.width = width
        self.height = height
        self.image = None
        self.background = np.zeros((3, 1))
        self.numberSamples = 10

    def Render(self, cam: Camera, scene: Scene, background: np.ndarray((3, 1)) = np.zeros((3, 1))):
        self.cam = cam
        self.scene = scene
        self.image = np.zeros((self.height, self.width, 3))
        self.background = background

        for y in range(0, self.height):
            for x in range(0, self.width):
                color = self.PerPixel(x, y)
                color = np.clip(color, 0.0, 1.0)
                self.image[y, x] = color
            print("progress: %d/%d" % (y + 1, self.height))

    def RenderParallel(self, cam: Camera, scene: Scene, background: np.ndarray((3, 1)) = np.zeros((3, 1))):

        self.cam = cam
        self.scene = scene
        self.image = np.zeros((self.height, self.width, 3))
        self.background = background

        numCores = mp.cpu_count()
        dtype = np.float
        shape = self.image.shape
        shared_arr, image = create_shared_array(dtype, shape)

        with closing(mp.Pool(
                numCores, initializer=_init, initargs=((shared_arr, dtype, shape),))) as p:
            p.map(self.RenderRowParallel, [y for y in range(0, self.height)])

        p.join()
        self.image = image

    def RenderRowParallel(self, y):
        for x in range(0, self.width):
            color = self.PerPixel(x, y)
            color = np.clip(color, 0.0, 1.0)
            image = shared_to_numpy(*shared_arr)
            image[y, x] = color
        print("progress: %d/%d" % (y + 1, self.height))

    def PerPixel(self, x: int, y: int) -> np.ndarray:

        sampledColor = np.array([[0], [0], [0]])
        rayOrigin = self.cam.Position

        for sample in range(0, self.numberSamples):
            rayDirection = self.cam.calculateRayDirection(x,y)
            ray = Ray(rayOrigin, rayDirection)

            sampledColor = sampledColor + self.rayColor(ray, self.background, 40)

        return Utils.toColor(sampledColor / self.numberSamples)

    def rayColor(self, ray: Ray, background: np.ndarray((3, 1)), depth: int) -> np.ndarray((3, 1)):

        if depth <= 0:
            return np.array([[0], [0], [0]])

        payload: HitPayload = HitPayload(-1.0)
        payload = self.TraceRay(ray, payload)

        if payload.HitDistance <= 0.0:
            return background

        object = self.scene.Objects[payload.ObjectIndex]
        emitted = object.Material.emitted(payload, payload.WorldPosition)

        scattered, albedo, pdf, success = object.Material.scatter(
            ray,
            payload
        )

        if not success:
            return emitted

        onLight = np.array([[Utils.randomDouble(213, 343)[0]], [554], [Utils.randomDouble(-332, -227)[0]]])
        toLight = onLight - payload.WorldPosition
        distanceSquared = np.square(np.linalg.norm(toLight))
        toLight = Utils.normalize(toLight)

        if np.dot(toLight.T, payload.WorldNormal) < 0:
            return emitted

        lightArea = (343-213)*(332-227)
        lightCosine = np.fabs(toLight[1][0])
        if lightCosine < 0.000001:
            return emitted

        pdf = distanceSquared / (lightCosine * lightArea)
        scattered = Ray(payload.WorldPosition, toLight)

        color = self.rayColor(scattered, background, depth - 1) / pdf
        pdf_color = object.Material.scatteringPdf(ray, payload, scattered)
        return emitted + albedo * pdf_color * color

    def TraceRay(self, ray: Ray, payload: HitPayload) -> HitPayload:
        hitDistance = float("inf")

        for i in range(0, len(self.scene.Objects)):
            object = self.scene.Objects[i]

            payload, success = object.hit(ray, payload, 0.001, hitDistance)

            if success:
                hitDistance = payload.HitDistance
                payload.ObjectIndex = i

        return payload
