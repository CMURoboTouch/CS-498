from argparse import ArgumentParser
import numpy as np
from skimage.io import imread, imsave
from os.path import join, basename
import matplotlib.pyplot as plt
from glob import glob

from create_hdr_from_raw import hdr_merge
import utils as ut

if __name__ == '__main__':

  parser = ArgumentParser(description='Create RGB image from individual image')
  parser.add_argument('--folder', '-f', type=str, 
          default = "/media/arpit/datadisk1/prosilica_imagesetup/brdf_char_v4",
          help='folder containing all the images')
  parser.add_argument('--ext', '-e', type=str, 
          default = "jpeg", help='file ext')

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


  H,W,_ = imread(img_fns[0]).shape
  img_list = np.zeros((num_exposures, H,W,3), dtype="uint64")

  maxVal = 1023 # RPIv1 gives out 10bit images

  g = np.load("g_gaussian_reg10_whiteledcolorchecker1.npy")

  for i, (fn, exp) in enumerate(zip(img_fns, exp_times)):
    bayer_data = extract_bayer_raw_from_exif(fn)
    demosaiced_data = demosaic_bayer(bayer_data)
    ldr_img = np.clip(demosaiced_data, 0, maxVal)
    ldr_img = np.floor(ldr_img).astype("uint64")

    img_list[i,:] = ldr_img


  hdr = hdr_merge(img_list, ut.gaussian_weighting, 'linear', g, exp_times)

  np.save(join(args.folder, f"{args.base}_merged.npy"), hdr)
  # need to scale down due to storage problem; npy data is correct
  imsave(join(args.folder, f"{args.base}_merged.exr"), hdr/1e1)
  
  hdr_rz = hdr[::8, ::8]
  # need to scale down due to storage problem; npy data is correct
  imsave(join(args.folder, f"{args.base}_rz_merged.exr"), hdr_rz/1e1)
