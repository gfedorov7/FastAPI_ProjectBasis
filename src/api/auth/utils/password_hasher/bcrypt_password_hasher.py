import bcrypt

from src.api.auth.utils.password_hasher.password_hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):

    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: bytes):
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password
        )
