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
	template_file = h5py.File(template_path, 'r') 
	template_list = template_file['templates']
	signal_num = math.floor(len(template_list[0].flatten()) * float(signal_perc))
	mask_arr = []
	for template in template_list:
		sorted_data = sorted(template.flatten(), reverse = True)
		# intensity = sum(sorted_data[:signal_num]) - sum(sorted_data[signal_num:])
		threshold = sorted_data[signal_num]
		mask = template < threshold
		mask_arr.append(mask)
	return mask_arr

def get_mask_v2(signal_perc, bkg_perc, template_path):
	template_file = h5py.File(template_path, 'r') 
	template_list = template_file['templates']
	signal_num = math.floor(len(template_list[0].flatten()) * float(signal_perc))
	background_num = math.floor(len(template_list[0].flatten()) * float(bkg_perc))
	mask_arr = []
	for template in template_list:
		arr = template
		sorted_data = sorted(template.flatten(), reverse = True)
		threshold_b = sorted_data[225-background_num]
		mask_b = template <= threshold_b
		arr[mask_b] = 1
		threshold_s = sorted_data[signal_num]
		mask_s = template > threshold_s
		arr[mask_s] = 0
		mask_u = template >1
		arr[mask_u] = -1
		# print("threshold_b",threshold_b, "threshold_s", threshold_s)
		# print(arr)
		mask_arr.append(arr)
	return mask_arr

if __name__ == '__main__':
	args = sys.argv[1:]
	signal_perc = args[0]
	bkg_perc = args[1]
	template_dir = '/Users/wyf/Documents/now/templates/'
	files = os.listdir(template_dir)
	template_list = [os.path.join(template_dir, f) for f in files if f.endswith('correlation_templates.h5')]
	for template_path in template_list:
		template_type = os.path.basename(template_path).split('_')[1]
		mask_list = get_mask_v2(signal_perc, bkg_perc, template_path)
		arr = np.unique(mask_list, axis=0, return_counts=True)
		#print("unique template's 0-1 matrix: %d"%len(arr[1]))
		#print("the amount of every 0-1 matrix: ", arr[1])
		output = '/Users/wyf/Documents/now/templates/signal_'+str(signal_perc)+ '_' + str(bkg_perc) + '_' + str(template_type) + '_mask.npy'
		np.save(output, mask_list)
		mask_list = np.load(output)
		arr = np.unique(mask_list, axis=0, return_counts=True)
		print(template_type + " unique template's mask matrix: %d"%len(arr[1]))
		print("the amount of every mask matrix: \n", arr[1])
		print(arr[0].astype(np.int)[:20])

