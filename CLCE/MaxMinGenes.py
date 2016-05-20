def getdata(flname):
    fl = open(flname, 'r')
    list_min_max = []
    fl.readline()
    num_gen = 1
    for line in fl:
        attr = line.split(',')
        mn = 1
        mx = 1
        for num in range(1, len(attr)):
            val = float(attr[num])
            if float(attr[mn]) > val:
                mn = num
            if float(attr[mx]) < val:
                mx = num
        list_min_max.append([num_gen, float(attr[mn]), float(attr[mx])])
        num_gen += 1
    return list_min_max

def Comp_mn (v1, v2):
    if not v1[1] == v2[1]:
        return v1[1] < v2[1]
    if not v1[2] == v2[2]:
        return v1[2] < v2[2]
    return v[0] < v[0]

def Comp_mx (v1, v2):
    if not v1[2] == v2[2]:
        return v1[2] < v2[2]
    if not v1[1] == v2[1]:
        return v1[1] < v2[1]
    return v1[0] < v2[0]

def SepGen(ls1, ls2):
    ls_sep_gen = []
    for i in range(len(ls1)):
        if not ls1[i][0] == ls2[i][0]:
            print('Different Genes !!!')
            i = len(ls1)
            break
        if ls1[i][1] > ls2[i][2]:
            ls_sep_gen.append([ls1[i][0], 1, 2])
        if ls1[i][2] < ls2[i][1]:
            ls_sep_gen.append([ls1[i][0], 2, 1])
    
        

    return ls_sep_gen

def Logging(sep_gen, ls1, ls2, flname):
    fl = open(flname, 'w')
    for i in range(len(sep_gen)):
        if sep_gen[i][1] == 1:
            fl.write('Num: ' + str(ls1[i][0]) + ' Min_1: ' + str(ls1[i][1]) + ' Max_2: ' + str(ls2[i][2]) + '\n')
        if sep_gen[i][1] == 2:
            fl.write('Num: ' + str(ls1[i][0]) + ' Min_2: ' + str(ls2[i][1]) + ' Max_1: ' + str(ls1[i][2]) + '\n')
def main():
    small_cell = getdata('small_cell_lung_data.csv') 
    other_cell = getdata('other_cell_lung_data.csv')

    sep_gen = SepGen(small_cell, other_cell)
    if not len(sep_gen) == 0:
        Logging(sep_gen, small_cell, other_cell, 'SepGenes_Min_Max.log')
    else:
        print('There are not separated genes:(\n')

def get_all_data(flname):
    fl = open(flname, 'r')
    ls_gen = []
    fl.readline()
    numgen = 1
    for line in fl:
        vals = line.split(',')[1:]
        for i in range(len(vals)):
            vals[i] = float(vals[i])
        vals.sort()
        ls_gen.append([numgen, vals])
        numgen += 1
    return ls_gen

def num_err(ls1, ls2):
    errs = []
    for i in range(len(ls1)):
        err = 0
        if ls1[i][1][0] < ls2[i][1][0] and ls1[i][1][-1] > ls2[i][1][-1]:
            err = len(ls2[i][1])
            j = 0
            while ls1[i][1][j] < ls2[i][1][-1]:
                if ls1[i][1][j] >= ls2[i][1][0]:
                    err += 1
                j += 1
        if ls2[i][1][0] <= ls1[i][1][0] and ls2[i][1][-1] >= ls1[i][1][-1]:
            err = len(ls1[i][1])
            j = 0
            while ls2[i][1][j] < ls1[i][1][-1]:
                if ls2[i][1][j] >= ls1[i][1][0]:
                    err += 1
                j += 1
        if ls1[i][1][0] < ls2[i][1][0] and ls1[i][1][-1] <= ls2[i][1][-1]:
            while ls2[i][1][err] <= ls1[i][1][-1]:
                err += 1
                if err == len(ls2[i][1]):
                    print('Find sep gen !!!\n')
                    print('min1:{} max1:{} min2:{} max2:{}'.format(ls1[i][1][0], ls1[i][1][-1], ls2[i][1][0], ls2[i][1][-1]))
            j = -1
            while ls2[i][1][0] <= ls1[i][1][j]:
                j -= 1
                err += 1
        if ls2[i][1][0] <= ls1[i][1][0] and ls2[i][1][-1] < ls1[i][1][-1]:
            while ls1[i][1][err] <= ls2[i][1][-1]:
                err += 1
                if err == len(ls1[i][1]):
                    print('Find sep gen \n')
            j = -1
            while ls1[i][1][0] <= ls2[i][1][j]:
                j -= 1
                err += 1
        errs.append([ls1[i][0], err])
    return errs

def main2():
    small_cell = get_all_data('small_cell_lung_data.csv') 
    print(len(small_cell))
    other_cell = get_all_data('other_cell_lung_data.csv')
    print(len(other_cell))
    errs = num_err(small_cell, other_cell)
    f = open('SepGenes_Min_Max_Err.log', 'w')
    for i in range(len(errs)):
        f.write(str(errs[i][0]) + ',' + str(errs[i][1]) + '\n')
        print(errs[i])
main2()
