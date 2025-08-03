from abc import ABC, abstractmethod


class PasswordHasher(ABC):

    @staticmethod
    @abstractmethod
    def hash_password(password: str) -> bytes: ...

    @staticmethod
    @abstractmethod
    def verify_password(plain_password: str, hashed_password: bytes): ...
