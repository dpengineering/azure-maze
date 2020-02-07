import math
import numpy as np


def point(x, y, z):
    return np.array((x, y, z))

def length(v):
    return np.linalg.norm(v)

def normalize(v):
    l = length(v)
    if l < 0.000001:
        return None
    return v / l

def dist(a, b):
    return length(a - b)

def pitch(v, a):
    sin = math.sin
    cos = math.cos
    mat = ((1,      0,       0),
           (0, cos(a), -sin(a)),
           (0, sin(a),  cos(a)))
    return np.matmul(mat, v)

def project_onto_plane(v, n):
    # v is the vector, n is the normal of the plane
    return v - (v.dot(n) * n)

def angle_between_vectors(v1, v2):
    return math.acos(normalize(v1).dot(normalize(v2)))

def normalize_angle(t):
    return t % (2 * math.pi)

def angle_distance(t1, t2):
    res = abs(normalize_angle(t1) - normalize_angle(t2))
    if res > math.pi:
        res = (math.pi * 2) - res
    return res
