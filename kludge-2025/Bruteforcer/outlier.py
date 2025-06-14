
import hashlib
import base64
import os

class MultiLayerCrypto:
    def __init__(self, key=None):
        if key is None:
            self.key = os.urandom(32)
        else:
            self.key = hashlib.sha256(key.encode()).digest()
        
        self.xor_key = hashlib.md5(self.key).hexdigest().encode()
    
    def _xor_with_key(self, data, key):
        result = bytearray()
        for i, byte in enumerate(data):
            result.append(byte ^ key[i % len(key)])
        return bytes(result)
    
    def _reverse_bytes(self, data):
        return data[::-1]
    
    def _add_hash_signature(self, data):
        signature = hashlib.sha256(data + self.key).digest()[:8]
        return signature + data
    
    def encrypt(self, plaintext):
        if isinstance(plaintext, str):
            data = plaintext.encode('utf-8')
        else:
            data = plaintext
        
        data = self._xor_with_key(data, self.xor_key)
        data = self._reverse_bytes(data)
        data = self._xor_with_key(data, self.key)
        data = self._add_hash_signature(data)
        encrypted = base64.b64encode(data).decode('ascii')
        return encrypted

a = MultiLayerCrypto('r0cky0u')

with open('ciphertexts.txt', 'r') as file:
    ciphertexts = file.readlines()
    ciphertexts = [line.strip() for line in ciphertexts]


with open('plaintexts.txt', 'r') as file:
    for line in file:
        pt = line.strip()
        ct = a.encrypt(pt)
        if ct not in ciphertexts:
            print(pt)
