from __future__ import division
import numpy as np
import math
from math import cos, sin


def normalize(v, tolerance=0.00001):
    mag2 = sum(n * n for n in v)
    if abs(mag2 - 1.0) > tolerance:
        mag = sqrt(mag2)
        v = tuple(n / mag for n in v)
    return v


def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z


def q_conjugate(q):
    w, x, y, z = q
    return (w, -x, -y, -z)


def qv_mult(q1, v1):
    q2 = (0.0,) + v1
    return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]


def axisangle_to_q(v, theta):
    v = normalize(v)
    x, y, z = v
    theta /= 2
    w = cos(theta)
    x = x * sin(theta)
    y = y * sin(theta)
    z = z * sin(theta)
    return w, x, y, z


def q_to_axisangle(q):
    w, v = q[0], q[1:]
    theta = acos(w) * 2.0
    return normalize(v), theta


def leanForward(q):
    """
    find the angle between the chip's surface and earth surface
    i.e. the natural position of sitting straight should have an angle of 90
    lean forward will have an angle > 90
    lean backward will have an angle < 90
    """
    zaxis = (0, 0, 1)
    zaxisRotated = qv_mult(q, zaxis)

    try:
        return math.acos(np.dot(np.array(zaxis), np.array(zaxisRotated)))*180/math.pi
    except Exception:
        return np.nan

        