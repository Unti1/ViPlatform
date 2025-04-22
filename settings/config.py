
import pathlib
from authx import AuthX, AuthXConfig
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    ROOT_PATH: pathlib.Path = pathlib.Path(__file__).parent.parent 

    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_PORT: int
    REDIS_DB: int

    
    DATABASE_SQLITE: str = 'sqlite+aiosqlite:///data/main.db'
    
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=ROOT_PATH / '.env',
        env_file_encoding='utf-8'
    )

    def get_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        # return self.DATABASE_SQLITE
        
    def get_redis_url(self):
        return f"rediss://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

settings = Settings()

auth_config = AuthXConfig()
auth_config.JWT_SECRET_KEY = settings.SECRET_KEY
auth_config.JWT_ACCESS_COOKIE_NAME = "access_token"
auth_config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=auth_config)

