"""Shared test setup. Every test starts from a clean environment."""

import logging
import os
from collections.abc import Iterator
from pathlib import Path

import pytest

from mnist_mlops.infrastructure.config import get_settings


@pytest.fixture(autouse=True)
def isolated_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Hide your real MNIST_* variables and .env file, and restore logging after each test."""
    for name in list(os.environ):
        if name.startswith("MNIST_"):
            monkeypatch.delenv(name)
    monkeypatch.chdir(tmp_path)  # an empty folder, so no .env is found
    get_settings.cache_clear()

    root = logging.getLogger()
    saved_handlers, saved_level = list(root.handlers), root.level
    yield
    root.handlers[:] = saved_handlers
    root.setLevel(saved_level)
    get_settings.cache_clear()
