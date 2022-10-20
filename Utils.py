import numpy as np
from numpy.random import default_rng

def normalize(v: np.ndarray):
    mag = np.sqrt(np.dot(v.T, v))
    return v / mag

def toColor(vec3 : np.ndarray((1,3,1))) -> np.ndarray((3,)):
    return np.array([
        np.sqrt(vec3[0][0]),
        np.sqrt(vec3[1][0]),
        np.sqrt(vec3[2][0])])  # gamma correction


def randomInUnitSphere():
    rng = default_rng()
    while True:
        p = rng.uniform(-1.0, 1.0, (3,1))
        if np.sqrt(np.dot(p.T, p)) >= 1: continue
        return p




def randomUnitVector():
    return normalize(randomInUnitSphere())

def reflect(rayDirection, normal):
    return rayDirection - 2 * (np.dot(rayDirection.T, normal) * normal)

def refract(uv: np.ndarray((3,1)), n: np.ndarray((3,1)), etaiOverEtat) -> np.ndarray((3,1)):
    cosTheta = np.fmin(np.dot(-uv.T, n), 1.0)
    rOutPerp = etaiOverEtat * (uv + cosTheta * n)
    rOutParallel = -np.sqrt(np.fabs(1.0 - np.dot(rOutPerp.T, rOutPerp))) * n
    return rOutPerp + rOutParallel

def near_zero(vec3: np.ndarray((3,1))) -> bool:
    min = 1e-8
    return (abs(vec3[0][0]) < min) and (abs(vec3[1][0]) < min) and (abs(vec3[2][0]) < min)
