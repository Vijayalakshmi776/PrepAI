from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_PREFIX: str = '/api'
    JWT_SECRET: str = 'replace-with-strong-secret'
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    DATABASE_URL: str = 'postgresql+psycopg://user:password@localhost/prepai'
    GEMINI_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()
