import random, math, pylab, numpy, xlrd, xlwt, os
from sklearn.svm import LinearSVC


# Замечания:
# cell - компаратор, который задает параметры: 'organ', 'type', 'subtype'
# cells - кортеж двух cell
# samples - наименования клеток(список)
# data - таблица(или кортеж таблиц) с экспрессиями для определенного типа клетки,
# нулевая строка таблицы - наименования клеток(samples),
# первый элемент каждой строки - наименование гена

def get_samples(cell):
    print ('get sample')

    rb = xlrd.open_workbook('CLCE_2.xls')
    sheet = rb.sheet_by_index(0)

    samples = []    
    for row_num in range(1, sheet.nrows):
        print(row_num)
        row = sheet.row_values(row_num)
        if cell(row[1], row[2], row[3]):
            print("True")
            samples.append(row[0])
        else:
            print('False')

    return samples

def get_data(cells):
    print('get data')

    samples_1 = get_samples(cells[0])
    samples_2 = get_samples(cells[1])

    data_1 = [samples_1]
    data_2 = [samples_2]

    rb = xlrd.open_workbook('CLCE_2.xls')
    sheet = rb.sheet_by_index(2)

    num_columns_1 = []
    num_columns_2 = []
    row_0 = sheet.row_values(0)

    for num_column in range(4, len(row_0)):
        if row_0[num_column] in samples_1:
            num_columns_1.append(num_column)
        if row_0[num_column] in samples_2:
            num_columns_2.append(num_column)

    for num_rows in range(1, sheet.nrows):
        row = sheet.row_values(num_rows)
        row_data_1 = [row[1]]
        row_data_2 = [row[1]]
        
        for idx in num_columns_1:
            row_data_1.append(row[idx])
        for idx in num_columns_2:
            row_data_2.append(row[idx])
        data_1.append(row_data_1)
        data_2.append(row_data_2)

    return (data_1, data_2)

def av_expr_genes(data):
    print('Average')

    av_expr_genes_1 = ['Average: ']
    av_expr_genes_2 = ['Average: ']
    
    for num_rows in range(1, len(data[0])):
        sum_expr_gene = 0
        for num_col in range(1, len(data[0][num_rows])):
            sum_expr_gene += math.log(data[0][num_rows][num_col], 2)
        av_expr_genes_1.append((data[0][num_rows][0], sum_expr_gene / (len(data[0][num_rows]) - 1)))

    for num_rows in range(1, len(data[1])):
        sum_expr_gene = 0
        for num_col in range(1, len(data[1][num_rows])):
            sum_expr_gene += math.log(data[1][num_rows][num_col], 2)
        av_expr_genes_2.append((data[1][num_rows][0], sum_expr_gene / (len(data[1][num_rows]) - 1)))

    return (av_expr_genes_1, av_expr_genes_2)

def st_dev_expr_genes(data, av_expr):
    print('Standard Deviation')

    st_dev_expr_genes_1 = ['Standard Deviation: ']
    st_dev_expr_genes_2 = ['Standard Deviation: ']

    for num_rows in range (1, len(data[0])):
        sum_squared = 0
        for num_col in range(1, len(data[0][num_rows])):
            sum_squared += (av_expr[0][num_rows] - data[0][num_rows][num_col]) ** 2
        st_dev_expr_genes_1.append((data[0][num_rows][0], math.sqrt(sum_squared / (len(data[0][num_rows])) - 1)))

    for num_rows in range (1, len(data[1])):
        sum_squared = 0
        for num_col in range(1, len(data[1][num_rows])):
            sum_squared += (av_expr[1][num_rows] - data[1][num_rows][num_col]) ** 2
        st_dev_expr_genes_1.append((data[1][num_rows][0], math.sqrt(sum_squared / (len(data[1][num_rows])) - 1)))
    
    return (st_dev_expr_genes_1, st_dev_expr_genes_2)

def logging(data, av, st_dev, book, sheet):
    print('logging')

    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheet)

    for num_row in range(len(data)):
        for num_col in range(len(data[num_row])):
            if num_row != 0:
                ws.write(num_row, num_col, data[num_row][num_col])
            else:
                ws.write(num_row, num_col + 1, data[num_row][num_col])

    for num_row in range(len(av)):
        ws.write(num_row, len(data) + 1, av[num_row][1])

    for num_row in range(len(st_dev)):
        ws.write(num_row, len(data) + 2, st_dev[num_row][1])

    wb.save(book)

def simple_analysis(cells):
    print('simple analysis')

    data = get_data(cells)
    av = av_expr_genes(data)
    st_dev = st_def_expr_genes(data, av)

    logging(data[0], av[0], st_dev[0], 'Expressions of the cells.xls', 'First type cell')
    logging(data[1], av[1], st_dev[1], 'Expressions of the cells.xls', 'Second type cell')

def small_cell_lung(organ, type_, subtype):
    return (organ == 'lung' and subtype == 'small_cell_carcinoma')

def other_cell_lung(organ, type_, subtype):
    return (organ == 'lung' and subtype != 'small_cell_carcinoma')

simple_analysis((small_cell_lung, other_cell_lung))
