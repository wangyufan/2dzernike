#coding:utf-8
import sys
import os
import os.path
import argparse
from PIL import ImageChops
import numpy as np
import h5py

def get_template_mat(rank, cluster, cluster_data):
	# every element in a cluster have its own index of 4000 cluster data
	index = int(cluster[rank])
	if rank == 0:
		#return the first element cluster[0] in a cluster
		return cluster_data[index]
	else:
		img1 = cluster_data[index]
		img2 = get_template_mat(rank - 1, cluster, cluster_data)
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
			type_x += 1
			cluster_size = len(a_cluster)
			template_sum = get_template_mat(cluster_size - 1, a_cluster, cluster_data)
			template_mat = np.true_divide(template_sum, cluster_size)
			templates.append(template_mat)
	output = h5py.File(output,'w')
	output.create_dataset('templates', data = templates)
	output.close()


if __name__ == '__main__':
	h5_path = '/Users/wyf/Desktop/anti_stat/crop_test.h5'
	cluster_res = '/Users/wyf/Desktop/anti_stat/200_sed_res.dat'
	output = '/Users/wyf/Desktop/anti_stat/200_template.h5'
	get_res(h5_path, cluster_res, output)

