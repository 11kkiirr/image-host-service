from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any, ClassVar

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):

    APP_HOST: str = "localhost"
    APP_PORT: int = 8000
    BASE_URL: str

    DATABASE_SYSTEM: SecretStr
    DATABASE_DRIVER: SecretStr
    DATABASE_NAME: SecretStr
    DATABASE_USER: SecretStr
    DATABASE_PASSWORD: SecretStr
    DATABASE_HOST: SecretStr
    DATABASE_PORT: SecretStr
    
    SECRET_KEY: SecretStr

    BACKEND_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent.parent
    PROJECT_DIR: ClassVar[Path] = BACKEND_DIR.parent
    ENV_FILE: ClassVar[Path] = (
        BACKEND_DIR / ".env"
        if (BACKEND_DIR / ".env").exists()
        else PROJECT_DIR / ".env"
    )

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def __init__(self, **values: Any):
        super().__init__(**values)


config = Config()
