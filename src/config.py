from pydantic_settings import BaseSettings, SettingsConfigDict


class DataBaseSettings(BaseSettings):
    database_url: str
    database_echo: bool

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )

class TokenSettings(BaseSettings):
    secret_key: str
    token_algorithm: str
    token_expires: int
    token_type: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )

class CelerySettings(BaseSettings):
    celery_app_name: str
    celery_broker_url: str
    celery_backend_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )

class Settings:
    database_settings: DataBaseSettings = DataBaseSettings()
    auth_settings: TokenSettings = TokenSettings()
    celery_settings: CelerySettings = CelerySettings()

settings = Settings()
