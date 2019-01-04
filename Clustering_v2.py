from numpy import *
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import ward, fcluster
import h5py


def hcluster(features, x, type_flag):
	if type_flag == 'c':
		type_x = 'correlation'
	elif type_flag == 'm':
		type_x = 'mahalanobis'
	elif type_flag == 's':
		type_x = 'seuclidean'
	elif type_flag == 'cos':
		type_x = 'cosine'
	elif type_flag == 'b':
		type_x = 'braycurtis'
	else:
		 type_x = 'euclidean'

	Z = ward(pdist(features, type_x))
	# print Z
	data = fcluster(Z, t=x, criterion='distance')
	print len(data)
	# save('/Users/wyf/Desktop/aaa.npy',data)
	path = '/Users/wyf/Documents/test_doc/40cluster_res/'+type_x+'_cluster_res.h5'
	output = h5py.File(path, 'w')
	output.create_dataset('data', data = data)
	h5_file = h5py.File(path,'r')
  	cluster = h5_file['data'].value
  	cluster_unique = unique(cluster)
  	cluster_num = len(cluster_unique)
  	print("there are %d clusters." %cluster_num)
	print(cluster)
	return data