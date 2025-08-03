from pydantic_settings import BaseSettings


class DataBaseSettings(BaseSettings):
    database_url: str
    database_echo: bool

    class Config:
        env_file = ".env.backend"
        extra = "allow"

class AuthSettings(BaseSettings):
    secret_key: str
    token_algorithm: str
    token_expires: int
    token_type: str

    class Config:
        env_file = ".env.backend"
        extra = "allow"

class Settings:
    database_settings: DataBaseSettings = DataBaseSettings()
    auth_settings: AuthSettings = AuthSettings()

settings = Settings()
