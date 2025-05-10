import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

mean_1 = 1
mean_2 = 1.5
variance_1 = 2
variance_2 = 3
correlation = 0.1
x_range = 5
y_range = 5
stepsize = 1e-1  

fig = plt.figure()
fig.subplots_adjust(bottom=0.3)
ax = fig.add_subplot(111, projection="3d")

X = np.arange(-x_range, x_range, stepsize)
Y = np.arange(-y_range, y_range, stepsize)
X, Y = np.meshgrid(X, Y)

def Z(mean_1, mean_2, variance_1, variance_2, correlation, X, Y):
    A = (X - mean_1) / variance_1
    B = (Y - mean_2) / variance_2
    return (1 / (2 * np.pi * variance_1 * variance_2 * np.sqrt(1 - correlation ** 2))) * \
           np.exp(((-1) / (1 - correlation ** 2)) * (A ** 2 + B ** 2 - 2 * correlation * A * B))

Z_vals = Z(mean_1, mean_2, variance_1, variance_2, correlation, X, Y)

surf = ax.plot_surface(X, Y, Z_vals, cmap="viridis")

slider_positions = [
    (0.1, 0.25, r"$\mu_x$", 0, 10, mean_1),
    (0.1, 0.20, r"$\mu_y$", 0, 10, mean_2),
    (0.1, 0.15, r"$\sigma_x$", 0, 10, variance_1),
    (0.1, 0.10, r"$x_{min}$", 0, 10, x_range),
    (0.5, 0.25, r"$\sigma_y$", 0, 10, variance_2),
    (0.5, 0.20, r"$\rho$", -1, 1, correlation),  
    (0.5, 0.15, r"$y_{min}$", 0, 10, y_range),
]

sliders = {}
for x_pos, y_pos, label, min_val, max_val, init_val in slider_positions:
    ax_slider = plt.axes([x_pos, y_pos, 0.35, 0.03])
    sliders[label] = Slider(ax_slider, label, min_val, max_val, valinit=init_val)

def update(val):
    mean_1 = sliders[r"$\mu_x$"].val
    mean_2 = sliders[r"$\mu_y$"].val
    variance_1 = sliders[r"$\sigma_x$"].val
    variance_2 = sliders[r"$\sigma_y$"].val
    correlation = sliders[r"$\rho$"].val
    x_range = sliders[r"$x_{min}$"].val
    y_range = sliders[r"$y_{min}$"].val

    X = np.arange(-x_range, x_range, stepsize)
    Y = np.arange(-y_range, y_range, stepsize)
    X, Y = np.meshgrid(X, Y)

    updated_Z = Z(mean_1, mean_2, variance_1, variance_2, correlation, X, Y)

    ax.clear()
    ax.plot_surface(X, Y, updated_Z, cmap="viridis")

    fig.canvas.draw_idle()

for slider in sliders.values():
    slider.on_changed(update)

plt.show()

