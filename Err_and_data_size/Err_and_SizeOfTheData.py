import random, math, pylab, numpy, xlrd, xlwt, os
from sklearn.svm import LinearSVC

def GenerateDataOne(list_x, list_y, size, x0 = 0, y0 = 0, scatter = 1):
    for i in range(size):
        list_x.append(random.normalvariate(x0, scatter))
        list_y.append(random.normalvariate(y0, scatter))

def GenerateData(data, features, size, centre1, centre2, scatters):
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    if size % 2 == 0:
        GenerateDataOne(x1, y1, size // 2, centre1[0], centre1[1], scatters[0])
        GenerateDataOne(x2, y2, size // 2, centre2[0], centre2[1], scatters[1])

        for i in range(size // 2):
            data.append((x1[i], y1[i]))
            features.append(1)

            data.append((x2[i], y2[i]))
            features.append(-1)

    else:
        rand = random.randrange(0, 2, 1)
        GenerateDataOne(x1, y1, size // 2 + rand, centre1[0], centre1[1], scatters[0])
        GenerateDataOne(x2, y2, size // 2 + 1 - rand, centre2[0], centre2[1], scatters[1])

        for i in range(len(x1)):
            data.append((x1[i], y1[i]))
            features.append(1)
        
        for i in range(len(x2)):
            data.append((x2[i], y2[i]))
            features.append(-1)


def NumOfErr(svm, sample_data, sample_features):
    err = 0
    predicted_features = svm.predict(sample_data)
    for i in range(len(sample_data)):
        if sample_features[i] != predicted_features[i]:
            err += 1
    return err

def Average(ls):
    s = 0
    for i in ls:
        s += i
    return (s / len(ls))

def StDev(ls, av):
    st_dev = 0
    for i in range(len(ls)):
        st_dev += (av - ls[i]) ** 2
    st_dev /= len(ls)
    return math.sqrt(st_dev)

def LearningAndErrors(learning_data, learning_features, num_of_tests, sample_size):
#Learning
    svm = LinearSVC(C = 1)
    svm.fit(learning_data, learning_features)

#Errors
    errors = []
    for i in range(num_of_tests):
        sample_data = []
        sample_features = []
        sample_centres = [(0, 0), (0, 1)]
        sample_scatters = (1, 1)
        GenerateData(sample_data, sample_features, sample_size, sample_centres[0], sample_centres[1], sample_scatters)
        errors.append(NumOfErr(svm, sample_data, sample_features) / sample_size * 100)
    av_err = Average(errors)
    st_dev_err = StDev(errors, av_err)
    return (av_err, st_dev_err)


def Err_and_SizeOfTheData(beg_size = 3, end_size = 99, step = 2, num_of_tests = 100):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Errors')
    ws.write(0, 1, 'Learning Size: ')
    ws.write(1, 0, 'Sample Size: ')
    for learning_size in range(beg_size, end_size, step):
        for sample_size in range(beg_size, end_size, step):
            learning_data = []
            learning_features = []
            learning_centres = [(0, 0), (0, 1)]
            learning_scatters = (1, 1)
            GenerateData(learning_data, learning_features, learning_size, learning_centres[0], learning_centres[1], learning_scatters)
            res_err = LearningAndErrors(learning_data, learning_features, num_of_tests, sample_size)
        #Logging
            print ('Av = ' + str(res_err[0]) + ' St.Dev = ' + str(res_err[1]))
            if learning_size == beg_size:
                ws.write((sample_size // step + 1), 0, sample_size)
            ws.write((sample_size // step + 1), (learning_size // step + 1), 'Av = ' + str(res_err[0]) + ' St.Dev = ' + str(res_err[1]))
        ws.write(0, (learning_size // step + 1), learning_size)
    wb.save('Err&Size_Dist=' + str(math.sqrt(learning_centres[1][0] ** 2 + learning_centres[1][1] ** 2)) + '.xls')
    print('Ok')

Err_and_SizeOfTheData()