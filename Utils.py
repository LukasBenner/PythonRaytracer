import numpy as np

def normalize(v: np.ndarray):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm
def toColor(vec3 : np.ndarray((1,3,1))) -> np.ndarray((3,)):
    return np.array([vec3[0][0],vec3[1][0],vec3[2][0]])


def randomUnitVector():
    return normalize(np.random.rand(3,1))

def reflect(rayDirection, normal):
    return rayDirection - 2 * (np.dot(rayDirection.T, normal) * normal)
