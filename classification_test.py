import random
import numpy as np
import matplotlib.pyplot as plt
import h5py


h5_path = '/Users/wyf/Desktop/anti_stat/crop_test.h5'
h5_file = h5py.File(h5_path,'r')
label_file = open("/Users/wyf/Desktop/anti_stat/200_label.dat",'r')
X_train = h5_file['cluster_data'].value
y_train = label_file.readlines()
X_test = h5_file['cluster_data'].value

class KNearestNeighbor(object):
  """ a kNN classifier with L2 distance """

  def __init__(self):
    pass

  def train(self, X, y):
    self.X_train = X
    self.y_train = y
    
  def predict(self, X, k=1, num_loops=0):
    dists = self.compute_distances(X)
    return self.predict_labels(dists, k=k)

  def compute_distances(self, X):
    num_test = X.shape[0]
    num_train = self.X_train.shape[0]
    dists = np.zeros((num_test, num_train)) 
    X_sq = np.square(X).sum(axis=1)
    X_train_sq = np.square(self.X_train).sum(axis=1)
    dists = np.sqrt(-2*np.dot(X, self.X_train.T) + X_train_sq + np.matrix(X_sq).T)
    dists = np.array(dists)
    return dists

  def predict_labels(self, dists, k):
    num_test = dists.shape[0]
    y_pred = np.zeros(num_test)
    print  dists
    for i in range(num_test):
      closest_y = []
      candidate = np.argsort(dists[i,:])[:k]
      print "nearest index: ", candidate
      for i in candidate:
        # print self.y_train
        closest_y.append(self.y_train[i])
      y_pred[i] = np.argmax(np.bincount(closest_y))
    return y_pred

# This is a bit of magic to make matplotlib figures appear inline in the notebook
# rather than in a new window.
# plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
# plt.rcParams['image.interpolation'] = 'nearest'
# plt.rcParams['image.cmap'] = 'gray'


# As a sanity check, we print out the size of the training and test data.
# print('Training data shape: ', X_train.shape)
# print('Training labels shape: ', y_train.shape)
# print('Test data shape: ', X_test.shape)
# print('Test labels shape: ', y_test.shape)

# show some image in every type
# classes = range(1,101)
# num_classes = len(classes)
# samples_per_class = 7
# for y, cls in enumerate(classes):
#     print y, cls,y_train
#     idxs = np.flatnonzero(y_train == y)
#     idxs = np.random.choice(idxs, samples_per_class, replace=False)
#     for i, idx in enumerate(idxs):
#         plt_idx = i * num_classes + y + 1
#         plt.subplot(samples_per_class, num_classes, plt_idx)
#         plt.imshow(X_train[idx].astype('uint8'))
#         plt.axis('off')
#         if i == 0:
#             plt.title(cls)
# plt.show()

# cut data to improve speed
num_training = 500
mask = range(num_training)
X_train = X_train[mask]
y_train = y_train[1:500]

num_test = 50
mask = range(num_test)
X_test = X_test[mask]
y_test = y_train[501:550]

# reshape
X_train = np.reshape(X_train, (X_train.shape[0], -1))
X_test = np.reshape(X_test, (X_test.shape[0], -1))

print(X_train.shape)
print(X_test.shape)

classifier = KNearestNeighbor()
classifier.train(X_train, y_train)

dists = classifier.compute_distances(X_test)
# print(y_train)

# plt.imshow(dists, interpolation='none')
# plt.show()

# Now implement the function predict_labels and run the code below:
# y_test_pred = classifier.predict_labels(dists, k=1)

# # Compute and print the fraction of correctly predicted examples
# num_correct = np.sum(y_test_pred == y_test)
# accuracy = float(num_correct) / num_test
# print('Got %d / %d correct => accuracy: %f' % (num_correct, num_test, accuracy))

y_test_pred = classifier.predict_labels(dists, k=5)
num_correct = np.sum(y_test_pred == y_test)
accuracy = float(num_correct) / num_test
print('Got %d / %d correct => accuracy: %f' % (num_correct, num_test, accuracy))


# fold
num_folds = 5
k_choices = [1, 3, 5, 8, 10, 12, 15, 20, 50, 100]

X_train_folds = []
y_train_folds = []

X_train_folds = np.array_split(X_train, num_folds);
y_train_folds = np.array_split(y_train, num_folds)

k_to_accuracies = {}


for k in k_choices:
    k_to_accuracies[k] = []

for k in k_choices:#find the best k-value
    for i in range(num_folds):
        X_train_cv = np.vstack(X_train_folds[:i]+X_train_folds[i+1:])
        X_test_cv = X_train_folds[i]

        y_train_cv = np.hstack(y_train_folds[:i]+y_train_folds[i+1:])  #size:4000
        y_test_cv = y_train_folds[i]

        classifier.train(X_train_cv, y_train_cv)
        dists_cv = classifier.compute_distances_no_loops(X_test_cv)

        y_test_pred = classifier.predict_labels(dists_cv, k)
        num_correct = np.sum(y_test_pred == y_test_cv)
        accuracy = float(num_correct) / y_test_cv.shape[0]

        k_to_accuracies[k].append(accuracy)


# Print out the computed accuracies
for k in sorted(k_to_accuracies):
    for accuracy in k_to_accuracies[k]:
        print('k = %d, accuracy = %f' % (k, accuracy))



# plot the raw observations
for k in k_choices:
  accuracies = k_to_accuracies[k]
  plt.scatter([k] * len(accuracies), accuracies)

# plot the trend line with error bars that correspond to standard deviation
accuracies_mean = np.array([np.mean(v) for k,v in sorted(k_to_accuracies.items())])
accuracies_std = np.array([np.std(v) for k,v in sorted(k_to_accuracies.items())])
plt.errorbar(k_choices, accuracies_mean, yerr=accuracies_std)
plt.title('Cross-validation on k')
plt.xlabel('k')
plt.ylabel('Cross-validation accuracy')
plt.show()

