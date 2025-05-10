import matplotlib.pyplot as plt 
import numpy as np 

x = np.arange(-5, 5, 1e-5)
y = np.sqrt(((40)/(x**2+1) + 3*np.sqrt(2))**2 + 4)

plt.plot(x, y)
plt.xlabel("$s$")
plt.ylabel(r"$\left\Vert\vec{F_1}(s, \frac{\pi}{4})\right\Vert$")
plt.savefig("../figs/4b.png")

plt.show()
