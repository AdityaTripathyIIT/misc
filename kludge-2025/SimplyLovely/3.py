
import base64
import codecs
import string
import itertools

ciphertext = "TIOCXM5BDKR2SKJEVQ6SGMZIUCWKIJMYU2QKCPBTU2YSCN5DUE3DMIVEGYMDYIF3WGZKEKE6T2==="
flag_pattern = "ImNotMid{"

def fix_base64_padding(s):
    return s + "=" * ((4 - len(s) % 4) % 4)

# Use all printable ASCII characters for prefix (letters, digits, punctuation)
prefix_alphabet = string.printable.strip()  # removes whitespace chars

total_checked = 0
found_flag = False

for prefix in itertools.product(prefix_alphabet, repeat=3):
    prefix_str = "".join(prefix)
    candidate = prefix_str + ciphertext
    rot13_candidate = codecs.decode(candidate, 'rot_13')
    padded_candidate = fix_base64_padding(rot13_candidate)

    try:
        decoded = base64.b64decode(padded_candidate)
        decoded_text = decoded.decode('utf-8', errors='ignore')
        if flag_pattern in decoded_text:
            print(f"✅ FLAG found with prefix {repr(prefix_str)} and ROT13 + Base64 decode:")
            print(decoded_text)
            found_flag = True
            break
    except Exception:
        pass

    total_checked += 1
    if total_checked % 10000 == 0:
        print(f"[INFO] Checked {total_checked} prefixes so far...")

if not found_flag:
    print("❌ No flag found with full ASCII prefix brute force + ROT13 + Base64 decoding.")

