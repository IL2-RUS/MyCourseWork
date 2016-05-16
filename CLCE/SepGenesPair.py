import math, numpy
from sklearn.svm import LinearSVC
import matplotlib.pyplot as plt

def getnumgen(flname):
    fl = open(flname, 'r')
    numgen = []
    for line in fl:
        if not line == '\n':
            attr = line.split(',')
            info = attr[0].split(' ')
            numgen.append(int(info[4]))
    return numgen

def getdatanumgen(flname, numgen):
    fl = open(flname, 'r')
    data = []
    it = 0
    counter = 0
    for line in fl:
        if it < len(numgen) and counter == numgen[it]:
            data_line = line.split(',')[1:]
            for i in range(len(data_line)):
                data_line[i] = float(data_line[i])
            data.append(data_line)
            it += 1
        counter += 1
    if not len(data) == len(numgen):
        print('Error in getdatanumgen !')
    return data

def LearnAndErr(data_learn, features, data_1, data_2):
    svm = LinearSVC(C = 1)
    svm.fit(data_learn, features)
    
    num_err = 0
    predict = svm.predict(data_learn)
    for i in range(len(predict)):
        if not predict[i] == features[i]:
            num_err += 1
    return num_err

def SepGen(numgen, data_1, data_2):
    print('Find pairs of separated genes...')
    Sep_gens = []
    errors = []
    for i in range(len(numgen)):
        for k in range(len(numgen)):
            data_learn = []
            features = []
            for j in range(len(data_1[0])):
                for l in range(len(data_1[0])):
                    data_learn.append([data_1[i][j], data_1[k][l]])
                    features.append(1)
            for h in range(len(data_2[0])):
                for g in range(len(data_2[0])):
                    data_learn.append([data_2[i][h], data_2[k][g]])
                    features.append(-1)
            err = LearnAndErr(data_learn, features, data_1, data_2)
            if err == 0:
                Sep_gens.append([numgen[i], numgen[k]])
            errors.append([numgen[i], numgen[k], err])
        print(i)
    return (Sep_gens, errors)

def main():
    flnumgen = 'Separated_Genes'
    numgen = getnumgen(flnumgen)
    numgen.sort()
    
    fldata_1 = 'small_cell_lung_data.csv'
    data_1 = getdatanumgen(fldata_1, numgen)

    fldata_2 = 'other_cell_lung_data.csv'
    data_2 = getdatanumgen(fldata_2, numgen)

    genes_and_err = SepGen(numgen, data_1, data_2)
    if not len(genes_and_err[0]) == 0:
        fl = open('SepGenesPair.log', 'w')
        for i in genes_and_err[0]:
            fl.write(str(i[0]) + ',' + str(i[1]) + '\n')
            print(str(i[0]) + ',' + str(i[1]) + '\n')
    else:
        print('There are not separated pair of genes :(\n')

main()
