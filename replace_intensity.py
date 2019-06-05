from skimage import io
import sys
import h5py
import math
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
import random 
import time
import os

#########################################################version3.0########################################################
def Process_h5_v3(cxi_dir, f_input, intensity_list, range_x):
	t1 = time.time()
	arr = []
	# range_left = range_x
	# range_right = range_x + 1 #10.7 ~ 11.7 => 9,10,11,12
	total_peak_index = 0
	cxi_files = os.listdir(cxi_dir)
	cxi_list = [os.path.join(cxi_dir, f) for f in cxi_files if f.endswith('.cxi')]
	for cxi_path in cxi_list:
		cxi_id = int(os.path.basename(cxi_path).split('-')[2].split('.')[0].split('job')[1])
		print("======process cxi_id:", cxi_id)
		f_input = h5py.File(cxi_path, 'r')
		X_pos = f_input['entry_1/result_1/peakXPosRaw'].value
		Y_pos = f_input['entry_1/result_1/peakYPosRaw'].value
		for frame_index in range(100):
			print("======process frame_id:", frame_index)
			intensity_arr = np.zeros((1440 ,1440))
			pos = zip(X_pos[frame_index], Y_pos[frame_index])
			for (x, y) in pos:
				if x > 3 and y > 3:
					x = int(x)
					y = int(y)
					intensity_arr[x-range_x: x+range_x, y-range_x: y+range_x] = intensity_list[total_peak_index]
					total_peak_index += 1
			arr.append((cxi_id, frame_index, intensity_arr))
	t2 = time.time()
	print("generate  (cxi_id, frame_id, intensity_arr) time used:", (t2-t1))
	return arr	

def change_intensity_v3(data, cxi_num, frame_num, x, y, intensity_hkl):
	new_intensity = intensity_hkl
	filter_cxi_frame = list(filter(lambda elem: int(elem[0]) == cxi_num and int(elem[1]) == frame_num, data))
	intensity_list = [elem[2] for elem in filter_cxi_frame]
	intensity_arr = np.array(intensity_list[0])
	x = int(x.split('.')[0])
	y = int(y.split('.')[0])
	if int(intensity_arr[int(x)][int(y)]) != 0:
		new_intensity = round(intensity_arr[x][y], 2)
		print("======", cxi_num, frame_num, x, y, intensity_hkl, new_intensity)
	return new_intensity

def change_stream_v3(data, filepath):
    file = open(filepath,'r')
    lines  =  file.readlines()
    xy_list = []
    hkl_list = []
    flag_xy = False
    flag_hkl = False
    file_str = ""
    frame_num = 0
    replace_num = 0  
    for line in lines:
        linesplit = line.split()  #split on space
        if (len(linesplit) == 10):
            if (linesplit[0] == "h"):
            	flag_hkl = True
            	file_str += line
            	continue #??
        if (len(linesplit) == 3):
            if (linesplit[0] == "Image"):
            	# Image filename: /Users/wyf/Documents/SFX/keke/cxi_hit/r0004/hit5000/r0004-rank1-job0.cxi
            	cxi_num = int(linesplit[2].split('-')[2].split('.')[0].split('job')[1])
            	print("change cxi_num:", cxi_num)
        if (len(linesplit) == 2):
        	if(linesplit[0] == "Event:"):
        	# Event: //222
        		frame_num = int(linesplit[1].split('//')[1])
        		print("change frame_num:", frame_num)
        if (len(linesplit) == 4):      		
        	if (linesplit[0] == "End"):
        		flag_hkl = False
        if (len(linesplit) == 10 and flag_hkl):
            h = linesplit[0]
            k = linesplit[1]
            l = linesplit[2]
            intensity_hkl = linesplit[3]
            X_hkl = linesplit[7]
            Y_hkl = linesplit[8]
            new_intensity = change_intensity_v3(data, cxi_num, frame_num, X_hkl, Y_hkl, intensity_hkl)
            if (new_intensity!=intensity_hkl):
            	replace_num+=1
            line = line.replace(str(intensity_hkl), str(new_intensity)) 
        file_str += line
        # print("write one line..")
    with open('/Users/wyf/Documents/simulation/new_c_0.3_0121.stream', 'w') as f:
    	f.writelines(file_str)
    return replace_num


#########################################################version2.0########################################################
def Process_h5(f_input, intensity_list):
	t1 = time.time()
	total_size = len(intensity_list)
	intensity_count = 0
	X_pos = f_input['peak_x'].value
	Y_pos = f_input['peak_y'].value
	frame_id_arr = f_input['frame_id'].value
	cxi_id_arr = f_input['cxi_id'].value
	arr = []
	for index in range(total_size):
		cxi_id = cxi_id_arr[index]
		frame_id = frame_id_arr[index]
		x = X_pos[index] 
		y = Y_pos[index]
		intensity = intensity_list[index]
		arr.append((cxi_id, frame_id, x, y, intensity))
	t2 = time.time()
	print("Process_h5 time used:", (t2-t1))
	return arr

def change_intensity_v2(data, cxi_num, frame_num, x, y, intensity_hkl):
	new_intensity = intensity_hkl
	# for (item_cxi_id, item_frame_id, item_x, item_y, item_i) in filter_data:
	# 	if (int(item_cxi_id) == cxi_num) and (int(item_frame_id) == frame_num) and (abs(float(x) - float(item_x)) < 0.9 and abs(float(y) - float(item_y)) < 0.9):
			# new_intensity = round(item_i, 2)
	filter_cxi_frame = list(filter(lambda elem: int(elem[0]) == cxi_num and int(elem[1]) == frame_num, data))
	filter_xy = list(filter(lambda elem: (abs(float(elem[2]) - float(X_hkl)) < 0.9 and abs(float(elem[3]) - float(Y_hkl)) < 0.9), filter_cxi_frame))
	if filter_xy:	
		arr = data[0]
		new_intensity = round(arr[4], 2)
		print("======", cxi_num, frame_num, x, y, intensity_hkl, new_intensity)
	return new_intensity

def Process_h5_v2(f_input, intensity_list, range_x):
	t1 = time.time()
	total_size = len(intensity_list)
	X_pos = f_input['peak_x'].value
	Y_pos = f_input['peak_y'].value
	frame_id_arr = f_input['frame_id'].value
	cxi_id_arr = f_input['cxi_id'].value
	arr = []
	intensity_arr = np.array([])
	# for index in range(total_size):
	for cxi_id in cxi_id_arr:
		for frame_id in frame_id_arr:
			index = cxi_id*100 + frame_id
			cxi_id = cxi_id_arr[index]
			frame_id = frame_id_arr[index]
			x = int(X_pos[index])
			y = int(Y_pos[index])
			intensity_arr[x - range_x: x + range_x][y - range_x: y + range_x] = intensity_list[index]
			print(intensity_arr)
			arr.append((cxi_id, frame_id, intensity_arr))
	t2 = time.time()
	print("generate  (cxi_id, frame_id, intensity_arr) time used:", (t2-t1))
	return arr	

def change_stream_v2(data, filepath):
    file = open(filepath,'r')
    lines  =  file.readlines()
    xy_list = []
    hkl_list = []
    flag_xy = False
    flag_hkl = False
    file_str = ""
    frame_num = 0  
    for line in lines:
        linesplit = line.split()  #split on space
        if (len(linesplit) == 10):
            if (linesplit[0] == "h"):
            	flag_hkl = True
            	file_str += line
            	continue #??
        if (len(linesplit) == 3):
            if (linesplit[0] == "Image"):
            	# Image filename: /Users/wyf/Documents/SFX/keke/cxi_hit/r0004/hit5000/r0004-rank1-job0.cxi
            	cxi_num = int(linesplit[2].split('-')[2].split('.')[0].split('job')[1])
            	print("cxi_num:", cxi_num)
        if (len(linesplit) == 2):
        	if(linesplit[0] == "Event:"):
        	# Event: //222
        		frame_num = int(linesplit[1].split('//')[1])
        		print("frame_num:", frame_num)
        if (len(linesplit) == 4):      		
        	if (linesplit[0] == "End"):
        		flag_hkl = False
        if (len(linesplit) == 10 and flag_hkl):
            h = linesplit[0]
            k = linesplit[1]
            l = linesplit[2]
            intensity_hkl = linesplit[3]
            X_hkl = linesplit[7]
            Y_hkl = linesplit[8]
            new_intensity = change_intensity_v2(data, cxi_num, frame_num, X_hkl, Y_hkl, intensity_hkl)
            line = line.replace(str(intensity_hkl), str(new_intensity)) 
        file_str += line
        # print("write one line..")
    with open('/Users/wyf/Documents/simulation/new_asdf_5000.stream', 'w') as f:
    	f.writelines(file_str)

#########################################################version1.0########################################################
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
			# print("======", x, y, intensity_hkl, new_intensity)
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
            new_intensity = change_intensity(data, index_num, X_hkl, Y_hkl, intensity_hkl)
            line = line.replace(str(intensity_hkl), str(new_intensity)) 
        file_str += line
    with open('/Users/wyf/Documents/simulation/new.stream', 'w') as f:
    	f.writelines(file_str)
#########################################################version1.0########################################################
def change_intensity_v4(intensity_list, cxi_num, frame_num, i):
	#most time consuming
	filter_cxi_frame = list(filter(lambda elem: int(elem[0]) == cxi_num and int(elem[1]) == frame_num, intensity_list)) 
	intensity_list = [elem[2] for elem in filter_cxi_frame]
	new_intensity = intensity_list[i]
	return new_intensity

def change_stream_v4(intensity_path, stream_path):
    file = open(stream_path,'r')
    lines  =  file.readlines()
    xy_list = []
    hkl_list = []
    flag_xy = False
    flag_hkl = False
    file_str = ""
    frame_num = 0
    replace_num = 0  
    intensity_list = np.load(intensity_path)
    f_input = h5py.File('/Users/wyf/Documents/real_data/cxilr2816-r0211-c00.cxi', 'r')
    mask = f_input['entry_1/instrument_1/detector_1/detector_corrected/mask']
    # intensity_arr = np.load(intensity_path)
    # intensity_list = [elem[2] for elem in intensity_arr]

    with open('/Users/wyf/Documents/simulation/new_0.2_0.5_intensity_max.stream', 'w') as f:
	    for line in lines:
	        linesplit = line.split()  #split on space
	        if (len(linesplit) == 10):
	            if (linesplit[0] == "h"):
	            	flag_hkl = True
	            	file_str += line
	            	i = 0
	            	continue #??
	        # if (len(linesplit) == 3):
	        #     if (linesplit[0] == "Image"):
	            	# Image filename: /Users/wyf/Documents/SFX/keke/cxi_hit/r0004/hit5000/r0004-rank1-job0.cxi
	            	# cxi_num = int(linesplit[2].split('-')[2].split('.')[0].split('job')[1])
	            	# print("change cxi_num:", cxi_num)
	        if (len(linesplit) == 2):
	        	if(linesplit[0] == "Event:"):
	        	# Event: //222
	        		frame_num = int(linesplit[1].split('//')[1])
	        		# print("change frame_num:", frame_num)
	        if (len(linesplit) == 3):      		
	        	if (linesplit[0] == "End"):
	        		flag_hkl = False
	        		# f.append(frame_num)
	        if (len(linesplit) == 10 and flag_hkl):
	            h = linesplit[0]
	            k = linesplit[1]
	            l = linesplit[2]
	            intensity_hkl = linesplit[3]
	            # X_hkl = linesplit[7]
	            # Y_hkl = linesplit[8]
	            X_hkl = linesplit[8]
	            Y_hkl = linesplit[7]
	            x = int(float(X_hkl) + 0.5)
	            y = int(float(Y_hkl)+ 0.5)
	            # if x>4 and x<1475 and y>4 and y<1547:
		           #  mask_peak = mask[(y - 4): (y + 4), (x - 4): (x + 4)]
		           #  mask_peak_sum = mask_peak.sum()
		           #  if mask_peak_sum == 0:
			          #   intensity_value = intensity_list[replace_num]
			          #   new_intensity = float('%.2f' %intensity_value)
			          #   line = line.replace(str(intensity_hkl), str(new_intensity)) 
			          #   replace_num+=1
			          #   i+=1
########################################################## 
	            intensity_value = intensity_list[replace_num]
	            new_intensity = float('%.2f' %intensity_value)
	            line = line.replace(str(intensity_hkl), str(new_intensity)) 
	            replace_num+=1
	            i+=1 
			            # if(int(cxi_num)==0 and int(frame_num)==2):
			            #  intensity_value = change_intensity_v4(intensity_list2,cxi_num, frame_num, i)
			            # if(int(cxi_num)==0 and int(frame_num)==2):
			            #     print("======", cxi_num, frame_num, X_hkl, Y_hkl, intensity_hkl, new_intensity)
	        # file_str += line
	        # print("write one line..")
	        f.writelines(line)
    file.close()
    # with open('/Users/wyf/Documents/simulation/new_asdf_0125.stream', 'w') as f:
    	# f.writelines(file_str)
  #   for i in range(len(c)):
		# if(c[i-1] > c[i] and int(c[i])!= 0):
		# 	print(c[i-1], c[i],"====")
  #   return f
    return replace_num


def change_stream_v5(intensity_path, stream_path):
    file = open(stream_path,'r')
    lines  =  file.readlines()
    xy_list = []
    hkl_list = []
    flag_xy = False
    flag_hkl = False
    file_str = ""
    frame_num = 0
    cxi_num = 0
    replace_num = 0  
    count_no=0
    intensity_list = np.load(intensity_path)
    f_input = h5py.File('/Users/wyf/Documents/real_data/cxilr2816-r0211-c00.cxi', 'r')
    mask = f_input['entry_1/instrument_1/detector_1/detector_corrected/mask']
    # intensity_arr = np.load(intensity_path)
    # intensity_list = [elem[2] for elem in intensity_arr]

    with open('/Users/wyf/Documents/simulation/new_0.05_0.6_intensity.stream', 'w') as f:
	    for line in lines:
	        linesplit = line.split()  #split on space
	        if (len(linesplit) == 10):
	            if (linesplit[0] == "h"):
	            	flag_hkl = True
	            	file_str += line
	            	# i = 0
	            	continue #??
	        if (len(linesplit) == 2):
	        	if(linesplit[0] == "Event:"):
	        		frame_num = int(linesplit[1].split('//')[1])
	        if (len(linesplit) == 3):      		
	        	if (linesplit[0] == "End"):
	        		flag_hkl = False
	        	elif (linesplit[0] == "Image"):
	        		cxi_num = int(linesplit[2].split('-')[1].split('r0')[1])
	        if (len(linesplit) == 10 and flag_hkl):
	            h = linesplit[0]
	            k = linesplit[1]
	            l = linesplit[2]
	            intensity_hkl = linesplit[3]
	            X_hkl = linesplit[8]
	            Y_hkl = linesplit[7]
	            x = int(float(X_hkl) + 0.5)
	            y = int(float(Y_hkl)+ 0.5)
	            
	      #       if x>4 and x<1475 and y>4 and y<1547:
		     #        mask_peak = mask[(y - 4): (y + 4), (x - 4): (x + 4)]
		     #        mask_peak_sum = mask_peak.sum()
		     #        if mask_peak_sum == 0:
			    #         intensity_value = intensity_list[replace_num]
			    #         new_intensity = float('%.2f' %intensity_value)
			    #         line = line.replace(str(intensity_hkl), str(new_intensity)) 
			    #         # i+=1
			    # replace_num+=1


########################################################## 
	            intensity_value = intensity_list[replace_num]
	            new_intensity = float('%.2f' %intensity_value)
	            if int(intensity_value) == 0:
	            	print('======')
	            	new_intensity=intensity_hkl
	            	count_no+=1
	            # if (new_intensity==0.00):
	            # 	print(cxi_num,frame_num,x,y)
	            # 	new_intensity=intensity_hkl
	            # 	count_no+=1
	            line = line.replace(str(intensity_hkl), str(new_intensity)) 
	            replace_num+=1



	            # i+=1 
			            # if(int(cxi_num)==0 and int(frame_num)==2):
			            #  intensity_value = change_intensity_v4(intensity_list2,cxi_num, frame_num, i)
			            # if(int(cxi_num)==0 and int(frame_num)==2):
			            #     print("======", cxi_num, frame_num, X_hkl, Y_hkl, intensity_hkl, new_intensity)
	        # file_str += line
	        # print("write one line..")
	        f.writelines(line)
    file.close()
    # with open('/Users/wyf/Documents/simulation/new_asdf_0125.stream', 'w') as f:
    	# f.writelines(file_str)
  #   for i in range(len(c)):
		# if(c[i-1] > c[i] and int(c[i])!= 0):
		# 	print(c[i-1], c[i],"====")
  #   return f
    print(replace_num,count_no)
    return replace_num-count_no

#########################################################version4.0########################################################

if __name__ == "__main__":
	# arg = sys.argv[1]
	# cxi_path = '/Users/wyf/Documents/SFX/kekeke/cxi_hit/r0004/hit150/'
	# h5_path = '/Users/wyf/Documents/peaks_0121.h5'
	# f_input = h5py.File(h5_path, 'r')
	# # intensity_path = '/Users/wyf/Documents/100f_result/b_235_intensity.npy'
	# intensity_path = '/Users/wyf/Documents/100f_result/c_0.3_intensity.npy'

	# intensity_list = np.load(intensity_path)
	# filepath = '/Users/wyf/Documents/simulation/asdf_0125.stream'
	filepath = '/Users/wyf/Documents/simulation/intensity_457.stream'
	# filepath = '/Users/wyf/Documents/simulation/test.stream'
	# #save total data
	# range_x = 1
	# data = Process_h5_v3(cxi_path, f_input, intensity_list, range_x)
	t1 = time.time()

	# # intensity_path = '/Users/wyf/Documents/100f_result/3test_b_235_intensity.npy'
	# intensity_path2 = '/Users/wyf/Desktop/align_code/total_intensity_cc2.npy'
	
	# intensity_path = '/Users/wyf/Documents/100f_result/test_cc_145_intensity.npy'
	# intensity_path = '/Users/wyf/Documents/100f_result/0.2_intensity.npy'
	intensity_path = '/Users/wyf/Desktop/align_code/total_intensity_cc.npy'

	# intensity_path = '/Users/wyf/Desktop/20w_result/result/1_20w_b_235_intensity.npy'
	replace_num = change_stream_v5(intensity_path , filepath)
	# for i in range(len(replace_num)):
	# 	if(replace_num[i-1] > replace_num[i] and int(replace_num[i])!= 0):
	# 		print(replace_num[i-1], replace_num[i])
	# 		count+=1
	# print(count)
	t2 = time.time()
	print("replace time used:", (t2-t1))
	print("total replace_num:",replace_num)