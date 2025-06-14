import math

a = [182, 49, 208, 123, 182, 172, 163, 123]
for i in range(8):
    for j in range(i + 1, 8):
        print(math.fabs(a[i] - a[j]))
