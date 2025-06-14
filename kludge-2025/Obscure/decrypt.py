

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

ciphertext = b"W5M0MpCehiHzreSzNTczkc9d"
priv_key = 162267
key_bytes = priv_key.to_bytes(16, 'big')  # Pad/truncate to 16 bytes

cipher = AES.new(key_bytes, AES.MODE_ECB)
try:
    decrypted = unpad(cipher.decrypt(ciphertext), 16)
    print("Decrypted message:", decrypted.decode())
except Exception as e:
    print("AES decryption failed:", e)

