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
        num_gen +=1
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

small_cell = getdata('small_cell_lung_data.csv') 
other_cell = getdata('other_cell_lung_data.csv')

sep_gen = SepGen(small_cell, other_cell)
if not len(sep_gen) == 0:
    Logging(sep_gen, small_cell, other_cell, 'SepGenes_Min_Max.log')
else:
    print('There are not separated genes:(\n')
