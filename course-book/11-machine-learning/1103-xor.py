# 1103.py
import cv2
import numpy as np
import matplotlib.pyplot as plt

#1
ann = cv2.ml.ANN_MLP_create()
ann.setLayerSizes(np.array([2,2,1]))
#ann.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)
ann.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM)
ann.setTermCriteria((cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 1000, 1e-5))

#2
X = np.array([[0,0],[0,1],[1,0],[1,1]], dtype = np.float32)
y = np.array([0,1,1,0], dtype = np.float32) # XOR
target = y.copy()

#3
#ret = ann.train(samples = X, layout = cv2.ml.ROW_SAMPLE, responses = y)
trainData = cv2.ml.TrainData_create(samples = X, layout = cv2.ml.ROW_SAMPLE, responses = y)
ret = ann.train(trainData)

#4
ann.save('../data/ann-xor.res')

#5
h = 0.01
xMin, xMax = X[:,0].min() - h, X[:,0].max() + h
yMin, yMax = X[:,1].min() - h, X[:,1].max() + h

xx, yy = np.meshgrid(np.arange(xMin,xMax,h), np.arange(yMin,yMax,h))

sample = np.c_[xx.ravel(), yy.ravel()]
ret, Z = ann.predict(sample)
Z = np.round(Z)
Z = Z.reshape(xx.shape)

fig = plt.gcf()
fig.set_size_inches(5,5)

plt.contour(xx,yy,Z,cmap = plt.cm.gray)
plt.contour(xx,yy,Z,colors = 'red', linewidths = 3)
plt.scatter(*X[:,:].T, c = target.flatten(), s = 75)
plt.show()