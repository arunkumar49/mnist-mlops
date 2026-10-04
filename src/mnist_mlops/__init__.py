"""MNIST digit classifier built with enterprise MLOps practices."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mnist-mlops")
except PackageNotFoundError:  # pragma: no cover - only when the package isn't installed
    __version__ = "0.0.0+unknown"

__all__ = ["__version__"]
