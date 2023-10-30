import numpy as np
import matplotlib.pyplot as plt

import utils as ut

min_clip = 0.02
max_clip = 0.98

eps = 1e-10
def hdr_merge(img_list, weight_fn = ut.uniform_weighting, method='linear', g=None, exp_times=None):
  
  # TODO : make default to maxVal
  if(g is None):
    print("g is required for linearization")
    exit(0)

  # for dim
  img = img_list[0,:,:,:]

  # init to zero creates problem as the least value is not zero
  out_img = np.zeros(img.shape, dtype=np.float32)
  weights_sum = np.zeros(img.shape, dtype=np.float32)

  overexposed = np.ones(img.shape, dtype=bool)
  underexposed = np.ones(img.shape, dtype=bool)

  for k, (img, exp) in enumerate(zip(img_list, exp_times)):
    print(f"Adding {k} img vals")

    img_lin = np.exp(g[img]).squeeze()

    # use ldr
    # check for underexposure and overexposure
    overexposed = np.logical_and(img_lin>max_clip, overexposed)
    underexposed = np.logical_and(img_lin<min_clip, underexposed)

    if weight_fn == ut.photon_weighting:
      weight = weight_fn(img_lin, tk=exp, zmin=min_clip, zmax=max_clip)
    else:
      weight = weight_fn(img_lin, zmin=min_clip, zmax=max_clip)

    # based on matlab implementation
    weight[underexposed] = 0.
    weight[overexposed] = 0.
    img[underexposed] = 1.
    img[overexposed] = 1.

    weights_sum += weight
    # use linear img
    if method == "linear":
      out_img += weight*img/exp
    elif method == "log":
      out_img += weight*(np.log(img+eps) - log(exp))
    else:
      print("Wrong method string. Please specify linear/log")
      
  weights_sum += eps

  if method == 'log':
    out_img = np.exp(out_img/weights_sum)
  elif method == "linear":
    out_img = out_img/weights_sum

  return out_img