from __future__ import division
import numpy as np
import tools as t
import hamiltonian


H = hamiltonian.HubbardHamiltonian(4,4)

out = H.generate_matrix()

print out

#print np.linalg.eig(out)