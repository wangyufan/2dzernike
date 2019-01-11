import sys
import matplotlib.pyplot as plt
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks
import os.path
import numpy as np
import h5py
import math
import itertools

def get_mask(signal_perc, template_path):
	template = h5py.File(template_path, 'r') 
	template_list = template['templates']
	signal_num = math.floor(len(template_list[0].flatten()) * float(signal_perc))
	mask_arr = []
	for template in template_list:
		sorted_data = sorted(template.flatten(), reverse = True)
		# intensity = sum(sorted_data[:signal_num]) - sum(sorted_data[signal_num:])
		threshold = sorted_data[signal_num]
		mask = template < threshold
		mask_arr.append(mask)
	return mask_arr

if __name__ == '__main__':
	args = sys.argv[1:]
	signal_perc = args[0]
	template_path = '/Users/wyf/Documents/100f_result/templates/100_braycurtis_templates.h5'
	template_type = os.path.basename(template_path).split('_')[1]
	mask_list = get_mask(signal_perc, template_path)
	# arr = []
	# count=0
	# for i in range(len(mask_list)-1):
	# 	if((mask_list[i] == mask_list[i+1]).all()):
	# 		count+=1
	# 	else:
	# 		arr.append(mask_list[i].all())
	arr = np.unique(mask_list, axis=0, return_counts=True)
	# print(arr[0])
	print("unique template's 0-1 matrix: %d"%len(arr[1]))
	print("the amount of every 0-1 matrix: ", arr[1])
	output = '/Users/wyf/Documents/100f_result/templates/signal_'+ str(signal_perc)+ '_' + str(template_type) + '_mask.npy'
	np.save(output, mask_list)
	# b = np.load(output)
	# print(b)

