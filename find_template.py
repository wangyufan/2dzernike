#coding:utf-8
import sys
import os
import os.path
import argparse
import numpy as np
import h5py
from PIL import Image
import matplotlib.pyplot as plt
import imagehash
import time
import multiprocessing
from multiprocessing import Pool
import math

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

# def draw(arr):
# 	plt.figure("correct")
# 	img_arr = []
# 	for i in arr:
# 		img = Image.open(i)
# 		img_arr.append(img)
# 	# len_arr = len(arr)
# 	# if len_arr >0 :
# 	# 	for i in arr:
# 	# 		img = Image.open(i)
# 	# 		img_arr.append(img)
# 	# 	print len(arr)
# 	# 	for j in range(len_arr):
# 		# plt.subplot(481+j)
# 	plt.subplot(241)
# 	plt.imshow(img_arr[0])
# 	plt.subplot(242)
# 	plt.imshow(img_arr[1])
# 	plt.subplot(243)
# 	plt.imshow(img_arr[2])
# 	plt.subplot(244)
# 	plt.imshow(img_arr[3])
# 	plt.subplot(245)
# 	plt.imshow(img_arr[4])
# 	plt.subplot(246)
# 	plt.imshow(img_arr[5])
# 	plt.subplot(247)
# 	plt.imshow(img_arr[6])
# 	plt.subplot(248)
# 	plt.imshow(img_arr[7])
# 	plt.show()

# def findTemplate(cluster_path, template_path, h5_path, ahash_path, hash_type):
# 	cluster_file = h5py.File(h5_path,'r')
# 	cluster_data = cluster_file['cluster_data'].value
# 	cluster_res = open(cluster_path)
# 	template = h5py.File(template_path, 'r') 
# 	template_data = template['templates'].value
# 	ahash_res = open(ahash_path,'w')
# 	cluster_num = 0
# 	for line in cluster_res.readlines():
# 		cluster_num += 1
# 		cl_list = line.split('[')[1].split(']')[0].split()
# 		for cl in cl_list:
# 			index = int(cl.split(',')[0])
# 			ahash_max = 0
# 			image_mat = cluster_data[index]
# 			# if index == 2747:
# 			for j in range(len(template_data)):
# 				if hash_type == 0:
# 					ahash_template = ahash(template_data[j])
# 					ahash_image = ahash(image_mat)
# 				else:
# 					ahash_template = dhash(template_data[j])
# 					ahash_image = dhash(image_mat)
# 				ahash_cmp = cmpHash(ahash_template, ahash_image)
# 				if ahash_cmp > ahash_max:
# 					ahash_max = ahash_cmp
# 					find_template = j+1
# 				print(ahash_max)
# 			print >> ahash_res, (index, cluster_num, find_template, ahash_max)
# 	cluster_res.close()
# 	ahash_res.close()

# def findTemplate_v2(cluster_path, template_path, h5_path, hash_dir, hash_type):
# 	cluster_file = h5py.File(h5_path,'r')
# 	cluster_data = cluster_file['cluster_data'].value
# 	h5_cluster = h5py.File(cluster_path,'r')
# 	cluster_res = h5_cluster['data'].value
# 	cluster_type = os.path.basename(cluster_path).split('_')[0]
# 	elements_list = list(cluster_res)
# 	template = h5py.File(template_path, 'r') 
# 	template_data = template['templates'].value
# 	if hash_type == 0:
# 		filename = str(cluster_type)+'_ahash_res.dat'
# 	elif hash_type == 1:
# 		filename = str(cluster_type)+'_dhash_res.dat'
# 	else:
# 		filename = str(cluster_type)+'_phash_res.dat'
# 	hash_path = os.path.join(hash_dir, filename)

# 	hash_res = open(hash_path,'w')
# 	cluster_num = 0
# 	for index in range(len(elements_list)):
# 		cluster_id = elements_list[index]
# 		hash_max = 0
# 		image_mat = cluster_data[index]
# 		# if index == 2747:
# 		for j in range(len(template_data)):
# 			if hash_type == 0:
# 				hash_template = ahash(template_data[j])
# 				hash_image = ahash(image_mat)
# 			elif hash_type == 1:
# 				hash_template = dhash(template_data[j])
# 				hash_image = dhash(image_mat)
# 			else:
# 				hash_template = imagehash.phash(Image.fromarray(template_data[j]), hash_size=8, highfreq_factor=4)
# 				hash_image = imagehash.phash(Image.fromarray(image_mat), hash_size=8, highfreq_factor=4)
# 			hash_cmp = cmpHash(hash_template, hash_image)
# 			# print(hash_template)
# 			# hash_cmp = 1 - (hash_template - hash_image)/len(hash_template.hash)**2
# 			if hash_cmp > hash_max:
# 				hash_max = hash_cmp
# 				find_template = j+1
# 			print(hash_max)
# 		# print >> hash_res, (index, cluster_id, find_template, hash_max)
# 		hash_res.write(str(index)+','+str(cluster_id)+','+str(find_template)+','+str(hash_max)+'\n') 
# 	hash_res.close()


# def findTemplate_v3(template_path, h5_path, hash_dir, hash_type):
# 	cluster_file = h5py.File(h5_path,'r')
# 	cluster_data = cluster_file['data'].value
# 	template = h5py.File(template_path, 'r') 
# 	template_data = template['templates'].value
# 	cluster_type = os.path.basename(template_path).split('_templates')[0]
# 	if hash_type == 0:
# 		filename = str(cluster_type)+'_ahash_res.dat'
# 	elif hash_type == 1:
# 		filename = str(cluster_type)+'_dhash_res.dat'
# 	else:
# 		filename = str(cluster_type)+'_phash_res.dat'
# 	hash_path = os.path.join(hash_dir, filename)

# 	hash_res = open(hash_path,'w')
# 	cluster_num = 0
# 	for index in range(len(cluster_data)):
# 		hash_max = 0
# 		image_mat = cluster_data[index]
# 		# if index == 2747:
# 		for j in range(len(template_data)):
# 			if hash_type == 0:
# 				hash_template = ahash(template_data[j])
# 				hash_image = ahash(image_mat)
# 			elif hash_type == 1:
# 				hash_template = dhash(template_data[j])
# 				hash_image = dhash(image_mat)
# 			else:
# 				hash_template = imagehash.phash(Image.fromarray(template_data[j]), hash_size=8, highfreq_factor=4)
# 				hash_image = imagehash.phash(Image.fromarray(image_mat), hash_size=8, highfreq_factor=4)
# 			hash_cmp = cmpHash(hash_template, hash_image)
# 			# print(hash_template)
# 			# hash_cmp = 1 - (hash_template - hash_image)/len(hash_template.hash)**2
# 			if hash_cmp > hash_max:
# 				hash_max = hash_cmp
# 				find_template = j+1
# 			print(hash_max)
# 		# print >> hash_res, (index, cluster_id, find_template, hash_max)
# 		hash_res.write(str(index)+','+str(find_template)+','+str(hash_max)+'\n') 
# 	hash_res.close()

def findTemplate_v4(template_path, h5_path, hash_dir, hash_type, template_intensity, cxi_path):
	cluster_file = h5py.File(h5_path,'r+')
	cxi_file = h5py.File(cxi_path,'a')
	cluster_data = cluster_file['data'].value
	template = h5py.File(template_path, 'r') 
	template_data = template['templates'].value
	cluster_type = os.path.basename(template_path).split('_templates')[0]
	if hash_type == 0:
		filename = str(cluster_type)+'_ahash_res.dat'
	elif hash_type == 1:
		filename = str(cluster_type)+'_dhash_res.dat'
	else:
		filename = str(cluster_type)+'_phash_res.dat'
	# hash_path = os.path.join(hash_dir, filename)
	# hash_res = open('/Users/wyf/Documents/test_doc/aaa.txt','w')
	cluster_num = 0
	intensity_data = []
	for index in range(len(cluster_data)):
		hash_max = 0
		image_mat = cluster_data[index]
		# if index == 2747:
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
			# print(hash_template)
			# hash_cmp = 1 - (hash_template - hash_image)/len(hash_template.hash)**2
			if hash_cmp > hash_max:
				hash_max = hash_cmp
				find_template = j+1
			print(template_intensity[find_template-1])
		intensity_data.append(template_intensity[find_template-1])
		# hash_res.write(str(index)+','+ str(find_template) + ','+str(hash_max)+'\n') 
	# hash_res.close()
	cluster_file.close()
	cxi_file.create_dataset('sim_intensity', data = intensity_data)
	cxi_file.close()

def calc_intensity_by_mask(mask, mat):
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
			if (mask_flat[i]):
				background += pixel
				background_count +=1
			else:
				signal += pixel
				signal_count +=1
		intensity = np.divide(signal, signal_count) - np.divide(background, background_count)
	return intensity

def findTemplate_v5(process_n):
	cluster_file = h5py.File(h5_path)
	# cxi_file = h5py.File(cxi_path)
	cluster_data = cluster_file['data'].value
	template = h5py.File(template_path, 'r') 
	template_data = template['templates'].value
	cluster_type = os.path.basename(template_path).split('_templates')[0]
	if hash_type == 0:
		filename = str(cluster_type)+'_ahash_res.dat'
	elif hash_type == 1:
		filename = str(cluster_type)+'_dhash_res.dat'
	else:
		filename = str(cluster_type)+'_phash_res.dat'
	# hash_path = os.path.join(hash_dir, filename)
	
	total_size = len(cluster_data)
	# total_size = 40
	perSize = int(math.ceil(total_size / 4))
	start_line = process_n*perSize
	if (process_n+1)*perSize > total_size:
		end_line = total_size
		print("last_end_line:",end_line)
	else:
	    end_line = (process_n+1)*perSize
	    print("end_line:",end_line)

	cluster_num = 0
	intensity_data = []
	for index in range(start_line, end_line):
		hash_max = 0
		image_mat = cluster_data[index]
		# if index == 2747:
		for j in range(start_line, end_line):
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
			# print(hash_template)
			# hash_cmp = 1 - (hash_template - hash_image)/len(hash_template.hash)**2
			if hash_cmp > hash_max:
				hash_max = hash_cmp
				find_template = j+1
			mask = template_mask[find_template-1]
			intensity = calc_intensity_by_mask(mask, image_mat)	
		print(index, intensity)
		intensity_data.append((index, intensity))
		# hash_res.write(str(index)+','+ str(intensity)+'\n') 
	# np.save(hash_res, intensity_data)
	# hash_res.close()
	cluster_file.close()
	# cxi_file.create_dataset('c_0.4_intensity', data = intensity_data)
	# cxi_file.close()
	return intensity_data


def calAccurate(hash_dir):
	res_list = [os.path.join(hash_dir, f) for f in os.listdir(hash_dir) if f.endswith('hash_res.dat')]
	for file in res_list:
		ahash_res = open(file)
		count = 0
		img_arr = []
		# plt.subplot(141)
		for line in ahash_res.readlines():
			res_list = line.split(',')
			# index = res_list[0].split('(')[1]
			index = res_list[0]
			cluster = res_list[1]
			template =  res_list[2]

			if cluster == template:
				# print line
				# cluster_index = '/Users/wyf/Documents/test_doc/crop_image_40_'+str(int(cluster))+"_"+index+".jpg"
				count +=1
				# if count<10:
				# 	img_arr.append(cluster_index)
		# draw(img_arr)
		tip = os.path.basename(file).split('_res')[0]+': '+ str(count)+'/ 40 = '+ str(np.true_divide(count, 40)) 
		print(tip)
	return 1

def calAccurate_v2(hash_dir, cluster_type):
	res_list = [os.path.join(hash_dir, f) for f in os.listdir(hash_dir) if f.find(str(cluster_type)) == 0]
	for file in res_list:
		ahash_res = open(file)
		count = 0
		img_arr = []
		for line in ahash_res.readlines():
			res_list = line.split(',')
			index = res_list[0].split('(')[1]
			cluster = res_list[1]
			template =  res_list[2]
			if cluster == template:
				count +=1
				if count<10 :
					cluster_index = '/Users/wyf/Documents/test_doc/crop_image_40_'+str(cluster_type)+"/"+str(int(cluster))+'_'+index+".jpg"
					img_arr.append(cluster_index)
		draw(img_arr)
		tip = os.path.basename(file).split('_res')[0]+': '+ str(count)+'/ 40 = '+ str(np.true_divide(count, 40)) 
		print(tip)
	return 1

if __name__ == '__main__':

	h5_path = '/Users/wyf/Desktop/anti_stat/crop5000.h5'
	# cluster_path = '/Users/wyf/Desktop/anti_stat/200_sed_res.dat'
	cluster_dir = '/Users/wyf/Documents/100f_result/cluster_res/'
	template_dir = '/Users/wyf/Documents/100f_result/templates/'
	hash_dir = '/Users/wyf/Documents/100f_result/hash_res/'
	# template_intensity_path = '/Users/wyf/Documents/100f_result/templates/signal_0.2_correlation_intensity.npy'
	template_mask_path = '/Users/wyf/Documents/100f_result/templates/signal_0.3_correlation_mask.npy'
	cxi_path = '/Users/wyf/Documents/SFX/keke/cxi_hit/r0004/hit5000/r0004-rank1-job0.cxi'
	template_path = '/Users/wyf/Documents/100f_result/templates/100_correlation_templates.h5'
	# template_intensity = np.load(template_intensity_path)
	template_mask = np.load(template_mask_path)
	cluster_files = os.listdir(cluster_dir)
	cluster_list = [os.path.join(cluster_dir, f) for f in cluster_files if f.endswith('cluster_res.h5')]
	templates_files = os.listdir(template_dir)
	# for cluster_path in cluster_list:
	# 	cluster_type = os.path.basename(cluster_path).split('_')[0]
	# 	filename = list(filter(lambda x: x.endswith(str(cluster_type) + '_templates.h5'), templates_files))[0]
	# 	template_path = os.path.join(template_dir, filename)
	# 	# findTemplate_v2(cluster_path, template_path, h5_path, hash_dir, 2)
	# 	findTemplate_v2(cluster_path, template_path, h5_path, hash_dir, 1)
	# 	findTemplate_v2(cluster_path, template_path, h5_path, hash_dir, 0)	
	# 	# calAccurate_v2(hash_dir, cluster_type)
	# calAccurate(hash_dir)

	# findTemplate_v3(template_path, h5_path, hash_dir, 1)
	# findTemplate_v4(template_path, h5_path, hash_dir, 1, template_intensity, cxi_path)
	t1 = time.time()
	# findTemplate_v5(template_path, h5_path, hash_dir, 1, template_mask, cxi_path)
	hash_type = 1
	pool = multiprocessing.Pool(processes=4)
	result = pool.map(findTemplate_v5, range(4))
	res=[]
	cxi_file = h5py.File(cxi_path)
	print(result[0])
	for n in range(4):
		res += result[n]
	hash_res = open('/Users/wyf/Documents/100f_result/c_0.4_intensity.txt','w')
	np.save('/Users/wyf/Documents/100f_result/c_0.4_intensity.txt', res)
	# cxi_file.create_dataset('c_4_intensity', data = res)
	# cxi_file.attrs['c_4_intensity'][:] = res
	cxi_file.close()
	t2 = time.time()
	print("total time used:%d" %(t2-t1))



