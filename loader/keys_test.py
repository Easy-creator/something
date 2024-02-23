import random
import string

def generate_password(length=15):
    # Combine lowercase letters, uppercase letters, and digits
    characters = string.ascii_letters + string.digits

    # Ensure that the specified length does not exceed the combined set's length
    length = min(length, len(characters))

    # Generate a random password using the adjusted length
    lookup_key = ''.join(random.choice(characters) for _ in range(length))

    return lookup_key