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


def ImageToDat(filename):
  im = Image.open(filename)
  width,height = im.size
  im = im.convert("L") 
  im.show()
  data = im.getdata()
  new_data = np.reshape(data,(width,height))
  image = flex.vec3_double()
  cha=open('cha.dat','w')
  for x in range(0, width):
	for y in range(0, height):
	  value = new_data[x][y]
	  image.append([x,y,value])
	  print>>cha, x,y, value
  cha.close()
  return image

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
  print "==add_value==",add_value
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
  	  	print "=------v_max------=",v_max  
  	  	value=round((v_max-v_min)*(file[x][y]-p_min)/(p_max-p_min)+v_min)
  	  else :
  	  	v_max=int(max(p_list)/10)
  	  	print "=------v_max------=",v_max  
  	  	value=round((v_max-v_min)*(file[x][y]-p_min)/(p_max-p_min)+v_min)
  	  image.append([x,y,value])
  	  print>>original, x,y, value
  original.close()
  return image

def tst_2d_zernike_mom(n, l, filename, h5file, flag):
  rebuilt=open(filename,'w')
  # image = generate_image()
  # image=ImageToDat("/Users/wyf/Desktop/test11.png")
  image = preprocess_image(h5file, flag)
  # image = ImageToDat('cha.png')

  NP=int(smath.sqrt( image.size() ))  
  N=int(NP/2)
  print"=====",NP, N
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
  # print nl_array.get_coef(n,l)*2

  for nl, c in zip( nls, moments):
    if(abs(c)<1e-3):
      c=0
    print nl, c

  reconst=flex.complex_double(NP**2, 0)
  for nl,c in zip( nls, moments):
    n=nl[0]
    l=nl[1]
    if(l>0):
      c=c*2
    #rzfa = math.zernike_2d_radial(n,l,lfg)
    rap = math.zernike_2d_polynome(n,l) #,rzfa)
    i=0
    for x in range(0,NP):
      x=x-N
      for y in range(0,NP):
        y=y-N
        rr = smath.sqrt(x*x+y*y)/N  
        if rr>1.0:
          value=0.0
        else:
          tt = smath.atan2(y,x)
          value = rap.f(rr,tt)
        reconst[i]=reconst[i]+value*c
        i=i+1

  i = 0
  for x in range(0,NP):
    for y in range(0,NP):
      value=reconst[i].real  
      print>>rebuilt, x,y,value
      i=i+1
  rebuilt.close()

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
  	print x,y,value 
  	# if value > float(0):  
  	# 	res[x][y] = value 
  	# else:
  	# 	res[x][y] = 0
  f.close()
  return res
    
def MatrixToImage(data):
  # data =data*10 #used after lg
  new_im = Image.fromarray(data)
  return new_im

def plot_rebuilt(filename):
  data = DatToMatrix(filename)
  print data
  im = MatrixToImage(data)
  # from scipy import misc
  # new_im = misc.imresize(im,0.999) 
  # im = im.convert("1") 
  im.show()

if __name__ == "__main__":
  args = sys.argv[1:]
  t1 = time.time()
  n = 2
  l = 2
  nmax = max(3, n)
  flag = 0 #0-no , 1-log, 2-0~255
  h5file = '/Users/wyf/Documents/SFX/NoGap/transfered25432.h5'
  output = str(flag)+"_25432_rebuilt_nmax"+str(nmax)+".dat"

  # output = "cha20.dat"
  # output='test.dat'
  # tst_2d_zernike_mom(n, l, output, h5file, flag)
  # plot_rebuilt(output)
  plot_rebuilt(h5file.split(".")[0]+"_original.dat")
  t2 = time.time()
  print "time used: ", t2-t1
  print "output:",output
  print "OK"
