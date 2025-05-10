import numpy as np
import matplotlib.pyplot as plt

# Grid size
N = 20  # The grid will be N x N
x_values = np.linspace(-2, 2, N)
y_values = np.linspace(-2, 2, N)
X, Y = np.meshgrid(x_values, y_values)

# Charges positions and Coulomb constant
charges = [
    (1, 0, 1),   # positive charge at (1,0)
    (-1, 0, 1),  # positive charge at (-1,0)
    (0, 1, -1),  # negative charge at (0,1)
    (0, -1, -1)  # negative charge at (0,-1)
]

k = 8.99e9  # Coulomb constant

# Initialize field components
Ex, Ey = np.zeros(X.shape), np.zeros(Y.shape)

for x_q, y_q, q in charges:
    dx = X - x_q
    dy = Y - y_q
    r_squared = dx**2 + dy**2
    r_squared[r_squared == 0] = np.nan  # Avoid division by zero
    r_power = np.sqrt(r_squared) ** 3
    
    Ex += k * q * dx / r_power
    Ey += k * q * dy / r_power

# Calculate field strength and normalize for quiver plot
E_strength = np.sqrt(Ex**2 + Ey**2)
Ex /= E_strength
Ey /= E_strength

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
quiver = ax.quiver(X, Y, Ex, Ey, E_strength, cmap=plt.cm.plasma, norm=plt.Normalize(vmin=np.nanmin(E_strength), vmax=np.nanmax(E_strength)))

# Colorbar
cbar = plt.colorbar(quiver, ax=ax)
cbar.set_label("Field Strength")

# Limits and saving
plt.xlim(-2.1, 2.1)
plt.ylim(-2.1, 2.1)
plt.savefig("../figs/field_map.png")
plt.show()

