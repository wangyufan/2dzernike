import matplotlib.pyplot as plt
import sys
import math 



# f1 = open("200_sed_res.dat",'r')
# f1 = open("all_new_anticc763.txt",'r')
f2 = open("200_cc_res.dat",'r')
# f3 = open("100_ac_res.dat",'r')

def plot_one(f, color, lb, start):

  num=[]
  count=0
  cluster=[]

  for ll in f.readlines():
    
    elements=ll.split(",")
    cl = len(elements)
    if cl >1:
      count+=1
    # print cl
      num.append(cl)
      cluster.append(count+start)
  plt.xlabel('cluster number') 
  plt.ylabel('frequency')
  print num
  plt.bar(cluster, num, width=1 , color=color, label=lb) 



# plot_one(f1, 'r', "Standard Euclidean Distance" ,0)
plot_one(f2, 'b', "Pearson correlation coefficient",0.3)
# plot_one(f3, 'g', "adjusted cosine",0.6)
plt.legend(loc = 'upper left')
plt.show()