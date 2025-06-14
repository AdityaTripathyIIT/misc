import string
import random
def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

print(generate_random_password())
print(string.ascii_letters)
