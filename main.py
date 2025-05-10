import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Initial parameters
a_init, b_init, c_init, d_init, e_init = 1, 1, 1, 1, 0

# Create figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.3)

# Generate x values
x = np.linspace(-10, 10, 400)
y = a_init * np.sin(b_init * x) + c_init * np.cos(d_init * x) + e_init
line, = plt.plot(x, y, label="Dynamic Graph")

plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.title("Interactive Graph")
plt.legend()
plt.grid()

# Add sliders for parameters
ax_a = plt.axes([0.1, 0.2, 0.65, 0.03])
ax_b = plt.axes([0.1, 0.15, 0.65, 0.03])
ax_c = plt.axes([0.1, 0.1, 0.65, 0.03])
ax_d = plt.axes([0.1, 0.05, 0.65, 0.03])
ax_e = plt.axes([0.1, 0.0, 0.65, 0.03])

slider_a = Slider(ax_a, "a", -5, 5, valinit=a_init)
slider_b = Slider(ax_b, "b", 0.1, 5, valinit=b_init)
slider_c = Slider(ax_c, "c", -5, 5, valinit=c_init)
slider_d = Slider(ax_d, "d", 0.1, 5, valinit=d_init)
slider_e = Slider(ax_e, "e", -5, 5, valinit=e_init)

# Update function
def update(val):
    a, b, c, d, e = slider_a.val, slider_b.val, slider_c.val, slider_d.val, slider_e.val
    line.set_ydata(a * np.sin(b * x) + c * np.cos(d * x) + e)
    fig.canvas.draw_idle()

# Connect sliders to update function
slider_a.on_changed(update)
slider_b.on_changed(update)
slider_c.on_changed(update)
slider_d.on_changed(update)
slider_e.on_changed(update)

plt.show()

