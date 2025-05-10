import numpy as np 
import matplotlib.pyplot as plt 

x = np.random.rand(1, 1000) * 2 - 1

for i in range(1000):
    plt.scatter(x[0,i], np.random.rand(1, 1) * 2 * np.sqrt(1 - x[0,i] ** 2) - np.sqrt(1 - x[0, i] ** 2))

plt.savefig("point.png")
plt.show()
