"""Typed runtime settings, read from MNIST_* environment variables."""

from enum import StrEnum
from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]
LogFormat = Literal["json", "console"]


class Environment(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"


class Settings(BaseSettings):
    """All runtime settings. Invalid values fail at startup, not halfway through a job."""

    model_config = SettingsConfigDict(
        env_prefix="MNIST_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )

    service_name: str = "mnist-mlops"
    environment: Environment = Environment.LOCAL
    log_level: LogLevel = "INFO"
    log_format: LogFormat = "json"
    aws_region: str = Field(default="ap-south-1", pattern=r"^[a-z]{2}(-[a-z]+)+-\d$")
    git_sha: str | None = Field(default=None, pattern=r"^[0-9a-f]{7,40}$")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load settings once per program run."""
    return Settings()
