import sys
import os
import argparse
from PIL import ImageChops
from PIL import Image
import numpy as np
import h5py
from skimage import io,transform
import imagehash

global radius 
radius = 15
def ahash(image_mat):
	s = 0 
	hash_str = ''
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
	return hash_str

def dhash(image_mat):
	hash_str = ''
	for row in range(radius):
		row_start_index = row * radius
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
	return 1 - np.true_divide(n, radius*radius)

def get_best_mat(add_mat, sum_mat):
	highfreq_factor = 2
	hash_size = 4
	img_size = hash_size * highfreq_factor

	add_mat_arr = [] 
	add_mat_90 =transform.rotate(add_mat, 90)  
	add_mat_180 =transform.rotate(add_mat, 180)  
	add_mat_270 =transform.rotate(add_mat, 270)
	add_mat_arr = np.array([add_mat, add_mat_90, add_mat_180, add_mat_270])
	best_mat = add_mat
	# hash_sum = imagehash.phash(Image.fromarray(sum_mat),hash_size=hash_size,highfreq_factor=highfreq_factor)
	hash_sum = dhash(sum_mat)
	hash_max = 0
	for i in range(4):
		# hash_add = imagehash.phash(Image.fromarray(add_mat_arr[i]),hash_size=hash_size,highfreq_factor=highfreq_factor)
		hash_add = ahash(add_mat_arr[i])
		hash_cmp = cmpHash(hash_add, hash_sum)
		# hash_cmp = 1 - (hash_sum - hash_add)/len(hash_sum.hash)**2
		if hash_cmp > hash_max:
			hash_max = hash_cmp
			# print(hash_max)
			best_mat = add_mat_arr[i].astype(np.int)
	return best_mat



def get_template_mat_v3(cluster_elements, cluster_data):
	sum_mat = np.empty([radius,radius]).astype(np.int)
	elements_list = list(cluster_elements)[0]
	for i in range(len(elements_list)):
		index = elements_list[i]
		add_mat = cluster_data[index].astype(np.int)
		best_mat = get_best_mat(add_mat, sum_mat).astype(np.int)
		sum_mat = (np.add(sum_mat, best_mat)).astype(np.int)
	return sum_mat

def get_template_mat_v2(cluster_elements, cluster_data):
	sum_mat = np.empty([radius,radius],dtype=float)
	elements_list = list(cluster_elements)[0]
	for i in range(len(elements_list)):
		index = elements_list[i]
		add_mat = cluster_data[index]
		sum_mat = np.add(sum_mat, add_mat)
	return sum_mat

def get_res_v2(h5_path, cluster_path):
	h5_data = h5py.File(h5_path,'r')
	cluster_data = h5_data['peak_mat'].value
	h5_cluster = h5py.File(cluster_path,'r')
	cluster_res = h5_cluster['data'].value
	cluster_unique = np.unique(cluster_res)
	cluster_num = len(cluster_unique)
	cluster_type = os.path.basename(cluster_path).split('_')[0]
	print("there are %d clusters." %cluster_num)
	templates = []
	for i in range(cluster_num):
		# p = cluster_res.index(i) usage of list
		cluster_id = i + 1
		cluster_elements = np.where(cluster_res == cluster_id) #usage of nparray
		cluster_size = len(list(cluster_elements)[0])
		print("there are %d elements in cluster %d." %(cluster_size,cluster_id))
		template_sum = get_template_mat_v3(cluster_elements, cluster_data)
		template_mat = np.true_divide(template_sum, cluster_size)
		templates.append(template_mat)
	# print templates
	path = '/Users/wyf/Documents/100f_result/templates/'
	# os.makedirs(path)
	filename = str(cluster_num)+'_'+str(cluster_type)+'_templates.h5'
	output = h5py.File(path + filename,'w')
	output.create_dataset('templates', data = templates)
	output.close()

def get_template_mat(rank, cluster, cluster_data):
	# every element in a cluster have its own index of 4000 cluster data
	index = int(cluster[rank])
	test = [725 , 1224 , 1677 , 2562,  4339,  5606 , 5914, 7722 ,9344 ,10237,10472, 10773, 12049 ,12053, 12159,12205 ,13029,13223, 1 ,16213 ,17016, 19131, 19676]
	# if index in test:
	# 	print("cluster_data[index]",cluster_data[index])
	if rank == 0:
		#return the first element cluster[0] in a cluster
		return cluster_data[index].astype(np.int)
	else:
		img1 = cluster_data[index].astype(np.int)
		img2 = get_template_mat(rank - 1, cluster, cluster_data)
		if  index==986:
			print(index,"===",img1, img2, np.add(img1, img2),img1.dtype)
		return np.add(img1, img2)

def get_res(h5_path, cluster_res, output):
  	h5_file = h5py.File(h5_path,'r')
  	cluster_data = h5_file['cluster_data'].value
  	type_x = 0
  	label = []
  	templates = []
  	with open(cluster_res, 'r') as df:
  		for a_cluster in [d.strip().split('[')[1].split(']')[0].split(', ') for d in df]:
  		#calculate every cluster's template
  			type_x+=1
  			cluster_size = len(a_cluster)
  			template_sum = get_template_mat(cluster_size - 1, a_cluster, cluster_data)
  			template_mat = np.true_divide(template_sum, cluster_size)
  			templates.append(template_mat)
  	output = h5py.File(output,'w')
  	output.create_dataset('templates', data = templates)
  	output.close()

def get_res_v3(h5_path, cluster_path):
	h5_data = h5py.File(h5_path,'r')
	cluster_data = h5_data['peak_mat'].value
	h5_cluster = h5py.File(cluster_path,'r')
	cluster_res = h5_cluster['data'].value
	cluster_unique = np.unique(cluster_res)
	cluster_num = len(cluster_unique)
	cluster_type = os.path.basename(cluster_path).split('_')[0]
	freq = dict(zip(*np.unique(cluster_res, return_counts=True)))
	new_arr=sorted(freq.items(), key=lambda d: d[1], reverse = True)[:100] #[(cluster1, 330), (cluster9, 210)... (cluster5, 33)]
	cluster_num = len(new_arr)
	templates = []
	for i in range(cluster_num):
	# p = cluster_res.index(i) usage of list
		cluster_id = i + 1
		cluster_elements = np.where(cluster_res == new_arr[i][0]) #usage of nparray
		cluster_size = len(list(cluster_elements)[0])
		# print("there are %d elements in cluster %d. original cluster: %d" %(cluster_size,cluster_id,new_arr[i][0]))
		print("there are %d elements in cluster %d. original cluster: %d" %(cluster_size,cluster_id,new_arr[i][0]))
		template_sum = get_template_mat_v3(cluster_elements, cluster_data)
		template_mat = (np.true_divide(template_sum, cluster_size)).astype(np.int)
		templates.append(template_mat)

	path = '/Users/wyf/Documents/now/templates/'
	# os.mkdir(path)
	filename = str(cluster_num)+'_'+str(cluster_type)+'_templates.h5'
	output = h5py.File(path + filename,'w')
	output.create_dataset('templates', data = templates)
	output.close()

def get_res_v4(h5_path, cluster_path):
	h5_data = h5py.File(h5_path,'r')
	cluster_data = h5_data['peak_mat'].value #remove dead point and gap 
	h5_cluster = h5py.File(cluster_path,'r')
	cluster_res = h5_cluster['data'].value # [cluster1, cluster20, cluster3...]
	cluster_unique = np.unique(cluster_res)
	cluster_num = len(cluster_unique)
	cluster_type = os.path.basename(cluster_path).split('_')[0]
	freq = dict(zip(*np.unique(cluster_res, return_counts=True)))
	new_arr=sorted(freq.items(), key=lambda d: d[1], reverse = True)[:200] #[(cluster1, 330), (cluster9, 210)... (cluster5, 33)]
	cluster_num = len(new_arr)
	print("there are %d clusters." %len(new_arr))
	# print(cluster_res,freq)

	templates = []
	for i in range(len(new_arr)):
		# p = cluster_res.index(i) 
		cluster_id = i + 1
		cluster_elements = np.where(cluster_res == new_arr[i][0]) #element_ids should be generated as a list for merging, amount of clusters is not enough
		cluster_size = len(list(cluster_elements)[0])
		print("there are %d elements in cluster %d. original cluster: %d" %(cluster_size,cluster_id,new_arr[i][0]))
		template_sum = get_template_mat_v3(cluster_size-1,cluster_elements[0], cluster_data)
		template_mat = np.true_divide(template_sum, cluster_size)
		if i==199:
			print(template_sum, template_mat, cluster_elements[0])
		templates.append(template_mat)
	# print templates
	path = '/Users/wyf/Documents/100f_result/templates/'
	# os.makedirs(path)
	filename = str(cluster_num)+'_'+str(cluster_type)+'_templates.h5'
	output = h5py.File(path + filename,'w')
	output.create_dataset('templates', data = templates)
	output.close()

if __name__ == '__main__':
	h5_path = '/Users/wyf/Documents/real_data/cluster_data_r15.h5'
	h5_path =  '/Users/wyf/Documents/now/for_cluster.h5'
	# cluster_res = '/Users/wyf/Desktop/anti_stat/200_sed_res.dat'
	# output = '/Users/wyf/Desktop/anti_stat/4_template.h5'
	cluster_dir = '/Users/wyf/Documents/100f_result/cluster_res/'
	files = os.listdir(cluster_dir)
	cluster_list = [os.path.join(cluster_dir, f) for f in files if f.endswith('cluster_res.h5')]
	for cluster in cluster_list:
		get_res_v3(h5_path, cluster)

