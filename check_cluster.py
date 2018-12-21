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
  file = f['cluster_data'].value
  return file 

if __name__ == "__main__":
  path = '/Users/wyf/Desktop/anti_stat/crop_test.h5'

  cluster = '/Users/wyf/Desktop/anti_stat/200_sed_res.dat'
  data = H5ToMatrix(path)
  f = open(cluster) 
  count = 0
  cluster_num = 0
  for line in f.readlines():
    cluster_num += 1
    count += 1
    cl_list = line.split('[')[1].split(']')[0].split()
    if cluster_num < 201:
      for i in cl_list:
        i= int(i.split(',')[0])
        image_mat = data[i]
        im = MatrixToImage(image_mat)
        im.resize((640,640)).convert('L').save('/Users/wyf/Documents/crop_image8/'+str(count)+'_'+str(i)+".jpg")