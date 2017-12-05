from __future__ import division
import numpy as np
import tools as t
import hamiltonian


H = hamiltonian.HubbardHamiltonian(3,1, 2, 1)

out = H.generate_matrix()

print out.toarray()

print np.linalg.eigh(out.toarray())

#print np.linalg.eig(out)