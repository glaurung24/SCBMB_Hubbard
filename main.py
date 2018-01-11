
from __future__ import division
import numpy as np
import timeit
import tools as t
import hamiltonian
import matplotlib.pyplot as plt
from scipy.sparse.linalg import eigsh


H = hamiltonian.HubbardHamiltonian(3, 3, 2, 1)

out = H.generate_matrix()

print "done"


def eig_normal(M):
    eigvals, eigvecs = np.linalg.eigh(M.toarray())

    return eigvals, eigvecs


def eig_sparse(M):
    n_eigenvals = 323
    eigvals, eigvecs = eigsh(M, n_eigenvals)

    return eigvals, eigvecs


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


wrapper_n = wrapper(eig_normal, out)
wrapper_s = wrapper(eig_sparse, out)

print "normal: ", timeit.timeit(wrapper_n, number=1)
print "sparse: ", timeit.timeit(wrapper_s, number=1)

#eigvals, eigvecs = np.linalg.eigh(out.toarray())
#n_eigenvals = 1295
#eigvals2, eigvecs2 = eigsh(out, n_eigenvals) #Lanzcos (or Arnoldi?)
#print eigvals
#print eigvals2

#plt.hist(eigvals, 100)  # arguments are passed to np.histogram
plt.title("DOS")
plt.show()



#print np.linalg.eig(out)