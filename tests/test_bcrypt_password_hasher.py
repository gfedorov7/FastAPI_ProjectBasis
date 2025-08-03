import random
import string

from src.api.auth.utils.password_hasher.password_hasher import PasswordHasher


def generate_random_string(length: int = 32) -> string:
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))

def test_password_hash_and_verify(password_hasher: PasswordHasher):
    password = generate_random_string()
    not_use_password = generate_random_string()

    hash_password = password_hasher.hash_password(password)

    assert hash_password != password
    assert password_hasher.verify_password(password, hash_password)
    assert not password_hasher.verify_password(not_use_password, hash_password)