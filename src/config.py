from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.backend",
        extra="allow"
    )

class DataBaseSettings(CommonSettings):
    database_url: str
    database_echo: bool

class TokenSettings(CommonSettings):
    secret_key: str
    token_algorithm: str
    token_expires: int
    token_type: str

class CelerySettings(CommonSettings):
    celery_app_name: str
    celery_broker_url: str
    celery_backend_url: str

class Settings:
    database_settings: DataBaseSettings = DataBaseSettings()
    auth_settings: TokenSettings = TokenSettings()
    celery_settings: CelerySettings = CelerySettings()

settings = Settings()
