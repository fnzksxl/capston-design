import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

class Settings():
  DB_USERNAME = os.environ.get("DB_USERNAME")
  DB_HOST = os.environ.get("DB_HOST")
  DB_PASSWORD = os.environ.get("DB_PASSWORD")
  DB_NAME = os.environ.get("DB_NAME")
  DB_PORT = int(os.environ.get("DB_PORT"))

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()