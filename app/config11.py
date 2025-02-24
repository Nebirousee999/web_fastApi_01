from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
import os

# Получение секретных ключей, паролей из файла .env

# Класс настроек для базы данных
class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    LOG_LEVEL: str

    # Получение ссылки для бызы данных postgresql+asyncpg
    def get_database_url(self):
        TEST_DATABASE_URL = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return TEST_DATABASE_URL

    # переменные для тестовой базы данных
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    # Получение ссылки для тестовой бызы данных postgresql+asyncpg
    def get_test_database_url(self):
        DATABASE_URL = f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:" \
                       f"{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        return DATABASE_URL

    # атрибуты для секретного ключа
    SECRET_KEY: str
    ALGORITM: str

    # Откуда берутся атрибуты
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    )

settings = Settings()

print(settings.get_database_url())