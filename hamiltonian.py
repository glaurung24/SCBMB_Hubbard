# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 22:39:28 2017

@author: andi
"""
from __future__ import division
import tools as t
import numpy as np
from copy import deepcopy
from scipy.sparse import coo_matrix


# class that defines and generates the Hamiltonian of the system

class HubbardHamiltonian:
    def __init__(self, size_x=3, size_y=3, nr_up = 2, nr_down = 2):
        if(size_x <= 1):
            print 'The dimension x must be larger than 1'
            exit()
        if(size_y < 1):
            print 'The dimension y must be larger or eval to 1'
            exit()
        self.size_x = size_x
        self.size_y = size_y

        self.system_size = size_x * size_y

        self.nr_spins_up = nr_up
        self.nr_spins_down = nr_down
        self.U = 10
        self.t = 0.5




    def generate_matrix(self):
        configs_up = t.configurations(self.nr_spins_up, self.system_size)
        configs_down = t.configurations(self.nr_spins_down, self.system_size)

        nr_configs_up = len(configs_up)
        nr_configs_down = len(configs_down)
        nr_configs_total = nr_configs_up * nr_configs_down



        ##################### Calculation of H_1 ####################################

        configs_both = []
        row = []
        col = []
        data = []
        #H_1 = np.zeros(nr_configs_total)
        counter = 0
        for i in xrange(nr_configs_up):
            for j in xrange(nr_configs_down):
                configs_both.append([configs_up[i], configs_down[j]])
                data = np.concatenate((data, [self.U*bin(configs_up[i] & configs_down[j]).count("1")]))
                row = np.concatenate((row, [counter]))
                col = np.concatenate((col, [counter]))
                counter += 1


#        H =
#        H = np.diag(H_1*self.U) #TODO maybe switch to sparse matrix at some point?

        ################ Filling H with H_0 #########################################

        subH_0_up = self.generateSubH_0(configs_up)
        subH_0_down = self.generateSubH_0(configs_down)

        H_0 = self.merge_h_0(subH_0_up, subH_0_down)

        data = np.concatenate((data, H_0.data))
        row = np.concatenate((row, H_0.row))
        col = np.concatenate((col, H_0.col))

        H = coo_matrix((data, (row, col)), shape=(nr_configs_total, nr_configs_total))
        return coo_matrix.tocsr(H)

        ##################### Calculation of H_0 ####################################
    def generateSubH_0(self, configs):

        nr_configs = len(configs)
        LNN = t.nearest_neighbours(self.size_x, self.size_y)

        n = self.system_size
        row = []
        col = []
        data = []

        for i in xrange(nr_configs):  # i ... i-th configuration
            bits_0 = configs[i]
            for site in xrange(n):  # site  ... current site
                for neigh in xrange(2):  # neigh ... Index for upper or left NN
                    nn = LNN[site][neigh]

                    bit_s = bits_0 >> site & 1
                    bit_n = bits_0 >> nn & 1
                    if bit_s != bit_n:

                        bits = bits_0 ^ (1 << site) ^ (1 << nn)
                        if bit_s:
                            setbits = bin(bits_0 & ((1 << site) - 1)).count("1")
                            setbits += bin((bits_0 ^ (1 << site)) & ((1 << nn) - 1)).count("1")
                        else:
                            setbits = bin(bits_0 & ((1 << nn) - 1)).count("1")
                            setbits += bin((bits_0 ^ (1 << nn)) & ((1 << site) - 1)).count("1")

                        s = (-1) ** setbits

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
                        data.append(-s * self.t)

        H_0 = coo_matrix((data, (row, col)), shape=(nr_configs, nr_configs))

        return H_0#.toarray()


    def merge_h_0(self, h_u, h_d):


            dim_up = np.shape(h_u)[0]
            dim_down = np.shape(h_d)[0]
            dim = dim_up * dim_down

            row = []
            col = []
            data = []

            for k in xrange(dim_up):
                row = np.concatenate((row, h_d.row + k * dim_down))
                col = np.concatenate((col,  h_d.col + k * dim_down))
                data = np.concatenate((data, h_d.data))

            for k in xrange(dim_down):
                row = np.concatenate((row, h_u.row * dim_down + k))
                col = np.concatenate((col, h_u.col * dim_down + k))
                data = np.concatenate((data, h_u.data))

            h_0 = coo_matrix((data, (row, col)), shape=(dim, dim))
            return h_0#.toarray()


                    #do the jump, ask which config index k -> H_ki = -t * s
                    # determine s...(sign)



