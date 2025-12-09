import secrets
import string

def generate_random_string(length: int = 32) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))