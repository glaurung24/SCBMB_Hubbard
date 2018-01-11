from __future__ import division
import numpy as np
import tools as t
import hamiltonian
import matplotlib.pyplot as plt
from scipy.sparse.linalg import eigsh


H = hamiltonian.HubbardHamiltonian(2,2, 1, 1)

out = H.generate_matrix()

print out.toarray()


eigvals, eigvecs =  np.linalg.eig(out.toarray())
n_eigenvals = 4
eigvals2, eigvecs2 = eigsh(out, n_eigenvals) #Lanzcos (or Arnoldi?)
print eigvals
print eigvals2

#plt.hist(eigvals)  # arguments are passed to np.histogram
#plt.title("DOS")
#plt.show()



#print np.linalg.eig(out)
