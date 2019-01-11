from skimage import io
import sys
import os
import h5py
import math
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
import random 
import multiprocessing
from multiprocessing import Pool
import time


def MatrixToImage(data):
    new_im = Image.fromarray(data)
    return new_im

def ProcessCxi(file, index):
	f_input = h5py.File(file, 'r')
	X_pos = f_input['peak_info/peakXPosRaw'].value
	Y_pos = f_input['peak_info/peakYPosRaw'].value
	data = f_input['data'].value
	# List_set = set(X_pos[index]) 
	# List_set2 = set(Y_pos[index])
	# print(len(List_set), len(List_set2)) 
	# for item in List_set: 
	# 	if list(X_pos[index]).count(item)>1:
	# 		print("the %f has found %d" %(item, list(X_pos[index]).count(item)))
	# for item in List_set2: 
	# 	if list(Y_pos[index]).count(item)>1:
	# 		print("the %f has found %d" %(item, list(Y_pos[index]).count(item)))
	pos = zip(X_pos[index], Y_pos[index]) 
	full_img = data[index]
	f_input.close()
	return pos, full_img

def crop_peak(process_n):

	data = []
	total_count = 0
	path_list = os.listdir(input_path)
	cxi_list = [os.path.join(input_path, f) for f in path_list if f.endswith('.cxi')]
	total_size = 50
	perSize = int(math.ceil(total_size / 4))
	start_line = process_n*perSize
	if (process_n+1)*perSize > total_size:
		end_line = total_size
	else:
	    end_line = (process_n+1)*perSize
	    print("cc_end_line:",end_line)
	for cxi_rank in range(start_line, end_line):
		path = cxi_list[cxi_rank]
		for num in range(frame_num):
			pos, full_img = ProcessCxi(path, num)
			count = 0
			for (i,j) in pos:
				if i>3 and j>3:
					# print (i,j)
					image = MatrixToImage(full_img)
					box = (i-4, j-4, i+4, j+4)
					cut_img = image.crop(box)
					count += 1
					total_count += 1
					cut_arr = np.array(cut_img)
					data.append(cut_arr)
			print("frame %d has %d peaks" %(num, count))
	return data
	# 	if (cxi_rank==0):
	# 		f_output.create_dataset('cluster_data', data = data)
	# 		print("choose %dpeaks of 100 frame in cxijob %d for clustering" %(total_count, cxi_rank))		
	# f_output.create_dataset('data', data = data)


if __name__ == "__main__":
	args = sys.argv[1:]
	input_path = args[0]
	frame_num = int(args[1])
	output_path = args[2]
	f_output = h5py.File(output_path)
	#save total data
	# data = []
	# total_count = 0
	# for num in range(frame_num):
	# 	pos, full_img = ProcessCxi(input_path, num)
	# 	count = 0
	# 	for (i,j) in pos:
	# 		if i>3 and j>3:
	# 			# print (i,j)
	# 			image = MatrixToImage(full_img)
	# 			box = (i-4, j-4, i+4, j+4)
	# 			cut_img = image.crop(box)
	# 			count += 1
	# 			total_count += 1
	# 			cut_arr = np.array(cut_img)
	# 			data.append(cut_arr)
	# 	print("frame %d has %d peaks" %(num, count))
	# f_output.create_dataset('data', data = data)
	# print("total peaks amonut: %d" %total_count)
	#save data for clustering ramdomly
	# cluster_data = []
	# cluster_ids = []
	# total_ids = list(range(0,len(data)))
	# cluster_ids = random.sample(total_ids, 40000)
	# for index in cluster_ids:
	# 	cluster_data.append(data[index])
	# f_output.create_dataset('cluster_data', data = cluster_data)
	# f_output.create_dataset('cluster_ids', data = cluster_ids)
	# f_output.close()

	res = []
	#process pool
	tnlm1 = time.time()
	# pool = multiprocessing.Pool(processes=4)
	# result = pool.map(crop_peak, range(4))
	# for n in range(0,len(result)):
	# 	res += result[n]
	# f_output.create_dataset('data', data = res)
	res=f_output['cluster_data'].value
	print("total peaks amonut: %d" %len(res))
	# f_c = h5py.File('/Users/wyf/Desktop/anti_stat/ccc.h5')
	# f_c.create_dataset('cluster_data', data = res)

	tnlm2 = time.time()
	f_output.close()
	print("time used:", tnlm2 - tnlm1)
