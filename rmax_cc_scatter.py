import matplotlib.pyplot as plt
import sys
import math 




# f1 = open("all_new_aanticc763.txt",'r')
# f2 = open("all_new_anticc595.txt",'r')
# f3 = open("all_new_anticc1452.txt",'r')

def plot_one(f, color):
  active_cc=[]
  active_num=[]
  moderate_cc = []
  moderate_num = []
  inactive_cc=[]
  inactive_num=[]


  for ll in f.readlines():
    elements=ll.split(",")
    sortnum = elements[0].split("(")[1]
    # if int(sortnum) < 101 and int(sortnum)>1:
      # print elements
    sortnum = elements[7].split(")")[0]
    cc = elements[3]
    # active_cc.append(float(cc))
    # active_num.append(float(rmax_diff))
      #'Active' != Active, ' ' has to been removed
    activity = elements[6].split()[0].split(",")[0].split()[0].split("'")[1]
    if activity == 'Active':
      active_cc.append(float(cc))
      active_num.append(float(sortnum))
    elif activity == 'Moderate':
      moderate_cc.append(float(cc))
      moderate_num.append(float(sortnum))
    else:
      inactive_cc.append(float(cc))
      inactive_num.append(float(sortnum))


  plt.xlabel('rmax_diff') 
  plt.ylabel('cc')
  plt.scatter(inactive_num, inactive_cc, c=color[2], s=5, marker='+',label ='Inactive')
  plt.scatter(active_num, active_cc, c=color[0], s=50, marker='o', label ='Active')
  plt.scatter(moderate_num, moderate_cc, c=color[1], s=40, marker='^',label ='Moderate')



color1 = ('g', 'b', 'r')
filename = "cc_rmax586.txt"
f1 = open(filename,'r')
plt.xlim(xmin=0)
plt.ylim(ymin=0)
plt.xlim(xmax=50)
plt.title('cc and rmax_diff distribution of molecular alldata_'+ filename.split(".")[0].split("rmax")[1], fontsize=16)
plot_one(f1, color1)
# plot_one(f2, color2)
# plot_one(f3, color3)
plt.legend(loc = 'upper right')
plt.show()