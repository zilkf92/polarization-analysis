import numpy as np


def sin(x, a, b, c, d):
    return a * np.sin((b * x) + c, dtype=np.longdouble) + d
