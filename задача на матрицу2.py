def get_matrix_values(matrix,colum_index):
    colum_values=[]
    for row in matrix:
        if colum_index<len(row):
            colum_values.append(row[colum_index])
    return colum_values

def sum_values(values):
    return sum(values)

def average_value(values):
    if len(values)==0:
        return 0
    return sum(values)/len(values)


def colum(matrix,colum_index):
    colum_values=get_matrix_values(matrix,colum_index)

    print(f"Значения в колонке {colum_index}:{colum_values}")

    colum_sum=sum_values(colum_values)
    print(f"Сумма значений {colum_sum}")

    colum_average=average_value(colum_values)
    print(f"Среднее значение {colum_average}")

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
colum(matrix, 1)