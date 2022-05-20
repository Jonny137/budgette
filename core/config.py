import os
from dotenv import load_dotenv
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings

from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    API_STR: str = '/api'
    PROJECT_NAME: str = os.getenv('PROJECT_NAME')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    HOST: Union[str, None] = os.getenv('HOST') or '0.0.0.0'
    PORT: Union[int, None] = os.getenv('PORT') or 8000
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        os.getenv('LOCAL_ORIGIN')
    ]

    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER: str = os.getenv('POSTGRES_SERVER', 'localhost')
    POSTGRES_PORT: str = os.getenv('POSTGRES_PORT', 5432)
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', PROJECT_NAME)
    UNIT_TEST_DB: str = os.getenv('TEST_DB', 'tes')
    SQLALCHEMY_DATABASE_URL = f'postgresql://' \
                              f'{POSTGRES_USER}:{POSTGRES_PASSWORD}' \
                              f'@{POSTGRES_SERVER}:{POSTGRES_PORT}' \
                              f'/{POSTGRES_DB}'
    TEST_DATABASE_URL = f'postgresql://' \
                        f'{POSTGRES_USER}:{POSTGRES_PASSWORD}' \
                        f'@{POSTGRES_SERVER}:{POSTGRES_PORT}/budgette_test'

    class Config:
        case_sensitive = True


settings = Settings()
