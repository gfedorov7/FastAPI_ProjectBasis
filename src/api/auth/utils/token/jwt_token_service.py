from datetime import timedelta, datetime

import jwt

from src.api.auth.utils.token.token_service import TokenService
from src.api.auth.exceptions import (
    ExpiredTokenException, DecodeTokenException, InvalidTokenException
)


class JWTTokenService(TokenService):
    def __init__(self, secret: str, algorithm: str):
        self.secret = secret
        self.algorithm = algorithm

    def decode(self, token: str) -> dict:
        try:
            return self._decode(token)
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenException()
        except jwt.DecodeError:
            raise DecodeTokenException()
        except jwt.InvalidTokenError:
            raise InvalidTokenException()

    def _decode(self, token: str) -> dict:
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])

    def encode(self, data: dict, expire_hour: int) -> str:
        data_copy = data.copy()
        expired = self._get_expired_time(expire_hour)
        data_copy.update({"exp": expired})
        return jwt.encode(data_copy, self.secret, algorithm=self.algorithm)

    @staticmethod
    def _get_expired_time(expire_hour: int) -> int:
        expire_time = datetime.now() + timedelta(hours=expire_hour)
        return int(expire_time.timestamp())
