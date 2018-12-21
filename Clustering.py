from numpy import *
from itertools import combinations
from scipy.spatial.distance import pdist


class ClusterNode(object):
    def __init__(self,vec,left,right,distance=0.0,count=1):
        self.left = left
        self.right = right
        self.vec = vec
        self.distance = distance
        self.count = count # only used for weighted average
        # self.filename = filename

    def extract_clusters(self,dist):
        """ Extract list of sub-tree clusters from 
            hcluster tree with distance<dist. """
        if self.distance < dist:
            return [self]
        return self.left.extract_clusters(dist) + self.right.extract_clusters(dist)

    def get_cluster_elements(self):
        """    Return ids for elements in a cluster sub-tree. """
        return self.left.get_cluster_elements() + self.right.get_cluster_elements()

    def get_height(self):
        """    Return the height of a node, 
            height is sum of each branch. """
        return self.left.get_height() + self.right.get_height()

    def get_depth(self):
        """    Return the depth of a node, depth is 
            max of each child plus own distance. """
        return max(self.left.get_depth(), self.right.get_depth()) + self.distance

    def draw(self,draw,x,y,s,imlist,im):
        """    Draw nodes recursively with image 
            thumbnails for leaf nodes. """
    
        h1 = int(self.left.get_height()*20 / 2)
        h2 = int(self.right.get_height()*20 /2)
        top = y-(h1+h2)
        bottom = y+(h1+h2)
        
        # vertical line to children    
        draw.line((x,top+h1,x,bottom-h2),fill=(0,0,0))    
        
        # horizontal lines 
        ll = self.distance*s #line length
        draw.line((x,top+h1,x+ll,top+h1),fill=(0,0,0))    
        draw.line((x,bottom-h2,x+ll,bottom-h2),fill=(0,0,0))        
        
        # draw left and right child nodes recursively    
        self.left.draw(draw,x+ll,top+h1,s,imlist,im)
        self.right.draw(draw,x+ll,bottom-h2,s,imlist,im)
    

class ClusterLeafNode(object):
    def __init__(self,vec,id):
        self.vec = vec
        self.id = id

    def extract_clusters(self,dist):
        return [self] 

    def get_cluster_elements(self):
        return [self.id]

    def get_height(self):
        return 1

    def get_depth(self):
        return 0
    
    def draw(self,draw,x,y,s,imlist,im):
        # nodeim = Image.open(imlist[self.id])
        # print 'self.id',self.id
        nodeim = imlist[self.id]
        nodeim.thumbnail([20,20])
        ns = nodeim.size
        im.paste(nodeim,[int(x),int(y-ns[1]//2),int(x+ns[0]),int(y+ns[1]-ns[1]//2)])


def L2dist(v1,v2):
    return sqrt(sum((v1-v2)**2))

    
def L1dist(v1,v2):
    return sum(abs(v1-v2))

def VectorCosine(x,y):
    xmean = sum(x)/12
    ymean = sum(y)/12    
    x = [i - xmean for i in x]
    vector_a = mat(x) 
    y = [i - ymean for i in y]
    vector_b = mat(y)
    num = float(vector_a * vector_b.T)
    denom = linalg.norm(vector_a) * linalg.norm(vector_b)
    cos = num / denom
    # print cos
    # sim = 0.5 + 0.5 * cos
    return cos

def Mahalanobis(vec1, vec2):
    npvec1, npvec2 = array(vec1), array(vec2)
    npvec = array([npvec1, npvec2])
    sub = npvec.T[0]-npvec.T[1]
    inv_sub = linalg.inv(cov(npvec1, npvec2))
    return sqrt(dot(inv_sub, sub).dot(sub.T))


def StandardEuclidean(vec1, vec2):
    X = vstack([vec1, vec2])
    # dist = pdist(X,'seuclidean')
    # sd_mat = var(X, axis=0, ddof=1) / sd_mat
    # print (vec1 - vec2) ** 2 , sd_mat
    dist = sqrt(((vec1/vec1[0] - vec2/vec2[0]) ** 2).sum())
    # print dist
    return dist

def pearson_cc(x,y):
    xlength = len(x)
    ylength = len(y)
    xmean = sum(x)/xlength
    ymean = sum(y)/ylength
    # print xmean
    Sum_xy = 0
    Sx = 0
    Sy = 0
    for i in range(xlength):
        # print x[i]
        Sum_xy += (x[i]-xmean)*(y[i]-ymean)
    covariance = Sum_xy/(xlength-1)

    for i in range(xlength):
        Sx += (x[i]-xmean)*(x[i]-xmean)
    stddx = pow(Sx/(xlength-1), 0.5)

    for i in range(ylength):
        Sy += (y[i]-xmean)*(y[i]-ymean)
    stddy = pow(Sy/(ylength-1), 0.5)
    corr_xy = covariance/(stddx*stddy)
    return corr_xy

def hcluster(cluster_num, features, distfcn=StandardEuclidean):
    """ Cluster the rows of features using 
        hierarchical clustering. """
    
    # cache of distance calculations
    distances = {}
    # initialize with each row as a cluster 
    node = [ClusterLeafNode(array(f),id=i) for i,f in enumerate(features)]
    count = 0
    total_items = len(features)
    while ((len(node)>1) and (count < total_items - int(cluster_num))):
        # print "combination times:", count
        # closest = float(-1)
        closest = float('Inf')
        
        # loop through every pair looking for the smallest distance
        for ni,nj in combinations(node,2):
            if (ni,nj) not in distances: #calculate every pairs distance
                distances[ni,nj] = distfcn(ni.vec,nj.vec)

            d = distances[ni,nj]
            if d<closest:
                closest = d 
                lowestpair = (ni,nj) 
            # d = distances[ni,nj]
            # if d>closest:
            #     closest = d 
            #     lowestpair = (ni,nj) 
        print "-----", closest
        ni,nj = lowestpair#find a closest pair 
        # average the two clusters
        new_vec = (ni.vec + nj.vec) / 2.0
        count += 1
        
        # create new node
        new_node = ClusterNode(new_vec,left=ni,right=nj,distance=closest)
        node.remove(ni)
        node.remove(nj)
        node.append(new_node) #new node push into node list
    return node


from PIL import Image,ImageDraw
 
def draw_dendrogram(node,imlist,filename='clusters.jpg'):
    """    Draw a cluster dendrogram and save to a file. """
    
    # height and width
    rows = node.get_height()*20
    cols = 300
    
    # scale factor for distances to fit image width
    if node.get_depth()!=0:
      s = float(cols-100)/node.get_depth()
    else:
      s=0
    
    # create image and draw object
    im = Image.new('RGB',(cols,rows),(255,255,255))
    draw = ImageDraw.Draw(im)
    
    # initial line for start of tree
    draw.line((0,rows/2,20,rows/2),fill=(0,0,0))    
    
    # draw the nodes recursively
    node.draw(draw,20,(rows/2),s,imlist,im)
    im.save(filename)
    im.show()