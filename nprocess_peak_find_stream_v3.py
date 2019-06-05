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

global radius 
radius = 15
def ahash(image_mat):
	s = 0 
	hash_str = ''
	if image_mat.shape[0]==radius and image_mat.shape[1]==radius:
		for i in range(radius):
			for j in range(radius):
				s = s + image_mat[i,j]
				avg = np.true_divide(s, radius*radius)
		for i in range(radius):
			for j in range(radius):
				if image_mat[i,j]>avg:
					hash_str = hash_str+'1'
				else:
					hash_str = hash_str+'0'
	# else:
	# 	print("----bug image_mat----")
	return hash_str


def cmpHash(hash1, hash2):
	n=0
	if len(hash1) != len(hash2):
		return -1
	for i in range(len(hash1)):
		if hash1[i] != hash2[i]:
			n = n + 1
	return 1 - np.true_divide(n, 225)

def calc_intensity_by_mask_0121(mask, mat, flag):
	mask_flat = mask.flatten()
	mat_flat = mat.flatten()
	intensity = float("inf")
	med = np.median(mat_flat)
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
		# if flag:
		# 	print("signal=    ",int(signal))
		# 	print("background=",int(background/background_count))
		# 	print("intensity= ",int(np.divide(signal, signal_count) - np.divide(background, background_count)))
		# intensity = np.divide(signal, signal_count) - np.divide(background, background_count)
		# intensity = signal - signal_count*np.divide(background, background_count)
		# intensity = signal - np.divide(background, background_count)
		intensity = signal - med
	return intensity

def get_xy(filepath):
    file = open(filepath,'r')
    lines  =  file.readlines()
    xy_mat = []
    flag_hkl = False
    one_frame_xy_mat = []
    count = 0
    peak = 0
    for line in lines:
    	linesplit = line.split()
    	if (len(linesplit) == 10):
            if (linesplit[0] == "h"):
            	flag_hkl = True
            	one_frame_xy_mat = []
            	continue #??
    	if (len(linesplit) == 3):
            if (linesplit[0] == "Image"):
            	# Image filename: /Users/wyf/Documents/SFX/kekeke/cxi_hit/r0005/hit5000/r0005-rank1-job0.cxi
            	# cxi_num = int(linesplit[2].split('-')[2].split('.')[0].split('job')[1])
            	# Image filename: /Users/apple001/Documents/TempFiles/DataFromServer/dataCXI/cxilr2816-r0208-c00.cxi
            	cxi_num = int(linesplit[2].split('-')[1].split('r0')[1])
            	# print("cxi_num:", cxi_num)
    	if (len(linesplit) == 2):
        	if(linesplit[0] == "Event:"):
        		frame_num = int(linesplit[1].split('//')[1])
        		# print("frame_num:", frame_num)
        		# count+=1
        		# print(len(xy_mat), "==*********===", count)  , 19944/20w with no reflection frames
    	if (len(linesplit) == 10 and flag_hkl):
            intensity_hkl = linesplit[3]
            # X_hkl = linesplit[7]
            # Y_hkl = linesplit[8]
            X_hkl = linesplit[8]
            Y_hkl = linesplit[7]
            one_frame_xy_mat.append((cxi_num, frame_num, int(float(X_hkl) + 0.5), int(float(Y_hkl) + 0.5)))
    	if (len(linesplit) == 3 and linesplit[0] == "End"):
    		flag_hkl = False
    		xy_mat.append(one_frame_xy_mat)
    file.close()
    print(len(xy_mat))
    return xy_mat

def findTemplate_v2(perSize, process_n, node_n, xy_mat, hash_type, template_path, base_path):
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
	flag=False
	mat_half = 7
	mask_half = 7
	find_template = 1
	count_bug=0
	non_match=0
	for index in range(start_line, end_line):
		#get one frame in a cxi
		cxi_id = xy_mat[index][0][0]
		frame_id = xy_mat[index][0][1]
		x_arr = [x[2] for x in xy_mat[index]]
		y_arr = [x[3] for x in xy_mat[index]]
		# base_path = '/Users/wyf/Documents/SFX/kekeke/cxi_hit/r0005/hit150/'
		# cxi_path = base_path + 'r0005-rank1-job' + str(cxi_id)+'.cxi'
		cxi_path = base_path + 'cxilr2816-r0'+ str(cxi_id)+'-c00.cxi'
		f_cxi = h5py.File(cxi_path, 'r')
		# frames = f_cxi['entry_1/data_1/data'].value
		frames = f_cxi['entry_1/instrument_1/detector_1/detector_corrected/data']
		full_mat = frames[frame_id] #start from 0
		# print("full_mat===============================",full_mat)
		f_cxi.close()
		find_mat = np.zeros([15, 15])
		# if (frame_id ==  79) and (cxi_id == 209):
		for (x, y) in zip(x_arr, y_arr):
			# print( x, y)
			#deal with every peak in a frame
			hash_max = 0
			max_intensity = 0
			image_mat = full_mat[(x - mask_half): (x + mask_half+1), (y - mask_half): (y + mask_half+1)] #click_xy != matrix_xy
			for j in range(len(template_data)):
				if hash_type == 0:
					hash_template = ahash(template_data[j].astype(int))
					hash_image = ahash(image_mat.astype(int))
				elif hash_type == 1:
					hash_template = dhash(template_data[j])
					hash_image = dhash(image_mat)
				else:
					hash_template = imagehash.phash(Image.fromarray(template_data[j]), hash_size=8, highfreq_factor=4)
					hash_image = imagehash.phash(Image.fromarray(image_mat), hash_size=8, highfreq_factor=4)
				hash_cmp = cmpHash(hash_template, hash_image)
				# find template for a (x, y) of 9 possible images
				if int(hash_cmp) == -1:
					count_bug+=1
				elif float(hash_cmp) > float(0.5):
					if hash_cmp > hash_max:
						hash_max = hash_cmp
						find_template = j+1
						find_mat = image_mat
						mask = template_mask[j]
						intensity = calc_intensity_by_mask_0121(mask, image_mat, flag)
						max_intensity = intensity
					if hash_cmp == hash_max:
						# if(int(y)==1105 and int(x)==346):
						# 	print("=====x_left-----",x_left,"-----y_left------",y_left,"----",hash_max,"[",j)
						mask = template_mask[j]
						intensity = calc_intensity_by_mask_0121(mask, image_mat, flag)
						if intensity > max_intensity:
							max_intensity = intensity
							find_template = j+1
							find_mat = image_mat
						# print("==-1bug  cxi_id,frame_id, x,y,  hash_template, hash_image==",count_bug,cxi_id,frame_id,x,y,len(hash_template), len(hash_image))
				# if hash_cmp > hash_max:
				# 	hash_max = hash_cmp
				# 	find_template = j+1
				# 	find_mat = image_mat
				# 	mask = template_mask[j]
				# 	intensity = calc_intensity_by_mask_0121(mask, image_mat, flag)
				# 	max_intensity = intensity
				# if hash_cmp == hash_max:
				# 	mask = template_mask[j]
				# 	intensity = calc_intensity_by_mask_0121(mask, image_mat, flag)
				# 	if intensity > max_intensity:
				# 		max_intensity = intensity
				# 		find_template = j+1
				# 		find_mat = image_mat
				# if int(hash_cmp) == -1:
				# 	count_bug+=1
			if max_intensity == 0:
				non_match+=1

			if (int(y)==420 and int(x)==312) or (int(y)==362 and int(x)==362) or (int(y)==130 and int(x)==322) or (int(y)==1023 and int(x)==160) or (int(y)==85 and int(x)==175) or (int(y)==945 and int(x)==593) or (int(y)==868 and int(x)==166) or (int(y)==1023 and int(x)==160) or (int(y)==427 and int(x)==333) or (int(y)==758 and int(x)==1319) or (int(y)==67 and int(x)==45) or (int(y)==1199 and int(x)==844):
				print("template_mask[",find_template-1,"]")
				print("------hash max----------",hash_max)
				print("cxi_num:", cxi_id,frame_id)
				print("===============================peak_matrix================================")
				print(find_mat.astype(int))
				mask = template_mask[find_template-1]
				print("=============================== mask ================================")
				print(mask)
				print("===============================intensity =================================")
				print("cxi:", cxi_id,"  frame:",frame_id, "  x:",x, "  y:",y,"intensity",max_intensity)
				flag=True

			# mask = template_mask[find_template-1]
			# intensity = calc_intensity_by_mask_0121(mask, find_mat, flag)
			data.append((cxi_id, frame_id, max_intensity))# (x,y) in order in every frame
			flag=False
		print("count_bug",(count_bug/len(template_data)),"non_match",non_match)
	return data

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
	mask_type = os.path.basename(template_mask_path).split('_')[2]
	template_mask = np.load(template_mask_path)
	frame_mat = get_xy(stream_path)# the number of frames
	total_size = len(frame_mat)
	print(frame_mat[0])
	perSize = int(math.ceil(total_size / (process_num*node_num)))#amount of frames pre process
	
	arr = []
	res = []
	base_path = '/home/dongxq/Documents/2d_proj/'
	# base_path = '/Users/wyf/Documents/SFX/kekeke/cxi_hit/r0005/hit150/'
	# base_path = '/Volumes/Untitled/CXI/'
	pool = multiprocessing.Pool(processes=process_num)
	for process_n in range((node_n-1)*process_num, node_n*process_num):
		elem = pool.apply_async(findTemplate_v2, (perSize, process_n, node_n, frame_mat, 0, template_path, base_path))
		arr.append(elem)
	pool.close()
	pool.join()

	for item in arr:
		res.extend(item.get())
	print("get new intensity:",len(res),", processed frames:", total_size)

	# intensity_path = '/Users/wyf/Documents/100f_result/test_cc_235_intensity.npy'
	# intensity_path = base_path+'result/'+str(node_n)+'_20w_cc_235_intensity.npy'
	intensity_path = base_path+'result/2000_intensity_cut_med' + str(0.5) + '_' + str(node_n) + '.npy'
	np.save(intensity_path, res)
	t_2 = time.time()
	print("time used:", t_2 - t_1)

