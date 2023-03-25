import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "rencontrerlarche_benevolents"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "Benevolents missions management for L'Arche associations"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgres://postgresuser:password@127.0.0.1:5432/dbname")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "keep_your_secrets_secret")


settings = Settings()
