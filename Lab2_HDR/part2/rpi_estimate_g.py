from argparse import ArgumentParser
from skimage.io import imread
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from os.path import join, basename

from estimate_linearization_func import estimate_g
import utils as ut

from ipdb import set_trace

if __name__ == '__main__':

  parser = ArgumentParser(description='Create RGB image from individual image')
  parser.add_argument('--folder', '-f', type=str, 
          default = "output_folder",
          help='folder containing all the images')
  parser.add_argument('--ext', '-e', type=str, 
          default = "jpg", help='file ext')

  args = parser.parse_args()

  print(f"DIR:{args.folder}")
  print(f"BASE:{args.base}")
  print(f"EXT:{args.ext}")

  all_fns = glob(join(args.folder, f"*.{args.ext}"))

  exp_times = []
  img_fns = []
  for fn in all_fns:
    curr_name = basename(fn)
    exposure_val = int(curr_name.split(".")[0].split("_")[-1])
    print(f"{exposure_val} : {curr_name}")
    # convert exposure times to seconds
    exp_times.append(float(exposure_val)/1e6)
    img_fns.append(fn)

  
  if (len(img_fns) == 0): 
    print("No files were found")
    exit(0)

  num_exposures = len(exp_times)
  # subsample
  D1 = 50
  H,W,_ = imread(img_fns[0])[::D1,::D1,:].shape
  img_list = np.zeros((num_exposures, H*W*3), dtype="uint64")

  maxVal = 255

  for i, (fn, exp) in enumerate(zip(img_fns, exp_times)):
    ldr_img = imread(fn)
    img_list[i,:] = ldr_img[::D1,::D1,:].flatten()

  weight_name = "gaussian"
  reg = 10
  if weight_name == "uniform":
    g = estimate_g(img_list, weight_fn=ut.uniform_weighting, reg_sq=reg*reg, exp_list=exp_times, maxVal=maxVal)
  elif weight_name == "tent":
    g = estimate_g(img_list, weight_fn=ut.tent_weighting, reg_sq=reg*reg, exp_list=exp_times, maxVal=maxVal)
  elif weight_name == "gaussian":
    g = estimate_g(img_list, weight_fn=ut.gaussian_weighting, reg_sq=reg*reg, exp_list=exp_times, maxVal=maxVal)
  else:
    print(f"Unsupported weight name : {weight_name}")
    exit(1)


  # print(g[:5], g[-5:])
  plt.grid(axis='both', color='0.95')
  plt.plot(g)
  plt.title("%s%d"%(weight_name,reg))
  plt.savefig('%s%d.png'%(weight_name, reg))
  plt.show()
  np.save("g_%s_reg%d_%s.npy"%(weight_name, reg, args.base), g)
