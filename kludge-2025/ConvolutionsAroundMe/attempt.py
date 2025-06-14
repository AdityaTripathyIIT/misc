import numpy as np

# Matrix rows from C code
rows = [
    [26, 73, 25, 31, 66, 103],
    [67, 117, 88, 88, 117, 27],
    [67, 71, 29, 83, 31, 88],
    [31, 78, 100, 29, 90, 25],
    [25, 117, 81, 69, 25, 94],
    [117, 92, 27, 94, 94, 87]
]

# Start with the first row
result = rows[0]

# Repeated convolution with each subsequent row
for i in range(1, len(rows)):
    result = np.convolve(result, rows[i], mode='full')

# Convert to ASCII characters (mod 128)
ascii_chars = [chr(x % 128) for x in result]

# Join characters, keeping only printable ones
printable = ''.join(c if 32 <= ord(c) <= 126 else '.' for c in ascii_chars)

# Print the result
print("Decoded ASCII string:")
print(printable)

