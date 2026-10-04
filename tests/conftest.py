"""Shared test setup. Every test starts from a clean environment."""

import os
from collections.abc import Iterator
from pathlib import Path

import pytest

from mnist_mlops.infrastructure.config import get_settings


@pytest.fixture(autouse=True)
def isolated_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Hide your real MNIST_* variables and .env file from tests."""
    for name in list(os.environ):
        if name.startswith("MNIST_"):
            monkeypatch.delenv(name)
    monkeypatch.chdir(tmp_path)  # an empty folder, so no .env is found
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
