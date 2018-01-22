
from __future__ import division
import numpy as np
import timeit
import greensfct
import tools as t
import hamiltonian
import matplotlib.pyplot as plt
from scipy.sparse.linalg import eigsh


config = dict(x_size = 2, y_size = 1, el_up = 1, el_down = 1)

H = hamiltonian.HubbardHamiltonian(config['x_size'], config['y_size'], config['el_up'], config['el_down'])
out = H.generate_matrix()

print "done"


def eig_normal(M):
    eigvals, eigvecs = np.linalg.eigh(M.toarray())

    return eigvals, eigvecs


def eig_sparse(M):
    n_eigenvals = 2
    eigvals, eigvecs = eigsh(M, n_eigenvals, which='SA')

    return eigvals, eigvecs


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


#wrapper_n = wrapper(eig_normal, out)
#wrapper_s = wrapper(eig_sparse, out)

#print "normal: ", timeit.timeit(wrapper_n, number=1)
#print "sparse: ", timeit.timeit(wrapper_s, number=1)

eigvals, eigvecs = eig_sparse(out)
#print out.toarray()
#n_eigenvals = 1295
#eigvals2, eigvecs2 = eigsh(out, n_eigenvals) #Lanzcos (or Arnoldi?)
print eigvals
print eigvecs[:, 0]
print np.linalg.norm(eigvecs[:, 0])
#print eigvals2

plt.hist(eigvals, 11)  # arguments are passed to np.histogram
#plt.title("DOS")
#plt.show()

indexes = {'x_pos': 1, 'y_pos': 0, 'spin': 'up'}


greensfct.creatorOnWavefct(indexes, eigvecs[:,0], config)


#print np.linalg.eig(out)
