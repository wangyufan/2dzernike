import time, sys
import h5py
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

def MatrixToImage(data):
  new_im = Image.fromarray(data)
  return new_im

def H5ToMatrix(filename):
  f = h5py.File(filename,'r')
  f.keys()                        
  file = f['templates'].value * 0.05
  return file 

if __name__ == "__main__":
  template_mask_path = '/Users/wyf/Documents/100f_result/templates/signal_0.1_0.4_braycurtis_mask.npy'
  template_mask = np.load(template_mask_path)
  for i in range(len(template_mask_path)):
    print(template_mask[i])