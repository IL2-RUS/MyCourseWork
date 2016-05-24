import math, numpy, pylab
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

def SepLine(x, svm):
    return ((-1) * (svm.coef_[0][0] * x + svm.intercept_[0]) / svm.coef_[0][1])

def Graphics(data_learn, features, svm, num_g1, num_g2):
    x1 = []
    y1 = []

    x2 = []
    y2 = []

    x = numpy.linspace(0, 15, 400)
    y = SepLine(x, svm)

    for i in range(len(features)):
        if features[i] == 1:
            x1.append(data_learn[i][0])
            y1.append(data_learn[i][1])
        else:
            x2.append(data_learn[i][0])
            y2.append(data_learn[i][1])

    plt.plot(x1, y1, 'g. ', x2, y2, 'b. ', x, y)
    plt.savefig('images/NumSamp: {}, {}'.format(num_g1, num_g2))
    plt.cla()

def LearnAndErr(data_learn, features, num_g1, num_g2):
    svm = LinearSVC(C = 1)
    svm.fit(data_learn, features)
    
    Graphics(data_learn, features, svm, num_g1, num_g2)

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

    for num_g1 in range(len(numgen)):
        for num_g2 in range(num_g1, len(numgen)):
            data_learn = []
            features = []

            for num_samp in range(len(data_1[0])):
                data_learn.append((data_1[num_g1][num_samp], data_1[num_g2][num_samp]))
                features.append(1)

            for num_samp in range(len(data_2[0])):
                data_learn.append((data_2[num_g1][num_samp], data_2[num_g2][num_samp]))
                features.append(-1)

            err = LearnAndErr(data_learn, features, num_g1, num_g2)
            errors.append((num_g1, num_g2, err))
            if err == 0:
                Sep_gens.append(num_g1, num_g2)
        print('Complete: {}%'.format(num_g1))

    return (Sep_gens, errors)

def main():
    flnumgen = 'Separated_Genes'
    numgen = getnumgen(flnumgen)
    numgen.sort()
    print ("len numgen = " + str(len(numgen)))   
 
    fldata_1 = 'small_cell_lung_data.csv'
    data_1 = getdatanumgen(fldata_1, numgen)

    fldata_2 = 'other_cell_lung_data.csv'
    data_2 = getdatanumgen(fldata_2, numgen)

    genes_and_err = SepGen(numgen, data_1, data_2)
    if not len(genes_and_err[0]) == 0:
        fl = open('SepGenesPair.log', 'w')
        fl.write('Num_gen_1,num_gen_2')
        for i in genes_and_err[0]:
            fl.write(str(i[0]) + ',' + str(i[1]) + '\n')
            print(str(i[0]) + ',' + str(i[1]) + '\n')
    else:
        print('There are not separated pair of genes :(\n')

    f = open('SepGenesPair_Err.log', 'w')
    f.write('Num_gen_1, num_gen_2, num_err')
    for i in range(len(genes_and_err[1])):
        f.write('{},{},{}\n'.format(genes_and_err[1][i][0], genes_and_err[1][i][1], genes_and_err[1][i][2]))
        print(genes_and_err[1][i])

main()
