import matplotlib.pyplot as plt
import sys
import math 
import h5py
import numpy as np
import os


def get_singe():
  arr =[]
  cluster_dir = '/Users/wyf/Documents/100f_result/cluster_res/'
  files = os.listdir(cluster_dir)
  cluster_list = [os.path.join(cluster_dir, f) for f in files if f.endswith('cluster_res.h5')]
  for path in cluster_list:
    h5_file = h5py.File(path,'r')
    cluster_type = os.path.basename(path).split('_cluster')[0]
    cluster = h5_file['data'].value
    cluster_unique = np.unique(cluster)
    cluster_num = len(cluster_unique)
    freq = dict(zip(*np.unique(cluster, return_counts=True)))
    # print(freq.items())
    freq_s = [x[1] for x in freq.items()]
    # print(sorted(freq_s, reverse = True)[:200])
    
    new_arr=sorted(freq.items(), key=lambda d: d[1], reverse = True)[:200]
    # plt.title(str(cluster_num) +'-clusters distribution of method ' + str(cluster_type))
    arr.append((freq, cluster_type))
  return new_arr, arr




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


def draw(new_arr, arr):
  plt.subplot(121)
  plt.xlabel('cluster number') 
  plt.ylabel('frequency')
  plt.title('Clusters of method ' + str(arr[0][1]))
  plt.bar(arr[0][0].keys(), arr[0][0].values(), width=2 , color='b')
  plt.subplot(122)
  a = [x[0] for x in new_arr]
  b = [x[1] for x in new_arr]
  plt.title('Top 200 clusters of method'+ str(arr[0][1]))
  plt.xlabel('cluster number') 
  plt.bar(a, b,  width=2, color='g')
  # plt.scatter(a, b, s=5)
  # plt.subplot(132)
  # plt.xlabel('cluster number') 
  # plt.ylabel('frequency')
  # plt.title('200-clusters of method ' + str(arr[1][1]))
  # plt.bar(arr[1][0].keys(), arr[1][0].values(), width=1 , color='b')
  # plt.subplot(133)
  # plt.xlabel('cluster number') 
  # plt.ylabel('frequency')
  # plt.title('200-clusters of method ' + str(arr[2][1]))
  # plt.bar(arr[2][0].keys(), arr[2][0].values(), width=1 , color='b')
  plt.show()

if __name__ == "__main__":
  new_arr, arr = get_singe()
  draw(new_arr, arr)
