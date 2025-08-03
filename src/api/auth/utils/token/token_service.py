from abc import ABC, abstractmethod


class TokenService(ABC):


    @abstractmethod
    def decode(self, token: str) -> dict: ...

    @abstractmethod
    def encode(self, data: dict, expire_hour: int) -> str: ...
