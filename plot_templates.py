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
  file = f['templates'].value
  return file 

if __name__ == "__main__":
  path = '/Users/wyf/Desktop/anti_stat/200_template.h5'
  data = H5ToMatrix(path)
  for i in range(len(data)):
    image_mat = data[i]
    im = MatrixToImage(image_mat)
    im.resize((640,640)).convert('L').save('/Users/wyf/Documents/templates/'+str(i+1)+".jpg")