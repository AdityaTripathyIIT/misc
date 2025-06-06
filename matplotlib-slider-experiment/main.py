import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Initial Parameters
A = 5
f1 = 5  
f2 = 20  
sampling_frequency = 100
duration = 5  

# Time Ranges
true_time_range = np.linspace(0, duration, 100000)  
sampled_time_range = np.arange(0, duration, 1 / sampling_frequency)  

# Function Definition
def target_function_0(x, A, f1, f2):
    return A * np.sin(2 * np.pi * f1 * x) * np.sin(2 * np.pi * f2 * x)

# Compute Initial Signals
true_signal = target_function_0(true_time_range, A, f1, f2)
sampled_signal = target_function_0(sampled_time_range, A, f1, f2)

# Compute Initial Fourier Transform
dft_result = np.fft.fft(sampled_signal)
frequencies = np.fft.fftfreq(len(sampled_signal), d=1/sampling_frequency)  

# Keep only positive frequencies
frequencies_half = frequencies[:len(frequencies)//2]
dft_magnitude_half = np.abs(dft_result[:len(dft_result)//2])

# Create Figure and Axes
fig, ax = plt.subplots(2, 1, figsize=(10, 6))
plt.subplots_adjust(bottom=0.3)  # Extra space for sliders

# Plot Time-Domain Signal
ax[0].plot(true_time_range, true_signal, label="Original Function", alpha=0.7)
sampled_plot, = ax[0].plot(sampled_time_range, sampled_signal, 'ro', label="Sampled Points", markersize=3)
ax[0].legend()
ax[0].set_title("Time-Domain Signal")

# Plot Frequency Spectrum (DFT) using Stem Plot
stem_plot, = ax[1].plot(frequencies_half, dft_magnitude_half, 'bo', markersize=3)  # Blue dots
stem_lines = ax[1].vlines(frequencies_half, 0, dft_magnitude_half, colors='blue')  # Vertical lines
ax[1].set_title("Frequency Spectrum (DFT)")
ax[1].set_xlabel("Frequency (Hz)")

# Slider Axes
ax_a = plt.axes([0.1, 0.2, 0.65, 0.03])
ax_b = plt.axes([0.1, 0.15, 0.65, 0.03])
ax_c = plt.axes([0.1, 0.1, 0.65, 0.03])

# Define Sliders
slider_a = Slider(ax_a, "A", 0, 5, valinit=A)
slider_b = Slider(ax_b, "f1", 0, 100, valinit=f1)
slider_c = Slider(ax_c, "f2", 0, 100, valinit=f2)

# Update Function
def update(val):
    A, f1, f2 = slider_a.val, slider_b.val, slider_c.val
    
    # Update sampled signal
    updated_sampled_signal = target_function_0(sampled_time_range, A, f1, f2)
    sampled_plot.set_ydata(updated_sampled_signal)  

    # Compute new DFT
    updated_dft = np.fft.fft(updated_sampled_signal)
    updated_magnitude = np.abs(updated_dft[:len(updated_dft)//2])  # Keep only positive frequencies

    # Update plot data
    stem_plot.set_data(frequencies_half, updated_magnitude)  # Update points

    # FIX: Remove old lines and update with new ones
    global stem_lines
    segments = [[[x, 0], [x, y]] for x, y in zip(frequencies_half, updated_magnitude)]
    stem_lines.set_segments(segments)  # Efficiently update the vlines
    
    fig.canvas.draw_idle()  # Redraw the figure

# Link Sliders to Update Function
slider_a.on_changed(update)
slider_b.on_changed(update)
slider_c.on_changed(update)

plt.show()
