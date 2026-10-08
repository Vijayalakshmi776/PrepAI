import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_PREFIX: str = '/api'
    JWT_SECRET_KEY: str = 'replace-with-strong-secret'
    JWT_ALGORITHM: str = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    DATABASE_URL: str = 'postgresql+psycopg://user:password@localhost/prepai'
    GEMINI_API_KEY: str | None = None
    BACKEND_CORS_ORIGINS: str = 'http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173,http://localhost:8010,http://127.0.0.1:8010,http://localhost:8000,http://127.0.0.1:8000'

    model_config = SettingsConfigDict(
        env_file=['.env', 'backend/.env', os.path.join(os.path.dirname(__file__), '../../.env')],
        env_file_encoding='utf-8',
        extra='ignore'
    )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(',') if origin.strip()]


settings = Settings()
