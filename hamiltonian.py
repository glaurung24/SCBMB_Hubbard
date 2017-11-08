# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 22:39:28 2017

@author: andi
"""
from __future__ import division
import tools as t
import numpy as np
from copy import deepcopy


# class that defines and generates the Hamiltonian of the system

class HubbardHamiltonian:
    def __init__(self, size_x=3, size_y=3):
        if(size_x <= 1):
            print 'The dimension x must be larger than 1'
            exit()
        if(size_y < 1):
            print 'The dimension y must be larger or eval to 1'
            exit()
        self.size_x = size_x
        self.size_y = size_y

        self.system_size = size_x * size_y

        self.nr_spins_up = 2
        self.nr_spins_down = 2
        self.U = 1
        self.t = 1




    def generate_matrix(self):
        configs_up = t.configurations(self.nr_spins_up, self.system_size)
        configs_down = t.configurations(self.nr_spins_down, self.system_size)

        nr_configs_up = len(configs_up)
        nr_configs_down = len(configs_down)
        nr_configs_total = nr_configs_up * nr_configs_down

        configs_both = []
        H_1 = np.zeros(nr_configs_total)
        for i in xrange(nr_configs_up):
            for j in xrange(nr_configs_down):
                configs_both.append([configs_up[i], configs_down[j]])
                H_1[i+j] = bin(configs_up[i] & configs_down[j]).count("1")
        list_nearest_neighbors = t.nearest_neighbours(self.size_x, self.size_y)


        H = np.diag(H_1*self.U) #TODO maybe switch to sparse matrix at some point?


        len_bin_nr = len(bin(configs_up[-1]))-2
        for i in xrange(nr_configs_up): #TODO this part is a bit quick'n'dirty, so
                                        # maybe optimize it at some point, e.g. don't
                                        # use strings for doing stuff....
            config = configs_up[i]
            config_str = bytearray(bin(config))[2:].zfill(len_bin_nr)
            occupied_indexes = [x for x, v in enumerate(str(config_str)) if v == "1"]
#            occupied_indexes -= 2 #because of the string format
            for index in occupied_indexes:
                neighbors = list_nearest_neighbors[index]
                for j in xrange(len(neighbors)): #TODO maybe optimize
                    if neighbors[j] not in occupied_indexes:
                        config_str_temp = deepcopy(config_str)
                        config_str_temp[index] = "0"
                        config_str_temp[neighbors[j]] = "1"

                        k = configs_up.index(int(str(config_str_temp), 2))
                        s = 1 #TODO, find right sign...

                        for l in xrange(nr_configs_up): #does not generate hermitian hamiltonian...
                            #write into the Hamiltonian, but I am not sure yet if
                            # right subspaces get filled with this function...
                            #TODO
                            H[k + l*nr_configs_down, i + l*nr_configs_down] = \
                                                                    - self.t*s


                        #do the jump, ask which config index k -> H_ki = -t * s
                        # determine s...(sign)
        return H


