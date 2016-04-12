import random, math, pylab, numpy
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC

list_err = list()
list_dist = list()

def GenerateData(i, x1, y1, x2, y2, data, feature, path_to_save):
    for j in range(0, 10):
        x1.append(random.normalvariate(0, 1))
        y1.append(random.normalvariate(0, 1))
        x2.append(random.normalvariate(float(i / 20), 1))
        y2.append(random.normalvariate(float(i / 20), 1))

        data.append((x1[-1], y1[-1]))
        data.append((x2[-1], y2[-1]))
        feature.append(1)
        feature.append(-1)
    
    fl = open(path_to_save, 'a')
    fl.write("Sample: {0}\n".format(str(i)))
    for j in range(0, 10):
        fl.write(str(x1[j]) + ' ' + str(y1[j]) + '\n')
        fl.write(str(x2[j]) + ' ' + str(y2[j]) + '\n')
    fl.write('\n')
    fl.close()    

def NumErr(i, svm, num_it, path_to_save_vec, ifprint=False, ifgenerate=False, _data = [], _feature = [], x = [], y = []):
    av_num_err = 0
    for it in range(num_it):
        if ifgenerate:
#Generate new data:
            print("Generate the data for test#{0}".format(str(it)))
            _x1 = list()
            _y1 = list()
            _x2 = list()
            _y2 = list()
            _data = list()
            _feature = list()
            GenerateData(i, _x1, _y1, _x2, _y2, _data, _feature, 'samples_new.txt')
#The Number of errors:
        labels_after_train = svm.predict(_data)
        num_err = 0
        x_err = list()
        y_err = list()
        fl = open(path_to_save_vec, 'a')
        fl.write('Sample: ' + str(i) + '.' + str(it) + '\n')

        for j in range(len(_data)):
            if labels_after_train[j] != _feature[j]:
                num_err += 1
                x_err.append(_data[j][0])
                y_err.append(_data[j][1])
                fl.write(str(_data[j][0]) + ' ' + str(_data[j][1]) + '\n')

        fl.write('The number of Errors: ' +  str(num_err) + '\n')
        fl.close()
        av_num_err += num_err
        if ifprint:
        #Print
            plt.plot(_x1, _y1, 'g. ', _x2, _y2, 'b. ', x_err, y_err, 'r^ ', x, y)
            path = 'graphics/Example_' + str(i) + '_' + str(it)
            print(path)
            plt.savefig(path, dpi = 300)
            plt.clf()
    av_num_err /= num_it
    proc_of_err = av_num_err / 2

    fl = open(path_to_save_vec, 'a')
    fl.write('Average: ' + str(av_num_err) + '\n')
    fl.write('Proc of Av: ' + str(proc_of_err) + '\n')
    fl.close()
    return proc_of_err



list_err_data_1 = []
list_err_data_av = []
list_err_other_data = []
list_dist = []

for i in range(10):
    print(str(i) + '%')
    repeat = 7
    for it in range(repeat):
#Generate data:
        x1 = list()
        y1 = list()
        x2 = list()
        y2 = list()
        data = list()
        feature = list()
        GenerateData(i, x1, y1, x2, y2, data, feature, 'samples_.txt')

#Training and preparing:
        svm = LinearSVC(C = 1)
        f = svm.fit(data, feature)

        def SepLine(x):
            return (-1) * (svm.coef_[0][0] * x + svm.intercept_[0])

        x = numpy.linspace(-3, i / 20 + 3, 100)
        y = SepLine(x) / svm.coef_[0][1]

#Erorrs for the same data_1 and average
        if it == 0:
            proc_of_err_same_data_1 = NumErr(i, svm, 1, path_to_save_vec = "vec_err_same", _data = data, _feature = feature)
            proc_of_err_same_data_av = proc_of_err_same_data_1
            proc_of_err_other_data = NumErr(i, svm, 7, path_to_save_vec = "vec_err_other", ifgenerate = True)
        else:
            proc_of_err_same_data_av += NumErr(i, svm, 1, path_to_save_vec = "vec_err_same", _data = data, _feature = feature)
    proc_of_err_same_data_av /= repeat

#For graphic of err:
    list_err_data_1.append(proc_of_err_same_data_1)
    list_err_data_av.append(proc_of_err_same_data_av)
    list_err_other_data.append(proc_of_err_other_data)
    list_dist.append((i / 20) * 2 ** (0.5))

plt.plot(list_dist, list_err_data_1, label = u'Not averaged sample')
plt.plot(list_dist, list_err_data_av, label = u'Averaged sample')
plt.plot(list_dist, list_err_other_data, label = u'Averaged sample for generated data')

plt.grid(True)
plt.xlabel(u'Dist')
plt.ylabel(u'Err, %')
plt.legend()
plt.savefig('Errors')
plt.clf()
