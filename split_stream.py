from skimage import io
import sys
import math
import numpy as np
import random 
import time
import os

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
    for line in lines:
        linesplit = line.split()  #split on space
        if (len(linesplit) == 10):
            if (linesplit[0] == "h"):
            	flag_hkl = True
            	file_str += line
            	i = 0
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
        if (len(linesplit) == 3):      		
        	if (linesplit[0] == "End"):
        		flag_hkl = False
        if (len(linesplit) == 10 and flag_hkl):
            h = linesplit[0]
            k = linesplit[1]
            l = linesplit[2]
            intensity_hkl = linesplit[3]
            X_hkl = linesplit[7]
            Y_hkl = linesplit[8]
            new_intensity = change_intensity_v4(intensity_path, cxi_num, frame_num, i)
            print("======", cxi_num, frame_num, X_hkl, Y_hkl, intensity_hkl, new_intensity)
            replace_num+=1
            i+=1 
        file_str += line
        # print("write one line..")
    file.close()
    with open('/Users/wyf/Documents/simulation/new_asdf_0125.stream', 'w') as f:
    	f.writelines(file_str)
    return replace_num
