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
import numpy as np  
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans
import Clustering 
import pylab



def preprocess_image(h5file, flag):
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
  	  if flag == 0:
  	  	value = file[x][y]
  	  elif flag == 1:
  	    value = smath.log((float(file[x][y]) + add_value))  #lg value is too small...4 5 6 7...cannot be recognized
  	  elif flag == 2 :
  	  	v_max=255
  	  	value=round((v_max-v_min)*(file[x][y]-p_min)/(p_max-p_min)+v_min)
  	  else :
  	  	v_max=int(max(p_list)/2)
  	  	# print "=------v_max------=",v_max  
  	  	value=round((v_max-v_min)*(file[x][y]-p_min)/(p_max-p_min)+v_min)
  	  image.append([x,y,value])
  	  print>>original, x,y, value
  original.close()
  return image

def tst_2d_zernike_mom(n, l, h5file, flag):
  image = preprocess_image(h5file, flag)
  # image = ImageToDat('cha.png')
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
  nl_array.load_coefs( nls, coefs )
  lfg = math.log_factorial_generator(nmax)
  for nl, c in zip( nls, moments):
    if(abs(c)<1e-3):
      c=0
    feature_maxtix.append(c.real)
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
  	# if value > float(0):  
  	# 	res[x][y] = value 
  	# else:
  	# 	res[x][y] = 0
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
  print data
  im = MatrixToImage(data)
  im.show()

if __name__ == "__main__":
  args = sys.argv[1:]
  t1 = time.time()
  n = 2
  l = 2
  nmax = max(5, n)
  flag = 0 #0-no , 1-log, 2-0~255
  # h5file = '/Users/wyf/Documents/SFX/NoGap/transfered25432.h5'

  # create a list of images
  path = '/Users/wyf/Documents/test_h5'
  h5_list = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.h5')]
  
  features = np.zeros([len(h5_list), 21], dtype=np.float)
  for i, f in enumerate(h5_list):
    features[i] = tst_2d_zernike_mom(n, l, f, flag)
  print "features Matrix:",features
  tree = Clustering.hcluster(features)
  # visualize clusters with some (arbitrary) threshold
  # clusters = tree.extract_clusters(0.2 * tree.distance)
  # # plot images for clusters with more than 3 elements
  # imlist=[]
  # for c in clusters:
  #   elements = c.get_cluster_elements()
  #   print "elements:------",elements,";"
  #   nbr_elements = len(elements)
  #   if nbr_elements > 0:
  #     pylab. figure()
  #     for p in range(pylab.minimum(nbr_elements,20)):
  #       # pylab.subplot(4, 5, p + 1)
  #       h5name = h5_list[elements[p]]
  #       # dat = preprocess_image(h5name, 3)
  #       # mat = DatToMatrix(h5name.split(".")[0]+'_original.dat')
  #       mat = H5ToMatrix(h5name)
  #       im = MatrixToImage(mat)
  #       imlist.append(im)
        # pylab.imshow(im)
        # pylab.axis('off')
  # pylab.show()
  # Clustering.draw_dendrogram(tree,imlist,filename='sunset.pdf')
  t2 = time.time()
  print "time used: ", t2-t1
  print "OK"