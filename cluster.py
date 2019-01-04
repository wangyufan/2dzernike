from __future__ import division
from scitbx import math
from scitbx import differential_evolution as de
from scitbx import simplex
from scitbx import lbfgs
from scitbx import direct_search_simulated_annealing as dssa
from scitbx.array_family import flex
from stdlib import math as smath
import time, sys
import h5py
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans
import Clustering 
import pylab


def ImageToDat(file):
  im = Image.open(filename)
  width,height = im.size
  im = im.convert("L") 
  im.show()
  data = im.getdata()
  new_data = np.reshape(data,(width,height))
  image = flex.vec3_double()
  for x in range(0, width):
  for y in range(0, height):
    value = new_data[x][y]
    image.append([x,y,value])
  return image


def preprocess_image(h5file):
  f = h5py.File(h5file,'r')
  f.keys()                        
  file = f['trans_data'][:]                     
  f.close()
  p_list=[]
  for i in range(0, 11):
    for j in range(0, 11):
      value = file[i][j]
      p_list.append(value)
  
  v_min=0
  p_max=max(p_list)
  p_min=min(p_list)
  print p_max,smath.log((float(p_max)))
  if p_min>float(0):
    add_value = 0
  else:
  add_value = smath.minus(0, p_min)+1
  image = flex.vec3_double()
  original = open(h5file.split(".")[0]+'_original.dat','w')
  for x in range(0, 11):
    for y in range(0, 11):
      value = file[x][y]
      image.append([x,y,value])
      print>>original, x,y, value
  original.close()
  return image

def tst_2d_zernike_mom(n, l, file):
  # image = preprocess_image(h5file)
  image = ImageToDat(file)
  feature_maxtix = []
  NP=int(smath.sqrt( image.size() ))  
  N=int(NP/2)
  # print"=====",NP, N
  grid_2d = math.two_d_grid(N, nmax)
  grid_2d.clean_space( image )
  grid_2d.construct_space_sum()
  zernike_2d_mom = math.two_d_zernike_moments( grid_2d, nmax )
  moments = zernike_2d_mom.moments()
  coefs = flex.real( moments )
  nl_array = math.nl_array( nmax )
  nls = nl_array.nl()
  # nl_array.load_coefs( nls, coefs )
  # lfg = math.log_factorial_generator(nmax)
  for nl, c in zip( nls, moments):
    if(abs(c)<1e-3):
      c=0
    feature_maxtix.append(c.real)
    # print nl,c
  return feature_maxtix

def DatToMatrix(filename):
  f = open(filename)
  # res = np.zeros((500,500), dtype=np.float)
  res = np.zeros((11, 11), dtype=np.float)
  for line in f.readlines():
  	data = line.split(" ")
  	x=int(data[0])
  	y=int(data[1])
  	value=float(data[2])
  	res[x][y] = value
  f.close()
  return res
    
def MatrixToImage(data):
  data =data*float(.1) #to see the shape clearly...
  new_im = Image.fromarray(data)
  return new_im

def H5ToMatrix(filename):
  f = h5py.File(filename,'r')
  f.keys()                        
  file = f['trans_data'][:]
  return file 

def plot_h5(filename):
  data = H5ToMatrix(filename)
  im = MatrixToImage(data)
  im.show()

if __name__ == "__main__":
  args = sys.argv[1:]
  cluster_num = args[0]
  t_s = time.time()
  n = 2
  l = 2
  nmax = max(5, n)
  # create a list of images
  path = '/Users/wyf/Documents/SFX/NoGap'
  # path = '/Users/wyf/Documents/crop_image'
  # make sure the list is in order,1,2,3,...11,...99,100...1000,1001... since matching node's id depends on the files' order
  files = os.listdir(path)
  files.remove('.DS_Store')
  files.sort(key = lambda x: int(x.split(".")[0].split("transfered")[1]))
  h5_list = [os.path.join(path, f) for f in files if f.endswith('7.h5')]
  # imlist=[]  
  # for p in range(len(h5_list)):
  #   # pylab.subplot(4, 5, p + 1)
  #   h5name = h5_list[p]
  #   mat = H5ToMatrix(h5name)
  #   im = MatrixToImage(mat)
  #   imlist.append(im)
  t1 = time.time()
  features = np.zeros([len(h5_list), 12], dtype=np.float)
  # when namx=5, a vec has 21 items, but the real part is the same when l<0, so just calculate l>=0, 12 items.
  for i, f in enumerate(h5_list):
    features[i] = tst_2d_zernike_mom(n, l, f)
  # print "features Matrix:"
  # print features
  t2 = time.time()
  print "time used for getting features matrix: ", t2 - t1
  t3 = time.time()
  tree_list = Clustering.hcluster(cluster_num, features)
  # tree_list_plot = Clustering.hcluster(cluster_num, features)
  t4 = time.time()
  print "time used for clustering: ", t4 - t3
    # input outcome
  print "cluster outcome:"
  t5 = time.time()
  res = open(str(cluster_num)+'_ac_res.dat','w')
  while (len(tree_list)>0):
      for root in tree_list:
          print root.get_cluster_elements()
          print>>res, root.get_cluster_elements()
          tree_list.remove(root)
  t6 = time.time()
  # print "time used for generating result: ", t6 - t5
  # for i in range(len(tree_list_plot)):
  #   if len(tree_list_plot[i].get_cluster_elements())!=1:
  #     clusters = tree_list_plot[i].extract_clusters(0.2 * tree_list_plot[i].distance)
  #     Clustering.draw_dendrogram(tree_list_plot[i],imlist,filename='sunset.pdf')
  #   else:
  #     im.show(imlist[i])
  t_e = time.time()
  print "total time used: ", t_e - t_s
  print "OK"