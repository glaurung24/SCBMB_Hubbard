from __future__ import division
import numpy as np
import tools as t
from scipy.sparse import bsr_matrix
import hamiltonian

x = 3
y = 2
n = x*y
k = 2
T = 1

configs = t.configurations(k, n)
nr_configs = len(configs)
print configs

LNN = t.nearest_neighbours(x, y)
print LNN

#H_0 = np.zeros((nr_configs, nr_configs))
row = []
col = []
data = []

for i in xrange(nr_configs):     # i ... i-th configuration
    bits_0 = configs[i]
    for site in xrange(n):       # site  ... current site
        for neigh in xrange(2):  # neigh ... Index for upper or left NN
            nn = LNN[site][neigh]

            bit_s = bits_0 >> site & 1
            bit_n = bits_0 >> nn & 1
            if bit_s != bit_n:

                bits = bits_0 ^ (1 << site) ^ (1 << nn)
                if bit_s:
                    setbits = bin(bits_0 & ((1 << site)-1)).count("1")
                    setbits += bin((bits_0 ^ (1 << site)) & ((1 << nn)-1)).count("1")
                else:
                    setbits = bin(bits_0 & ((1 << nn) - 1)).count("1")
                    setbits += bin((bits_0 ^ (1 << nn)) & ((1 << site) - 1)).count("1")

                s = (-1)**setbits

                # bisection search algorithm
                notfound = True
                j = 0
                elements = configs
                nr_elements = nr_configs
                while notfound:
                    cut = nr_elements // 2
                    if bits == elements[cut]:
                        notfound = False
                        j += cut
                    elif bits < elements[cut]:
                        elements = elements[:cut]
                        nr_elements = cut
                    else:  # bits > elements[cut]:
                        elements = elements[cut:]
                        nr_elements -= cut
                        j += cut

                row.append(i)
                col.append(j)
                data.append(-s*T)
                #H_0[i, j] = -s*T

H_0 = bsr_matrix((data, (row, col)), shape=(nr_configs, nr_configs))#.toarray()
print H_0


