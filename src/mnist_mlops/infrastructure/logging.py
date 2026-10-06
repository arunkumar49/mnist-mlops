"""Structured JSON logging on top of Python's built-in logging module."""

import json
import logging
import sys
from collections.abc import Mapping
from datetime import UTC, datetime

from mnist_mlops.infrastructure.config import LogFormat, LogLevel

# Attributes every LogRecord has. Anything else on a record came from `extra=`.
_STANDARD_RECORD_ATTRS = frozenset(vars(logging.LogRecord("", 0, "", 0, "", None, None))) | {
    "message",
    "asctime",
}

_CONSOLE_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"


class JsonFormatter(logging.Formatter):
    """Render a log record as a single-line JSON object."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(
                timespec="milliseconds"
            ),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        payload.update(
            (key, value)
            for key, value in vars(record).items()
            if key not in _STANDARD_RECORD_ATTRS and not key.startswith("_")
        )
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str, ensure_ascii=False)


class StaticFieldsFilter(logging.Filter):
    """Add fixed fields (service, environment) to every record, without overriding extras."""

    def __init__(self, fields: Mapping[str, str]) -> None:
        super().__init__()
        self._fields = dict(fields)

    def filter(self, record: logging.LogRecord) -> bool:
        for key, value in self._fields.items():
            if not hasattr(record, key):
                setattr(record, key, value)
        return True


def configure_logging(
    level: LogLevel = "INFO",
    fmt: LogFormat = "json",
    static_fields: Mapping[str, str] | None = None,
) -> None:
    """Configure the root logger. Safe to call more than once."""
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter() if fmt == "json" else logging.Formatter(_CONSOLE_FORMAT))
    if static_fields:
        handler.addFilter(StaticFieldsFilter(static_fields))

    root = logging.getLogger()
    for existing in list(root.handlers):
        root.removeHandler(existing)
    root.addHandler(handler)
    root.setLevel(level)
