import matplotlib.pyplot as plt 
import numpy as np 
import math

x = list()
y = list()

x_0 = 0
y_0 = 0

h = 1e-3

def rhsfunc(a, b):
    return math.tan(a)

for i in range(int(1e4)):
    x.append(x_0)
    y.append(y_0)
    k1 = rhsfunc(x_0, y_0)
    k2 = rhsfunc(x_0 + 0.5 * h, y_0 + 0.5 * h * k1)
    k3 = rhsfunc(x_0 + 0.5 * h, y_0 + 0.5 * h * k2)
    k4 = rhsfunc(x_0 + h, y_0 + h * k3)

    y_0 += h*(k1+2*k2+2*k3+k4)/6
    x_0+=h 

plt.plot(x, y)
print(min(y))
print(np.sqrt(1.09))
plt.show()
