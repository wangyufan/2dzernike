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
  path = '/Users/wyf/Documents/100f_result/templates/'
  files = os.listdir(path)
  template_list = [os.path.join(path, f) for f in files if f.endswith('200_correlation_templates.h5')]
  for t_path in template_list:
    data = H5ToMatrix(t_path)
    t_type = os.path.basename(t_path).split('_templates')[0]
    for i in range(len(data)):
      image_mat = data[i]
      # if (i==23):
      print(data[i].astype(int))
      im = MatrixToImage(image_mat)
      output = '/Users/wyf/Documents/100f_result/templates_images/'+str(t_type)+'_'+str(i+1)+".jpg"
      # print(output)
      im.resize((640,640)).convert('L').save(output)