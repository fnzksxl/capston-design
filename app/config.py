from pydantic_settings import BaseSettings
from typing import ClassVar
from functools import lru_cache


class BaseConfig(BaseSettings):
    # DB
    DB_USERNAME: str
    DB_HOST: str
    DB_PASSWORD: str
    DB_PORT: int

    # CRED
    SECRET_KEY: str
    ALGORITHM: str

    # PAPAGO
    CLIENT_ID: str
    CLIENT_SECRET: str

    # Test Config
    TESTING: ClassVar[bool] = False

    class Config:
        extra = "ignore"
        env_file = ".env"
        env_file_encoding = "utf-8"


class testSettings(BaseConfig):
    TESTING: ClassVar[bool] = True
    DB_TEST_NAME: str


class Settings(BaseConfig):
    TESTING: ClassVar[bool] = False
    DB_NAME: str


class isMain(BaseSettings):
    IS_MAIN: bool

    class Config:
        extra = "ignore"
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    if is_main.IS_MAIN:
        return Settings()
    else:
        return testSettings()


is_main = isMain()
settings = get_settings()
