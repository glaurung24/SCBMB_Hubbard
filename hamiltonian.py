# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 22:39:28 2017

@author: andi
"""
from __future__ import division
import tools as t
import numpy as np


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
                
        
        H = np.diag(H_1) #TODO maybe switch to sparse matrix at some point?
        return H
            
        
