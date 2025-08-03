import pytest

from src.api.auth.utils.password_hasher.bcrypt_password_hasher import BcryptPasswordHasher


@pytest.fixture
def password_hasher() -> BcryptPasswordHasher:
    return BcryptPasswordHasher()