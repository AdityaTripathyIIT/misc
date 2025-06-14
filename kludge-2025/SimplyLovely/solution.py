
import base64
import string
from itertools import product

# Base32 character set
BASE32_CHARS = string.ascii_uppercase + '234567'

# Base32 character set for Caesar shift
BASE32_SHIFT_CHARS = BASE32_CHARS

# Ciphertext with missing 3 characters
ciphertext = "TIOCXM5BDKR2SKJEVQ6SGMZIUCWKIJMYU2QKCPBTU2YSCN5DUE3DMIVEGYMDYIF3WGZKEKE6T2==="

# Caesar shift function using the Base32 character set
def caesar_shift(text, shift):
    result = []
    for char in text:
        if char in BASE32_SHIFT_CHARS:
            idx = BASE32_SHIFT_CHARS.index(char)
            shifted_idx = (idx + shift) % len(BASE32_SHIFT_CHARS)
            result.append(BASE32_SHIFT_CHARS[shifted_idx])
        else:
            # Keep padding or invalid characters unchanged
            result.append(char)
    return ''.join(result)

# Check if all characters in bytes are printable ASCII
def is_valid_ascii(data):
    return all(32 <= byte < 127 for byte in data)

# Caesar shift amount
SHIFT_AMOUNT = 0

# Brute-force logic
for prefix_tuple in product(BASE32_CHARS, repeat=3):
    prefix = ''.join(prefix_tuple)
    full_input = prefix + ciphertext
    shifted_input = caesar_shift(full_input, SHIFT_AMOUNT)
    try:
        # Base32 decode
        b32_decoded = base64.b32decode(shifted_input, casefold=True)
        if is_valid_ascii(b32_decoded):
            print(f"32 {prefix} -> {b32_decoded.decode('ascii')}")

        # Base64 decode
        b64_decoded = base64.b64decode(b32_decoded[::-1], validate=True)
        
        # Check printable ASCII
        if is_valid_ascii(b64_decoded):
            print(f"64 {prefix} -> {b64_decoded.decode('ascii')}")
    except Exception:
        continue

