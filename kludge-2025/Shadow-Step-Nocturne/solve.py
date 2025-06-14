with open("note.txt:secret", "rb") as f:
    data = f.read()
print(bytes(data))
decoded = bytes([b ^ 66 for b in data])
print(decoded.decode())
