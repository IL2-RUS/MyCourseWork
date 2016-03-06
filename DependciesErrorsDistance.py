import random, math, pylab, numpy
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC

list_err = list()
list_dist = list()

for i in range(100):
    print(str(i) + '%')
#Generate data:
    x1 = list()
    y1 = list()
    x2 = list()
    y2 = list()
    data = list()
    feature = list()

    for j in range(0, 100):
        x1.append(random.normalvariate(0, 1))
        y1.append(random.normalvariate(0, 1))
        x2.append(random.normalvariate(float(i / 20), 1))
        y2.append(random.normalvariate(float(i / 20), 1))

        data.append((x1[-1], y1[-1]))
        data.append((x2[-1], y2[-1]))
        feature.append(1)
        feature.append(-1)

    fl = open('samples_.txt', 'a')
    fl.write('Sample: ' + str(i) + '\n')
    for j in range(0, 100):
        fl.write(str(x1[j]) + ' ' + str(y1[j]) + '\n')
        fl.write(str(x2[j]) + ' ' + str(y2[j]) + '\n')
    fl.write('\n')
    fl.close()

#Training and preparing:
    svm = LinearSVC(C = 1)
    f = svm.fit(data, feature)

    def SepLine(x):
        return (-1) * (svm.coef_[0][0] * x + svm.intercept_[0])

    x = numpy.linspace(-3, i / 20 + 3, 100)
    y = SepLine(x) / svm.coef_[0][1]

#The Number of errors:
    labels_after_train = svm.predict(data)
    num_err = 0
    x_err = list()
    y_err = list()
    fl = open('vec_err.txt', 'a')
    fl.write('Sample: ' + str(i) + '\n')
    for j in range(len(data)):
        if labels_after_train[j] != feature[j]:
            num_err += 1
            x_err.append(data[j][0])
            y_err.append(data[j][1])
            fl.write(str(data[j][0]) + ' ' + str(data[j][1]) + '\n')

    fl.write('The number of Errors: ' +  str(num_err) + '\n')
    fl.close()

#Print
    plt.plot(x1, y1, 'g. ', x2, y2, 'b. ', x_err, y_err, 'r^ ', x, y)
    path = 'graphics/Example_' + str(i)
    print(path)
    plt.savefig(path, dpi = 300)
    plt.clf()

#For graphic of err:
    list_err.append(num_err)
    list_dist.append((i / 20) * 2 ** (0.5))
plt.plot(list_dist, list_err)
plt.savefig('Errors')
plt.clf()
