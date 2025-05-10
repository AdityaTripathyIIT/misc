import matplotlib.pyplot as plt 
import numpy as np 

x = np.arange(-5, 5, 1e-5)
y = np.sqrt(38 + 24 * (np.cos(x) + np.sin(x)))

plt.plot(x, y)
plt.xlabel("$\phi$")
plt.ylabel(r"$\left\Vert\vec{F_1}(3, \phi)\right\Vert$")
plt.savefig("../figs/4a.png")

plt.show()
