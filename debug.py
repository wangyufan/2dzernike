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




def find_bug(filepath):
	file = open(filepath,'r')
	lines  =  file.readlines()
	xy_list = []
	hkl_list = []
	flag_xy = False
	flag_hkl = False
	file_str = ""
	index_num = 0  
	hc =0
	end=0
	c=0
	for i in range(len(lines)):
		c+=1
		line=lines[i]
		linesplit = line.split()#split on space
		if (len(linesplit) == 3 and linesplit[0] == "---" and linesplit[1] == "Begin"):
			line_pre = lines[i-1]
			line_pre_split = line_pre.split()
			if(len(line_pre_split) == 3 ):
				print(line_pre,"---==-",c)
#########################################################version1.0########################################################



#########################################################version4.0########################################################

if __name__ == "__main__":

	filepath = '/Users/wyf/Documents/simulation/intensity_145.stream'
	find_bug(filepath)

