import os
import pathlib
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    ROOT_PATH: pathlib.Path = pathlib.Path(__file__).parent.parent 

    DATABASE_SQLITE: str = 'sqlite+aiosqlite:///data/main.db'
    
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=ROOT_PATH / '.env',
        env_file_encoding='utf-8'
    )

    def get_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        # return self.DATABASE_SQLITE

settings = Settings()


