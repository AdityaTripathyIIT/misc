import numpy as np 
import matplotlib.pyplot as plt 

r = np.random.rand(1, 1000)
theta = np.random.rand(1, 1000) * 2 * np.pi
for i in range(1000):
    plt.scatter(r[0,i] * np.cos(theta[0,i]), r[0,i] * np.sin(theta[0,i]))

plt.savefig("R-theta.png")
plt.show()
