mat1 = [
    [26, 73, 25, 31, 66, 103],
    [67, 71, 29, 83, 31, 88],
    [25, 117, 81, 69, 25, 94]

]

mat2 = [
    [67, 117, 88, 88, 117, 27],
    [31, 78, 100, 29, 90, 25],
    [117, 92, 27, 94, 94, 87]
]


for i in range(3):
    for j in range(6):
        mat1[i][j] ^= mat2[i][j]

print(mat1)
