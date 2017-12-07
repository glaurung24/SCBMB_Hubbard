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
        self.U = 1
        self.t = 1




    def generate_matrix(self):
        configs_up = t.configurations(self.nr_spins_up, self.system_size)
        configs_down = t.configurations(self.nr_spins_down, self.system_size)

        nr_configs_up = len(configs_up)
        nr_configs_down = len(configs_down)
        nr_configs_total = nr_configs_up * nr_configs_down



        ##################### Calculation of H_1 ####################################

        configs_both = []
        H_1 = np.zeros(nr_configs_total)
        counter = 0
        for i in xrange(nr_configs_up):
            for j in xrange(nr_configs_down):
                configs_both.append([configs_up[i], configs_down[j]])
                H_1[counter] = bin(configs_up[i] & configs_down[j]).count("1")
                counter += 1


#        H =
        H = np.diag(H_1*self.U) #TODO maybe switch to sparse matrix at some point?

        ################ Filling H with H_0 #########################################

        subH_0_up = self.generateSubH_0(configs_up)
        subH_0_down = self.generateSubH_0(configs_down)

        H_0 = self.merge_h_0(subH_0_up, subH_0_down)

        H += H_0
        return H

        ##################### Calculation of H_0 ####################################
    def generateSubH_0(self, configs):
        nr_configs = len(configs)
#        print configs
        
        LNN = t.nearest_neighbours(self.size_x, self.size_y)
#        print LNN
        
        H_0 = np.zeros([nr_configs, nr_configs])
        
        for i in xrange(nr_configs):     # i ... i-th configuration
            bits_0 = configs[i]
            for site in xrange(self.system_size):       # site  ... current site
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
        
                        H_0[i, j] = -s*self.t
        return H_0
        
        
        
        
#        len_bin_nr = len(bin(configs[-1]))-2
#        nr_configs = len(configs)
#        H_0 = np.zeros([nr_configs, nr_configs])
#        list_nearest_neighbors = t.nearest_neighbours(self.size_x, self.size_y)
#        for ket_index in xrange(nr_configs): #TODO this part is a bit quick'n'dirty, so
#                                        # maybe optimize it at some point, e.g. don't
#                                        # use strings for doing stuff....
#            config = configs[ket_index]
#            config_str = bytearray(bin(config))[2:].zfill(len_bin_nr)
#            occupied_indexes = [x for x, v in enumerate(str(config_str)) if v == "1"]
##            occupied_indexes -= 2 #because of the string format
#            for index in occupied_indexes:
#                neighbors = list_nearest_neighbors[index]
#                for j in xrange(len(neighbors)): #TODO maybe optimize
#                    if neighbors[j] not in occupied_indexes:
#                        config_str_temp = deepcopy(config_str)
#                        config_str_temp[index] = "0"
#                        n_annihilator = config_str_temp[:index].count("1")
#                        config_str_temp[neighbors[j]] = "1"
#                        n_creator = config_str_temp[:neighbors[j]].count("1")
#                        bra_index = configs.index(int(str(config_str_temp), 2)) #... find index k of bra
#                                                                                #TODO this might not be the fastest solution (use bisection search algorithm)
#                        sign = (-1)**(n_annihilator+n_creator) #sign of matrix element
#
#                        H_0[bra_index, ket_index] = (-1)* self.t*sign
##                            for l in xrange(nr_configs_up): #does not generate hermitian hamiltonian...
##                                #write into the Hamiltonian, but I am not sure yet if
##                                # right subspaces get filled with this function...
##                                #TODO
##                                H[bra_index + l*nr_configs_down, ket_index + l*nr_configs_down] = \
##                                                                        - self.t*sign
#        return H_0
        


    def merge_h_0(self, h_u, h_d):

            dim_up = np.shape(h_u)[0]
            dim_down = np.shape(h_d)[0]
            dim = dim_up * dim_down
            h_0 = np.zeros([dim, dim])

            for i in xrange(dim):
                for j in xrange(dim):
                    i_up = i // dim_down #TODO check if up and down should be flipped
                    j_up = j // dim_down
                    i_down = i % dim_down
                    j_down = j % dim_down
                    if i_up == j_up:
                        h_0[i, j] += h_d[i_down, j_down]
                    if i_down == j_down:
                        h_0[i, j] += h_u[i_up, j_up]

            return h_0


                    #do the jump, ask which config index k -> H_ki = -t * s
                    # determine s...(sign)



