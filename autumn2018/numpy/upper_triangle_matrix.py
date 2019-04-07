import xlrd
import numpy as np

filename = r"matrix_triangle.xlsx"

rb = xlrd.open_workbook(filename)
sheet = rb.sheet_by_index(0)
vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
print(vals)
matrix = np.array(vals)
result = np.allclose(matrix, np.triu(matrix))
print(result)


def func1(mat):
    result = True
    for i in range(1,len(mat)):
        for j in range(0,i):
            if mat[i][j]!=0:
                result = False
                break
    return result


print(func1(vals))