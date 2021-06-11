def pascal(row, i):
    if i == 1:
        return 1
    if i == row:
        return 1
    return pascal(row-1, i-1) + pascal(row-1, i)

print(pascal(8, 3))