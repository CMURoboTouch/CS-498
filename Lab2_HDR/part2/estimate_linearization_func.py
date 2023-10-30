import utils as ut
import numpy as np
from numpy.linalg import lstsq
from time import time

def estimate_g(img_list, weight_fn = ut.uniform_weighting, reg_sq = 100, exp_list=None, maxVal=255):

  N = maxVal + 1
  
  # for dimensions
  K = len(img_list) # num of exposures

  # downsample factor 
  L = img_list.shape[1] # total pixels x 3

  # size of v : L+N
  # A = np.zeros((K*L+N +1, L+N))
  A = np.zeros((K*L+N, L+N))
  b = np.zeros((A.shape[0], 1))

  px_idx = np.arange(L)

  start_t = time()
  #equations for the first term = K*L
  M = K*L

  weights_second = weight_fn(np.arange(N)/(N+0.0)) #*N

  main_weight_quan = reg_sq*weights_second

  # second term - can only start from z=1
  A[ np.arange(M , M+N-2), np.arange(1,N-1)] = -2*main_weight_quan[1:-1]
  A[np.arange(M, M+N-2), np.arange(0,N-2)] = 1*main_weight_quan[:-2]
  A[np.arange(M, M+N-2), np.arange(2,N)] = 1*main_weight_quan[2:]

  # calc weights once and then just look up
  # not supported for photon optimal
  all_weights = weight_fn(np.arange(0,maxVal+1)/(N+0.0)) #*N

  for k in range(img_list.shape[0]):
    
    img = img_list[k,:]
    tk = exp_list[k]

    weights = all_weights[img]

    b[k*L:(k+1)*L,0] = np.log(tk)*weights
    A[k*L + px_idx, img] = weights # g terms
    A[k*L + px_idx, N + px_idx] = -weights  # Lij terms

  # add the last line g(N//2) = 0
  A[-1, N//2] = 1
  
  end_eq = time()
  v = lstsq(A,b, rcond=None)[0]
  end_solve = time()
  print(f"equa form time: {end_eq-start_t}, solve time: {end_solve - end_eq}")
  g = v[:N]

  return g