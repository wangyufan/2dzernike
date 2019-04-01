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
from operator import itemgetter
import imagehash
import argparse

def ahash(image_mat):
	s = 0 
	hash_str = ''
	for i in range(8):
		for j in range(8):
			s = s + image_mat[i,j]
			avg = np.true_divide(s, 64)
	for i in range(8):
		for j in range(8):
			if image_mat[i,j]>avg:
				hash_str = hash_str+'1'
			else:
				hash_str = hash_str+'0'
	return hash_str

def dhash(image_mat):
	hash_str = ''
	for row in range(8):
		row_start_index = row * 8
		for col in range(7):
			if image_mat[row, col] > image_mat[row, col + 1]:
				hash_str = hash_str+'1'
			else:
				hash_str = hash_str+'0'
	return hash_str


def cmpHash(hash1, hash2):
	n=0
	if len(hash1) != len(hash2):
		return -1
	for i in range(len(hash1)):
		if hash1[i] != hash2[i]:
			n = n + 1
	return 1 - np.true_divide(n, 64)

def calc_intensity_by_mask_0121(mask, mat):
	mask_flat = mask.flatten()
	mat_flat = mat.flatten()
	intensity = float("inf")
	if (len(mat_flat) == len(mask_flat)):
		background = 0
		signal = 0
		background_count = 0
		signal_count = 0
		for i in range(len(mask_flat)):
			pixel = mat_flat[i]
			if (int(mask_flat[i]) == 1):
				background += pixel
				background_count +=1
			elif (int(mask_flat[i]) == 0):
				signal += pixel
				signal_count +=1
		intensity = np.divide(signal, signal_count) - np.divide(background, background_count)
        #intensity=signal-signal_count*np.divide(background,background_count)
	return intensity

def findTemplate(perSize, process_n, node_n, xy_mat, hash_type, template_path, base_path):
	template = h5py.File(template_path, 'r') 
	template_data = template['templates'].value
	total_size = len(xy_mat)
	start_line = process_n*perSize
	if (process_n+1)*perSize > total_size:
		end_line = total_size
		print("last_end_line:",end_line)
	else:
	    end_line = (process_n+1)*perSize
	    print("end_line:",end_line)
	data = []
	for index in range(start_line, end_line):
		#get one frame in a cxi
		cxi_id = xy_mat[index][0][0]
		frame_id = xy_mat[index][0][1]
		x_arr = [x[2] for x in xy_mat[index]]
		y_arr = [x[3] for x in xy_mat[index]]
		# base_path = '/Users/wyf/Documents/SFX/kekeke/cxi_hit/r0005/hit150/'
		cxi_path = base_path + 'r0005-rank1-job' + str(cxi_id)+'.cxi'
		f_cxi = h5py.File(cxi_path, 'r')
		frames = f_cxi['entry_1/data_1/data'].value
		full_mat = frames[frame_id] #start from 0
		f_cxi.close()
		for (x, y) in zip(x_arr, y_arr):
			#deal with every peak in a frame 
			image_mat = full_mat[(x - 4): (x + 4), (y - 4): (y + 4)]
			hash_max = 0
			for j in range(len(template_data)):
				if hash_type == 0:
					hash_template = ahash(template_data[j])
					hash_image = ahash(image_mat)
				elif hash_type == 1:
					hash_template = dhash(template_data[j])
					hash_image = dhash(image_mat)
				else:
					hash_template = imagehash.phash(Image.fromarray(template_data[j]), hash_size=8, highfreq_factor=4)
					hash_image = imagehash.phash(Image.fromarray(image_mat), hash_size=8, highfreq_factor=4)
				hash_cmp = cmpHash(hash_template, hash_image)
				if hash_cmp > hash_max:
					hash_max = hash_cmp
					find_template = j+1
			mask = template_mask[find_template-1]
			intensity = calc_intensity_by_mask_0121(mask, image_mat)
			data.append((cxi_id, frame_id, intensity))# (x,y) in order in every frame
			print(cxi_id, frame_id, x, y, intensity)
	return data

def get_xy(filepath):
    file = open(filepath,'r')
    lines  =  file.readlines()
    xy_mat = []
    flag_hkl = False
    one_frame_xy_mat = []
    count = 0
    for line in lines:
    	linesplit = line.split()
    	if (len(linesplit) == 10):
            if (linesplit[0] == "h"):
            	flag_hkl = True
            	one_frame_xy_mat = []
            	continue #??
    	if (len(linesplit) == 3):
            if (linesplit[0] == "Image"):
            	# Image filename: /Users/wyf/Documents/SFX/keke/cxi_hit/r0004/hit5000/r0004-rank1-job0.cxi
            	cxi_num = int(linesplit[2].split('-')[2].split('.')[0].split('job')[1])
            	print("cxi_num:", cxi_num)
    	if (len(linesplit) == 2):
        	if(linesplit[0] == "Event:"):
        		frame_num = int(linesplit[1].split('//')[1])
        		# print("frame_num:", frame_num)
        		# count+=1
        		# print(len(xy_mat), "==*********===", count)  , 19944/20w with no reflection frames
    	if (len(linesplit) == 10 and flag_hkl):
            intensity_hkl = linesplit[3]
            X_hkl = linesplit[8]
            Y_hkl = linesplit[7]
            one_frame_xy_mat.append((cxi_num, frame_num, int(float(X_hkl) + 0.5), int(float(Y_hkl) + 0.5)))
    	if (len(linesplit) == 3 and linesplit[0] == "End"):
    		flag_hkl = False
    		xy_mat.append(one_frame_xy_mat)
    file.close()
    return xy_mat


if __name__ == "__main__":
	t_1 = time.time()
	parser = argparse.ArgumentParser()
	# parser.add_argument("-output", help="result intensity path", type=str)
	parser.add_argument("-input", help="input stream path", type=str)
	parser.add_argument("-processnum", help="processnum number", type=int)
	parser.add_argument("-node", help="node number", type=int)
	parser.add_argument("-node_n", help="node number", type=int)
	parser.add_argument("-template", help="template path", type=str)
	parser.add_argument("-mask", help="mask path", type=str)

	args = parser.parse_args()
	stream_path = args.input
	template_path = args.template
	# intensity_path = args.output
	node_num = args.node
	node_n = args.node_n
	process_num = args.processnum
	template_mask_path = args.mask
	# template_mask_path = '/Users/wyf/Documents/100f_result/templates/signal_235_braycurtis_mask.npy'
	template_mask = np.load(template_mask_path)
	frame_mat = get_xy(stream_path)# the number of frames
	total_size = len(frame_mat)
	print(total_size)
	perSize = int(math.ceil(total_size / (process_num*node_num)))#amount of frames pre process
	
	arr = []
	res = []
	base_path = '/home/dongxq/Documents/2d_proj/'
	pool = multiprocessing.Pool(processes=process_num)
	for process_n in range((node_n-1)*process_num, node_n*process_num):
		elem = pool.apply_async(findTemplate, (perSize, process_n, node_n, frame_mat, 0, template_path, base_path))
		arr.append(elem)
	pool.close()
	pool.join()

	for item in arr:
		res.extend(item.get())
	print("get new intensity:",len(res),", processed frames:", total_size)

	# intensity_path = '/Users/wyf/Documents/100f_result/20w_b_235_intensity.npy'
	intensity_path = base_path+'result/'+str(node_n)+'_20w_cc_1.5_intensity.npy'
	np.save(intensity_path, res)
	t_2 = time.time()
	print("time used:", t_2 - t_1)

