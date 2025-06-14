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
    
    def _verify_hash_signature(self, data):
        signature = data[:8]
        content = data[8:]
        expected_signature = hashlib.sha256(content + self.key).digest()[:8]
        
        if signature != expected_signature:
            raise ValueError("Invalid signature - data may be corrupted or wrong key")
        
        return content
    
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
    
    def get_key_info(self):
        """Return information about the current key."""
        key_hash = hashlib.sha256(self.key).hexdigest()[:16]
        return f"Key fingerprint: {key_hash}"


key = "r0cky0u"
a = MultiLayerCrypto(key)
with open("plaintexts.txt") as file:
    plaintexts = file.readlines()

with open("ciphertexts.txt") as file:
    ciphertexts = file.readlines()

for pt, ct in zip(plaintexts, ciphertexts):
    if(a.encrypt(pt) != ct):
        print(pt)
