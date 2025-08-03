import os

import pytest

from src.api.auth.utils.token.jwt_token_service import JWTTokenService
from src.api.auth.exceptions import ExpiredTokenException, DecodeTokenException


@pytest.fixture
def jwt_service_bad_secret() -> JWTTokenService:
    algorithm = os.getenv("TOKEN_ALGORITHM")
    return JWTTokenService("DSASDFFSDDFS", algorithm)

@pytest.fixture
def data() -> dict:
    return {"sub": "123"}

def test_encode_and_decode_jwt_service(jwt_service, data, expires):
    token = jwt_service.encode(data, expires)
    payload = jwt_service.decode(token)

    assert payload.pop("exp", None) is not None
    assert payload == data

def test_encode_and_decode_jwt_service_with_exc_expired_token(jwt_service, data):
    expired_expires = -5000
    token = jwt_service.encode(data, expired_expires)

    with pytest.raises(ExpiredTokenException):
        jwt_service.decode(token)

def test_encode_and_decode_jwt_service_with_exc_decode_token(jwt_service, jwt_service_bad_secret, data, expires):
    token = jwt_service.encode(data, expires)

    with pytest.raises(DecodeTokenException):
        jwt_service_bad_secret.decode(token)