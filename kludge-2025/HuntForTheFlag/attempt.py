with open("16times16.bin", "rb") as file:
    st = file.read()
    unique_chars= dict()
    for ch in st:
        if ch in unique_chars.keys():
            unique_chars[ch] += 1
        else :
            unique_chars[ch] = 1

    for key in sorted(unique_chars.keys()):
        print(f"{key} -> {unique_chars[key]}")





