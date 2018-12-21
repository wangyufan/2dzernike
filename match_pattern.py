#coding:utf-8
import sys
reload(sys)
import os
import os.path
import argparse
import pickle
import numpy
import h5py


def get_new_res(h5_path, cluster_res, output):
  	h5_file = h5py.File(h5_path,'r')
  	cluster_ids = h5_file['cluster_ids'].value
	#save cluster result as a directory
	res = {}
	type_x = 0 
	label = []
	with open(cluster_res, 'r') as df:
		for line in [d.strip().split('[')[1].split(']')[0].split(',') for d in df]:
			type_x += 1
			for index in line:
				print index
				# index is the rank in cluster dataset, but we should test the result in total datadset
				true_id = cluster_ids[int(index)]
				res[true_id] = type_x
				label.append(type_x)
	output = open(output,'w')
	# print>>output, res
	print>>output, label
	output.close()

if __name__ == '__main__':

	# parser = argparse.ArgumentParser()
	# parser.add_argument("-output", help="output file paths, it must be end up with '/' ", type=str)
	# parser.add_argument("--select", action='append', dest='select_list', default=[], help='select the activity type, default all. -select Active -select Moderate')
	# parser.add_argument('-filepath', action='append', dest='path_list', default=[], help='Add cc file paths to a list, -filepath /home/123 -filepath /home/124')
	# args = parser.parse_args()
	# filepath_list = args.path_list
	# output = args.output
	# select_list = args.select_list
	h5_path = '/Users/wyf/Desktop/anti_stat/crop_test.h5'
	cluster_res = '/Users/wyf/Desktop/anti_stat/200_sed_res.dat'
	output = '/Users/wyf/Desktop/anti_stat/200_label.dat'
	get_new_res(h5_path, cluster_res, output)

