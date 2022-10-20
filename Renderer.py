import Utils
from Camera import Camera
import numpy as np

from HitPayload import HitPayload
from Ray import Ray
from Scene import Scene
import multiprocessing as mp
from contextlib import closing


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


    def Render(self, cam: Camera, scene: Scene):
        self.cam = cam
        self.scene = scene
        self.image = np.zeros((self.height, self.width, 3))

        for y in range(0, self.height):
            for x in range(0, self.width):
                color = self.PerPixel(x, y)
                color = np.clip(color, 0.0, 1.0)
                self.image[y, x] = color
            print("progress: %d/%d" % (y + 1, self.height))

    def RenderParallel(self, cam: Camera, scene: Scene):

        self.cam = cam
        self.scene = scene
        self.image = np.zeros((self.height, self.width, 3))

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
        background = np.array([[0.70], [0.80], [1.00]])

        sampledColor = np.array([[0], [0], [0]])
        rayOrigin = self.cam.Position

        for sample in range(0, self.cam.numberSamples):

            rayDirection = self.cam.rayDirections[x * self.cam.numberSamples + y * self.width * self.cam.numberSamples + sample]

            ray = Ray(rayOrigin, rayDirection)

            sampledColor = sampledColor + self.rayColor(ray, background, 40)

        return Utils.toColor(sampledColor / self.cam.numberSamples)

    def rayColor(self, ray: Ray, background: np.ndarray((3,1)), depth: int) -> np.ndarray((3, 1)):

        if depth <= 0:
            return np.array([[0],[0],[0]])

        hitRecord = self.TraceRay(ray)

        if hitRecord.HitDistance <= 0.0:
            return background

        object = self.scene.Objects[hitRecord.ObjectIndex]
        emitted = object.Material.emitted(hitRecord.WorldPosition)

        scattered, attenuation, success = object.Material.scatter(
            object.Albedo,
            ray,
            hitRecord
        )
        if not success:
            return emitted
        else:
            return emitted + attenuation * self.rayColor(scattered, background, depth - 1)


    def TraceRay(self, ray: Ray):
        hitDistance = float("inf")
        payload: HitPayload = HitPayload(-1.0)

        for i in range(0, len(self.scene.Objects)):
            object = self.scene.Objects[i]

            payload, success = object.hit(ray, payload, 0.001, hitDistance)

            if success:
                hitDistance = payload.HitDistance
                payload.ObjectIndex = i

        return payload
