import matplotlib.pyplot as plt
import sys
import math 
import h5py
import numpy as np
import os

cluster_dir = '/Users/wyf/Documents/test_doc/40cluster_res/'
files = os.listdir(cluster_dir)
cluster_list = [os.path.join(cluster_dir, f) for f in files if f.endswith('cluster_res.h5')]
for path in cluster_list:
  h5_file = h5py.File(path,'r')
  cluster_type = os.path.basename(path).split('_cluster')[0]
  cluster = h5_file['data'].value
  cluster_unique = np.unique(cluster)
  cluster_num = len(cluster_unique)
  freq = dict(zip(*np.unique(cluster, return_counts=True)))
  plt.bar(freq.keys(), freq.values(), width=1 , color='b')
  plt.xlabel('cluster number') 
  plt.ylabel('frequency')
  plt.title(str(cluster_num) +'-clusters distribution of method ' + str(cluster_type))
  plt.show()
# def plot_one(f, color, lb, start):

#   num=[]
#   count=0
#   cluster=[]

  # for ll in f.readlines():
    # elements=ll.split(" ")
    # print elements
    # cl = len(elements)
    # if cl >1:
    #   count+=1
    #   num.append(cl)
    #   cluster.append(count+start)
  # plt.xlabel('cluster number') 
  # plt.ylabel('frequency')
  # plt.bar(ll, num, width=1 , color=color, label=lb) 




# plot_one(f1, 'r', "Standard Euclidean Distance" ,0)
# plot_one(f2, 'b', "Pearson correlation coefficient",0.3)
# plot_one(f3, 'g', "adjusted cosine",0.6)
# plot_one(f, 'r', 'cluster result', 0.6)
# plt.legend(loc = 'upper left')
# plt.show()