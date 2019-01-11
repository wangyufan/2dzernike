from skimage import io
import sys
import h5py
import math
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
import random 


def ProcessCxi(f_input):
	data = []
	intensity_count = 0
	X_pos = f_input['peak_info/peakXPosRaw'].value
	Y_pos = f_input['peak_info/peakYPosRaw'].value
	intensity_list = f_input['sim_intensity'].value
	for index in range(50):
		pos = zip(X_pos[index], Y_pos[index]) 
		arr = []
		for (x, y) in pos:
			if x>0 or y>0:
				intensity = intensity_list[intensity_count]
				intensity_count +=1
				arr.append((x, y, intensity))
		data.append(arr)
	return data

def change_intensity(data, index_num, x, y, intensity_hkl):
	new_intensity = intensity_hkl
	for (item_x, item_y, item_i) in data[index_num - 1]:
		if (abs(float(x) - float(item_x)) < 0.9 and abs(float(y) - float(item_y)) < 0.9):
			new_intensity = round(item_i, 2)
			print("======", x, y, intensity_hkl, new_intensity)
	return new_intensity
	



def change_stream(data, filepath):
    file = open(filepath,'r')
    lines  =  file.readlines()
    xy_list = []
    hkl_list = []
    flag_xy = False
    flag_hkl = False
    file_str = ""
    index_num = 0  
    for line in lines:
        linesplit = line.split()  #split on space
        if (len(linesplit) == 10):
            if (linesplit[0] == "h"):
            	flag_hkl = True
            	file_str += line
            	continue #???
        if (len(linesplit) == 4):
        	if(linesplit[0] == "Image"):
        		index_num = int(linesplit[3])
        	if (linesplit[0] == "End"):
        		flag_hkl = False
        if (len(linesplit) == 10 and flag_hkl):
            h = linesplit[0]
            k = linesplit[1]
            l = linesplit[2]
            intensity_hkl = linesplit[3]
            X_hkl = linesplit[7]
            Y_hkl = linesplit[8]
            # print("-------",index_num, line)
            new_intensity = change_intensity(data, index_num, X_hkl, Y_hkl, intensity_hkl)
            line = line.replace(str(intensity_hkl), str(new_intensity)) 
        file_str += line
    with open('/Users/wyf/Documents/simulation/new.stream', 'w') as f:
    	f.writelines(file_str)

if __name__ == "__main__":
	# arg = sys.argv[1]
	cxi_path = '/Users/wyf/Documents/SFX/keke/cxi_hit/r0003/hit100/r0003-rank1-job0.cxi'
	f_input = h5py.File(cxi_path, 'r')
	filepath = '/Users/wyf/Documents/simulation/intensity_asdf.stream'
	# filepath = '/Users/wyf/Documents/simulation/test.stream'
	#save total data
	data = ProcessCxi(f_input)
	change_stream(data, filepath)
	f_input.close()
