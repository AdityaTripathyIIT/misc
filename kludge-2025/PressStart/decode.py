data = [
    0x19, 0x3F, 0x7E, 0x28, 0x40, 0x00, 0x2C, 0x36, 0x2B, 0x25, 0x04, 0x33, 0x40, 0x12, 0x12, 0x66,
    0x2A, 0x07, 0x42, 0x18, 0x7C, 0x7C, 0x22, 0x1A, 0x23, 0x31, 0x7F, 0x35, 0x07, 0x12, 0x7D, 0x61,
    0x62, 0x6B, 0x04, 0x3A
]

targets = [b"imNotMid", b"ImNotMid"]

for keylen in range(1, 9):
    for target in targets:
        key = [d ^ t for d, t in zip(data[:keylen], target[:keylen])]
        # Repeat key to length of data
        fullkey = (key * ((len(data) + keylen - 1) // keylen))[:len(data)]
        decoded = bytes([d ^ k for d, k in zip(data, fullkey)])
        if decoded.startswith(target):
            print(f"Possible key (len={keylen}): {[hex(k) for k in key]}")
            print("Decoded:", decoded.decode('ascii'))

