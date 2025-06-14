
import base64
import string
from itertools import product

def is_valid_ascii(data):
    return all(32 <= byte < 127 for byte in data)

BASE_64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
ciphertext = "48WgB5GRRIXzFfQAYHK1MABxgMbBoGBllEHl0xAwceDQ=="

for prefix_tuple in product(BASE_64_CHARS, repeat=2):
    prefix = ''.join(prefix_tuple)
    full_input = prefix + ciphertext  # Combine prefix with ciphertext
    try:
        # Base64 decode the full string with prefix
        b64_decoded = base64.b64decode(full_input, validate=True)
        # Check printable ASCII
        if is_valid_ascii(b64_decoded):
            print(f"64 {prefix} -> {b64_decoded.decode('ascii')}")
    except Exception:
        continue

