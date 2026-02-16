from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    APP_NAME: str
    APP_VERSION: str
    FILE_ALLOWED_TYPES: list[str]
    MAX_FILE_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / ".env")

def get_settings():
    return Settings()