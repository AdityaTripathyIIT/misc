
import numpy as np

# Characters to map
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
n = len(chars)

# Generate linearly spaced frequencies
frequencies = np.linspace(20, 25000, n)
char_freq_map = {round(freq, 1): char for char, freq in zip(chars, frequencies)}

# Frequencies to decode
input_freqs = [18200.0, 4900.0, 20800.0, 12300.0, 18200.0, 17200.0, 16300.0, 12300.0]

# Find closest character for each input frequency
def find_closest_char(freq):
    closest_freq = min(frequencies, key=lambda f: abs(f - freq))
    return char_freq_map[round(closest_freq, 1)]

# Decode
decoded_string = ''.join(find_closest_char(f) for f in input_freqs)
print("Decoded ASCII string:", decoded_string)

