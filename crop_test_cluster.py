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
import Clustering_v2
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import pylab



def preprocess_image(file):
  image = flex.vec3_double()
  # original = open(h5file.split(".")[0]+'_original.dat','w')
  size = len(file)
  for x in range(0, size):
    for y in range(0, size):
      value = file[x][y]
      image.append([int(x),int(y),float(value)])
      # print>>original, x,y, value
  # original.close()
  return image

def tst_2d_zernike_mom(n, l, file):
  image = preprocess_image(file)
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
    # feature_maxtix.append(abs(c))
    feature_maxtix.append(abs(c))
    # print nl,c
  return feature_maxtix


if __name__ == "__main__":
  args = sys.argv[1:]
  cluster_num = args[0]
  cluster_type = args[1]
  t_s = time.time()
  n = 2
  l = 2
  nmax = max(5, n)
  # path = '/Users/wyf/Desktop/anti_stat/crop.h5'
  # path2 = '/Users/wyf/Desktop/anti_stat/crop248.h5'
  # file1 = h5py.File('crop.h5','r')
  # file2 = h5py.File('crop248.h5','r')
  # cluster_h5 = file1['data'].value + file2['data'].value

  # path = '/Users/wyf/Desktop/anti_stat/crop_.h5'
  path = '/Users/wyf/Documents/real_data/cluster_data.h5'
  h5_file = h5py.File(path,'r')
  # cluster_h5 = h5_file['data'].value
  cluster_h5 = h5_file['peak_mat'].value
  # print "----",cluster_h5
  # imlist=[]  
  # for p in range(len(cluster_h5)):
  #   # pylab.subplot(4, 5, p + 1)
  #   h5name = cluster_h5[p]
  #   mat = H5ToMatrix(h5name)
  #   im = MatrixToImage(mat)
  #   imlist.append(im)
  t1 = time.time()
  features = np.zeros([len(cluster_h5), 12], dtype=np.float)
  # when namx=5, a vec has 21 items, but the real part is the same when l<0, so just calculate l>=0, 12 items.
  i = 0
  for f in cluster_h5:
    features[i] = tst_2d_zernike_mom(n, l, f)
    i += 1
  # print "features Matrix:"
  # print features
  t2 = time.time()
  print("time used for getting features matrix: ", t2 - t1)
  t3 = time.time()
  print(cluster_type)
  tree_list = Clustering_v2.hcluster(features, cluster_num, cluster_type) #set cluster_num as x
  # Clustering_v2.hcluster(features, cluster_num, 'b')
  # Clustering_v2.hcluster(features, cluster_num, 'cos')
  # Clustering_v2.hcluster(features, cluster_num, 's')
  # Clustering_v2.hcluster(features, cluster_num, 'm')
  # Clustering_v2.hcluster(features, cluster_num, 'e')

  
  # tree_list = Clustering.hcluster(cluster_num, features)
  # tree_list_plot = Clustering.hcluster(cluster_num, features)
    # input outcome

  # print "cluster outcome:"
  # t5 = time.time()
  # res = open(str(cluster_num)+'_sed_res40.dat','w')
  # while (len(tree_list)>0):
  #     for root in tree_list:
  #         print root.get_cluster_elements()
  #         print>>res, root.get_cluster_elements()
  #         tree_list.remove(root)
  # t6 = time.time()


  # print "time used for generating result: ", t6 - t5
  # for i in range(len(tree_list_plot)):
  #   if len(tree_list_plot[i].get_cluster_elements())!=1:
  #     clusters = tree_list_plot[i].extract_clusters(0.2 * tree_list_plot[i].distance)
  #     Clustering.draw_dendrogram(tree_list_plot[i],imlist,filename='sunset.pdf')
  #   else:
  #     im.show(imlist[i])
  t_e = time.time()
  print("total time used: ", t_e - t_s)