import sys
import matplotlib.pyplot as plt
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks
import os.path
import numpy as np
import h5py
import math

if __name__ == '__main__':
	args = sys.argv[1:]
	signal_perc = args[0]
	template_path = '/Users/wyf/Documents/test_doc/templates/112_cosine_templates.h5'
	template = h5py.File(template_path, 'r') 
	template_list = template['templates']
	intensity_list = []
	signal_num = math.floor(len(template_list[0].flatten()) * float(signal_perc))
	for template in template_list:
		sorted_data = sorted(template.flatten(), reverse = True)
		intensity = sum(sorted_data[:signal_num]) - sum(sorted_data[signal_num:])
		intensity_list.append(intensity)
	# print(intensity_list)
	output = '/Users/wyf/Documents/test_doc/templates/signal_'+ str(signal_perc) + '_intensity.npy'
	np.save(output, intensity_list)
	print(signal_num)
	b = np.load(output)
	print(b)

