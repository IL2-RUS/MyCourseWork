import random, math, pylab, numpy
#import numpy as np
from sklearn.svm import LinearSVC

#Generate data:
'''
x1 = list()
y1 = list()
x2 = list()
y2 = list()
data = list()
feature = list()

for i in range(0, 100):
    x1.append(random.normalvariate(0, 1))
    y1.append(random.normalvariate(0, 1))
    x2.append(random.normalvariate(1, 1))
    y2.append(random.normalvariate(1, 1))

    data.append((x1[-1], y1[-1]))
    data.append((x2[-1], y2[-1]))
    feature.append(1)
    feature.append(-1)

fl = open('sample.txt', 'w')
for i in range(0, 100):
    fl.write(str(x1[i]) + ' ' + str(y1[i]) + '\n')
    fl.write(str(x2[i]) + ' ' + str(y2[i]) + '\n')
fl.close()
'''
#Read data from sample.txt:
data = list()
x1 = list()
y1 = list()
x2 = list()
y2 = list()
feature = list()
fl = open('sample.txt', 'r')
counter = 0

for line in fl:
    d = line.split()
    data.append([float(d[0]), float(d[1])])
    if counter % 2 == 0:
        feature.append(-1)
        x1.append(float(d[0]))
        y1.append(float(d[1]))
    else:
        feature.append(1)
        x2.append(float(d[0]))
        y2.append(float(d[1]))
    counter += 1
    

#Training and preparing:
svm = LinearSVC(C = 100)
f = svm.fit(data, feature)
data_feat = list()

def SepLine(x):
    return (-1) * (svm.coef_[0][0] * x + svm.intercept_[0])
x = numpy.linspace(-3, 3, 100)
y = SepLine(x) / svm.coef_[0][1]

#The Number of errors:
labels_after_train = svm.predict(data)
num_err = 0
x_err = list()
y_err = list()
for i in range(len(data)):
    if labels_after_train[i] != feature[i]:
        num_err += 1
        x_err.append(data[i][0])
        y_err.append(data[i][1])

print('The number of Errors: ', num_err)

#Print
print(svm.coef_)
print(svm.intercept_)
pylab.plot(x1, y1, 'g. ', x2, y2, 'b. ', x_err, y_err, 'r^ ', x, y)
pylab.show()
