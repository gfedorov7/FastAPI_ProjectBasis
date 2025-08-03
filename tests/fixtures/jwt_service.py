import os

import pytest
from dotenv import load_dotenv

from src.api.auth.utils.token.jwt_token_service import JWTTokenService


load_dotenv(".env.backend")

@pytest.fixture
def jwt_service() -> JWTTokenService:
    return JWTTokenService(
        secret=os.getenv("SECRET_KEY"),
        algorithm=os.getenv("TOKEN_ALGORITHM")
    )

@pytest.fixture
def expires() -> int:
    return int(os.getenv("TOKEN_EXPIRES"))