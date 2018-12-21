#coding:utf-8
import sys
import os
import os.path
import argparse
import numpy as np
import h5py
from PIL import Image
import matplotlib.pyplot as plt

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

def findTemplate(cluster_path, template_path, h5_path, ahash_path, hash_type):
	cluster_file = h5py.File(h5_path,'r')
	cluster_data = cluster_file['cluster_data'].value
	cluster_res = open(cluster_path)
	template = h5py.File(template_path, 'r') 
	template_data = template['templates'].value
	ahash_res = open(ahash_path,'w')
	cluster_num = 0
	for line in cluster_res.readlines():
		cluster_num += 1
		cl_list = line.split('[')[1].split(']')[0].split()
		for cl in cl_list:
			index = int(cl.split(',')[0])
			ahash_max = 0
			image_mat = cluster_data[index]
			# if index == 2747:
			for j in range(len(template_data)):
				if hash_type == 0:
					ahash_template = ahash(template_data[j])
					ahash_image = ahash(image_mat)
				else:
					ahash_template = dhash(template_data[j])
					ahash_image = dhash(image_mat)
				ahash_cmp = cmpHash(ahash_template, ahash_image)
				if ahash_cmp > ahash_max:
					ahash_max = ahash_cmp
					find_template = j+1
				print ahash_max,find_template
			print >> ahash_res, (index, cluster_num, find_template, ahash_max)
	cluster_res.close()
	ahash_res.close()

def draw(arr):
	plt.figure("correct")
	img_arr = []
	print arr
	for i in arr:
		img = Image.open(i)
		img_arr.append(img)
	plt.subplot(241)
	plt.imshow(img_arr[0])
	plt.subplot(242)
	plt.imshow(img_arr[1])
	plt.subplot(243)
	plt.imshow(img_arr[2])
	plt.subplot(244)
	plt.imshow(img_arr[3])
	plt.subplot(245)
	plt.imshow(img_arr[4])
	plt.subplot(246)
	plt.imshow(img_arr[5])
	plt.subplot(247)
	plt.imshow(img_arr[6])
	plt.subplot(248)
	plt.imshow(img_arr[7])
	plt.show()

def calAccurate(file):
	ahash_res = open(file)
	count = 0
	img_arr = []
	# plt.subplot(141)
	for line in ahash_res.readlines():
		res_list = line.split(',')
		index = res_list[0].split('(')[1]
		cluster = res_list[1]
		template =  res_list[2]

		if cluster == template:
			# print line
			cluster_index = '/Users/wyf/Documents/crop_image8/'+str(int(cluster))+"_"+index+".jpg"
			count +=1
			if count<10:
				img_arr.append(cluster_index)
	draw(img_arr)
	print count
	return 1


if __name__ == '__main__':

	h5_path = '/Users/wyf/Desktop/anti_stat/crop_test.h5'
	cluster_path = '/Users/wyf/Desktop/anti_stat/200_sed_res.dat'
	template_path = '/Users/wyf/Desktop/anti_stat/200_template.h5'
	ahash_path = '/Users/wyf/Desktop/anti_stat/dhash_res.dat'
	# findTemplate(cluster_path, template_path, h5_path, ahash_path, 1)
	calAccurate(ahash_path)



