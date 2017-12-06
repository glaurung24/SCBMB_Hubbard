from __future__ import division
import numpy as np
import tools as t
import hamiltonian

x = 2
y = 2
n = x*y
k = 3
T = 1

configs = t.configurations(k, n)
nr_configs = len(configs)
print configs

LNN = t.nearest_neighbours(x, y)
print LNN

H_0 = np.zeros([nr_configs, nr_configs])

for i in xrange(nr_configs):     # i ... i-th configuration
    bits_0 = configs[i]
    for site in xrange(n):       # site  ... current site
        for neigh in xrange(2):  # neigh ... Index for upper or left NN
            nn = LNN[site][neigh]

            if bits_0 >> site & 1 != bits_0 >> nn & 1:
                bits = bits_0 ^ (1 << site) ^ (1 << nn)
                setbits = bin(bits_0 & ((1 << nn)-1)).count("1")  # counts set bits up to bit nn
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

                H_0[i, j] = -s*T

print H_0