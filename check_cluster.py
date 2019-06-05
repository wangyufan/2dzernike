import time, sys
import h5py
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

def MatrixToImage(data):
  new_im = Image.fromarray(data)
  return new_im

def H5ToMatrix(filename, key):
  f = h5py.File(filename,'r')
  file = f[key].value
  return file 

def Draw_v2(path, cluster):
  data = H5ToMatrix(path, 'peak_mat')
  cluster_res = H5ToMatrix(cluster, 'data')
  cluster_size = len(cluster_res)
  cluster_type = os.path.basename(cluster).split('_')[0]
  output = '/Users/wyf/Documents/100f_result/cluster_image/crop_image_'+str(cluster_size)+'_'+str(cluster_type)+'/'
  os.mkdir(output)

  for index in range(cluster_size):
    cluster_id = cluster_res[index]
    image_mat = data[index]
    im = MatrixToImage(image_mat*0.1)
    filename = str(cluster_id)+'_'+str(index)+".jpg"
    im.resize((640,640)).convert('L').save(output+filename)

# def Draw(path, cluster):
#   data = H5ToMatrix(path, 'cluster_data')
#   cluster = open(cluster) 
#   count = 0
#   cluster_num = 0
#   for line in f.readlines():
#     cluster_num += 1
#     count += 1
#     cl_list = line.split('[')[1].split(']')[0].split()
#     if cluster_num < 201:
#       for i in cl_list:
#         i= int(i.split(',')[0])
#         image_mat = data[i]
#         im = MatrixToImage(image_mat)
#         im.resize((640,640)).convert('L').save('/Users/wyf/Documents/crop_image8/'+str(count)+'_'+str(i)+".jpg")

if __name__ == "__main__":
  path = '/Users/wyf/Documents/real_data/cluster_data_r15.h5'
  cluster_dir = '/Users/wyf/Documents/100f_result/cluster_res/'
  files = os.listdir(cluster_dir)
  cluster_list = [os.path.join(cluster_dir, f) for f in files if f.endswith('cluster_res.h5')]
  # cluster = '/Users/wyf/Desktop/anti_stat/200_sed_res.dat'
  for cluster in cluster_list:
    Draw_v2(path, cluster)
