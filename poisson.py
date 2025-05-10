import matplotlib.pyplot as plt 
import numpy as np 
from scipy.special import *
mean = 5
x = np.linspace(0, 1000, 1000)
y = np.exp(- mean) * np.power(mean, x) / factorial(x)
plt.plot(x, y)
plt.xlim(0, 20)
plt.show()
