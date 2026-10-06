from pathlib import Path

import pytest
from pydantic import ValidationError

from mnist_mlops.infrastructure.config import Environment, Settings, get_settings


def test_defaults() -> None:
    settings = Settings()
    assert settings.environment is Environment.LOCAL
    assert settings.aws_region == "ap-south-1"
    assert settings.log_level == "INFO"
    assert settings.git_sha is None


def test_reads_prefixed_environment_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MNIST_ENVIRONMENT", "prod")
    monkeypatch.setenv("MNIST_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("MNIST_GIT_SHA", "0123abc")
    settings = Settings()
    assert settings.environment is Environment.PROD
    assert settings.log_level == "DEBUG"
    assert settings.git_sha == "0123abc"


def test_reads_dotenv_file() -> None:
    Path(".env").write_text("MNIST_ENVIRONMENT=dev\n", encoding="utf-8")
    assert Settings().environment is Environment.DEV


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("MNIST_ENVIRONMENT", "staging"),
        ("MNIST_LOG_LEVEL", "LOUD"),
        ("MNIST_AWS_REGION", "mumbai"),
        ("MNIST_GIT_SHA", "not-a-sha"),
    ],
)
def test_rejects_invalid_values(monkeypatch: pytest.MonkeyPatch, name: str, value: str) -> None:
    monkeypatch.setenv(name, value)
    with pytest.raises(ValidationError):
        Settings()


def test_settings_are_immutable() -> None:
    settings = Settings()
    with pytest.raises(ValidationError):
        settings.environment = Environment.PROD  # type: ignore[misc]


def test_get_settings_is_cached() -> None:
    assert get_settings() is get_settings()
