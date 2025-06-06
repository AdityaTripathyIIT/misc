import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
epsilon_0 = 8.85e-12  # Permittivity of free space
k = 1 / (4 * np.pi * epsilon_0)  # Coulomb's constant (simplified form)

# Charge positions and values
charges = [
    (0, 1, 1),    # +1C at (0, +1)
    (0, -1, 1),   # +1C at (0, -1)
    (1, 0, -1),   # -1C at (+1, 0)
    (-1, 0, -1)   # -1C at (-1, 0)
]

# Define grid for the x-y plane
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)

# Compute potential at each point on the grid
V = np.zeros_like(X)
for charge in charges:
    x_c, y_c, q = charge
    R = np.sqrt((X - x_c)**2 + (Y - y_c)**2)
    R[R == 0] = 1e-9  
    V += k * q / R

# Create 3D plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, V, cmap='viridis', edgecolor='none')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Potential (V)')
ax.set_title('Electric Potential due to Point Charges')
plt.savefig("../figs/potential.png")
plt.show()
