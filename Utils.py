import numpy as np
from numpy.random import default_rng

def normalize(v: np.ndarray):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def toColor(vec3 : np.ndarray((1,3,1))) -> np.ndarray((3,)):
    return np.array([
        np.sqrt(vec3[0][0]),
        np.sqrt(vec3[1][0]),
        np.sqrt(vec3[2][0])])  # gamma correction


def randomInUnitSphere():
    rng = default_rng()
    while True:
        p = rng.uniform(-1.0, 1.0, (3,1))
        if np.linalg.norm(p) >= 1: continue
        return p


def randomUnitVector():
    return normalize(randomInUnitSphere())

def reflect(rayDirection, normal):
    return rayDirection - 2 * (np.dot(rayDirection.T, normal) * normal)

def near_zero(vec3: np.ndarray((3,1))) -> bool:
    min = 1e-8
    return (abs(vec3[0][0]) < min) and (abs(vec3[1][0]) < min) and (abs(vec3[2][0]) < min)
