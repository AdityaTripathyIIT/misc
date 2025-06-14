from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

X = 0x80fb32f0534c4c88f3ca0bda024ea41ff6d37f305551763c6805a338dc759dc6
Y = 0xeb8ce629a0dbac49c8b2de782d19dba58aea46931c827643310bc9306f160150
target_pubkey = ec.EllipticCurvePublicNumbers(X, Y, ec.SECP256R1()).public_key(default_backend())

for privKey in range(1, int(1e10)):  # Adjust range as needed
    test_privkey = ec.derive_private_key(privKey, ec.SECP256R1(), default_backend())
    test_pubkey = test_privkey.public_key().public_numbers()
    if (test_pubkey.x == X) and (test_pubkey.y == Y):
        print(f"Found private key: {privKey}")
        break
