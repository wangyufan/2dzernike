from skimage import io
import sys
import h5py
import math
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
import random 


def MatrixToImage(data):
    new_im = Image.fromarray(data)
    return new_im

def ProcessCxi(file, index):
	f_input = h5py.File(file, 'r')
	X_pos = f_input['peak_info/peakXPosRaw'].value
	Y_pos = f_input['peak_info/peakYPosRaw'].value
	data = f_input['data'].value
	pos = zip(X_pos[index], Y_pos[index]) 
	full_img = data[index]
	f_input.close()
	return pos, full_img


if __name__ == "__main__":
	arg = sys.argv[1]
	f_output = h5py.File('crop_test.h5','w')
	#save total data
	data = []
	count = 0
	for num in range(50):
		pos, full_img = ProcessCxi(arg, num)
		for (i,j) in pos:
			if i>3 and j>3:
				# print (i,j)
				image = MatrixToImage(full_img)
				box = (i-4, j-4, i+4, j+4)
				cut_img = image.crop(box)
				count += 1
				cut_arr = np.array(cut_img)
				data.append(cut_arr)
	print count
	f_output.create_dataset('data', data = data)
	#save data for clustering ramdomly
	cluster_data = []
	cluster_ids = []
	total_ids = list(range(0,len(data)))
	cluster_ids = random.sample(total_ids, 4000)
	for index in cluster_ids:
		cluster_data.append(data[index])
	f_output.create_dataset('cluster_data', data = cluster_data)
	f_output.create_dataset('cluster_ids', data = cluster_ids)
	f_output.close()
