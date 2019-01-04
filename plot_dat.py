import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image
import hdf5


# df = pd.read_csv('rebuilt.txt', sep=' ', header=None, dtype=str, na_filter=False)
# data=np.read_csv('rebuilt.txt')


# plt.axis('off') 
# plt.show()




def get_arr(filename):
	res = np.zeros((11,11), dtype=np.float)
	p_list=[]
	f1 = open(filename)
	for line in f1.readlines():
		data = line.split(" ")
		value=float(data[2])
		p_list.append(value)
	f1.close()
	v_max=255
	v_min=0
	p_max=max(p_list)
	p_min=min(p_list)
	

	f = open(filename)
	for line in f.readlines():
		data = line.split(" ")
		x=int(data[0])
		y=int(data[1])
		value=float(data[2])
		new_piexl=round((v_max-v_min)*(value-p_min)/(p_max-p_min)+v_min)
		print "----",new_piexl
		res[x][y] = new_piexl
		# if new_piexl<float(50):
		# 	res[x][y] = 0
		# else:
		# 	res[x][y] = 1

	print res	
	f.close()
	return res

                          


name= "rebuilt_nmax-cha"
res = get_arr(name+".dat")

imgData = res
f = h5py.File('cha.h5','w')   
f['trans_data'] = imgData                
f['labels'] = range(121)            
f.close() 

from scipy import misc
res_new_sz = misc.imresize(res,0.999) 
plt.imshow(res_new_sz,cmap='gray')
# plt.imshow(res_new_sz)
plt.axis('off')
# plt.title(name)
plt.show()

plt.savefig(name+"_rbg.png")
# image = Image.open(name+"_rbg.png")
# image_gray = image.convert("1") 
# image_gray.show()
