from skimage import color,data,filters
import skimage.morphology as sm
import skimage.filters.rank as sfr
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from skimage.morphology import disk

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
  f.close()
  return res

def plot_bi(filename):
  image = DatToMatrix(filename)
  # dst =filters.threshold_local(data,11,'median')
  thresh = filters.threshold_yen(image) 
  print "threshold:", thresh
  dst =(image <= thresh)*1.0 
  plt.figure('thresh',figsize=(11,11))
  plt.subplot(121)
  plt.title('original image')
  plt.imshow(image,plt.cm.gray)
  plt.subplot(122)
  plt.title('binary image')
  plt.imshow(dst,plt.cm.gray)
 
  dst1=sm.erosion(image,sm.square(1))
  dst2=sm.erosion(image,sm.square(5))
  dst3=sm.erosion(image,sm.square(6))
  dst4=sm.erosion(image,sm.square(3))
  plt.figure('morphology',figsize=(11,11))
  plt.subplot(141)
  plt.title('morphological image_filter1*1')
  plt.imshow(dst1,plt.cm.gray)
  plt.subplot(142)
  plt.title('morphological image_filter5*5')
  plt.imshow(dst2,plt.cm.gray)
  plt.subplot(143)
  plt.title('morphological image_filter6*6')
  plt.imshow(dst3,plt.cm.gray)
  plt.subplot(144)
  plt.title('morphological image_filter7*7')
  plt.imshow(dst4,plt.cm.gray)

  plt.show()



if __name__ == "__main__":
  plot_bi("/Users/wyf/Desktop/anti_stat/0_25432_rebuilt_nmax4.dat")