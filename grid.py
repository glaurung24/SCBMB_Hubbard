from __future__ import division
import numpy as np


def grid(size_x, size_y):
    N = size_x*size_y
    if size_y == 1:
        return np.arange(size_x)
    else:
        out = []
        for i in xrange(N):
                out.append(np.array([i//size_x,i%size_y]))
        return out



