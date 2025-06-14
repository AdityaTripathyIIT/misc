def try_xor_line(data):
    for key in range(1, 256):
        line = ''.join(chr(x ^ key) for x in data)
        if all(32 <= ord(c) < 127 for c in line):
            print(f"[Key {key}] {line}")

# Break hidden rows into 3 lines
rows = [
    [67, 117, 88, 88, 117, 27],
    [31, 78, 100, 29, 90, 25],
    [117, 92, 27, 94, 94, 87]
]

for i, row in enumerate(rows):
    print(f"\nHidden Row {i+1}:")
    try_xor_line(row)

