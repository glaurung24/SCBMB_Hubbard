# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 22:46:24 2018

@author: andi
"""

from __future__ import division
import tools as t
import numpy as np
from copy import deepcopy
from scipy.sparse import coo_matrix

def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

def creatorOnWavefct(indexes, wavefct, old_config_inp):
    size_x = old_config_inp['x_size']
    size_y = old_config_inp['y_size']
    nr_sites = size_x*size_y

    if(indexes['spin'] == 'up'):
        old_configs = t.configurations(old_config_inp['el_up'], nr_sites)
        new_configs = t.configurations(old_config_inp['el_up'] + 1, nr_sites)
    else:
        old_configs = t.configurations(old_config_inp['el_down'], nr_sites)
        new_configs = t.configurations(old_config_inp['el_down'] + 1, nr_sites)

    pos_in_sup_hilbertspace = size_x * indexes['y_pos'] + indexes['x_pos'] #warning the positions start counting at 0

    dim_sup_space = len(old_configs)
    n = dim_sup_space
    for i in xrange(len(old_configs)):
        old_config = bytearray(bin(old_configs[i]))[2:].zfill(n)
        old_config = str(old_config)
        if old_config[pos_in_sup_hilbertspace] == '1':
            # wavefct = 0
            print 'do something'
            print bin(old_configs[i])
        else:
            new_config = deepcopy(old_config)
#            new_config[pos_in_sup_hilbertspace] = '1'
            new_config = replace_str_index(new_config, pos_in_sup_hilbertspace, '1')

            new_config = int(str('0b' + new_config), 2)
            sign = -1**int('0b' + old_config[:pos_in_sup_hilbertspace], 2)
            print sign



