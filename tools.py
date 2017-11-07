#  tools.py
#  
#  Module, contains several tools needed for many body calculations
#


from __future__ import division
import numpy as np


# creates list of configurations for k 'ones' in n 'zeros', returned as integers
def configurations(n, k):

    el = (1 << k) - 1
    out = [el]
    while el < (((1 << k) - 1) << n-k):
        el = next_perm(el)
        out.append(el)

    return out


def next_perm(v):
    """
    Generates next permutation with a given amount of set bits,
    given the previous lexicographical value.
    Taken from http://graphics.stanford.edu/~seander/bithacks.html
    """
    t = (v | (v - 1)) + 1
    w = t | ((((t & -t) // (v & -v)) >> 1) - 1)

    return w
    
    
# doesn't work for size_x or size_y = 1
# lists n.n. as array [[upper neighbour of N=1, left neighbour of N=1],
#                      [u.n. N=2, l.n. N=2], ...]
def nearest_neighbours(size_x, size_y):
    n = size_x*size_y
    out = []
    if size_y == 1:
        out = np.arange(size_x) + 1
        out[-1] = 0
    else: 
        for i in xrange(n):
            out.append([i-size_y + (i < size_y)*n, i - 1 + (i % size_y == 0)*size_y])
    return out

# function grid
# returns a ordered list of x,y-coordinates for a system sized size_x x size_y,
# where the zeroth element in the list is in the left top corner of the grid, 
# then it counts to the right and the last element beeing in the right bottom
# corner of the grid
# 
def grid(size_x, size_y):
    N = size_x*size_y
    if size_y == 1:
        return np.arange(size_x)
    else:
        out = []
        size_y += 1
        for i in xrange(N):
                out.append([i%size_x,i//size_y])
    return out
