from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # DB
    DB_USERNAME: str
    DB_HOST: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int

    # CRED
    SECRET_KEY: str
    ALGORITHM: str

    # PAPAGO
    CLIENT_ID: str
    CLIENT_SECRET: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
