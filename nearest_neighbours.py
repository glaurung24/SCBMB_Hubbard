from __future__ import division
import numpy as np


# doesn't work for size_x or size_y = 1
# lists n.n. as array [[upper neighbour of N=1, left neighbour of N=1],
#                      [u.n. N=2, l.n. N=2], ...]
def nearest_neighbours(size_x, size_y):
    n = size_x*size_y
    out = []
    for i in xrange(n):
        out.append(np.array([i-size_y + (i < size_y)*n, i - 1 + (i % size_y == 0)*size_y]))
    return out
