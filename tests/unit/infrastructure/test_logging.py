import json
import logging

import pytest

from mnist_mlops.infrastructure.logging import configure_logging


def last_json_line(stderr: str) -> dict[str, object]:
    line = stderr.strip().splitlines()[-1]
    parsed: dict[str, object] = json.loads(line)
    return parsed


def test_emits_one_json_object_per_line(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(level="INFO", fmt="json")
    logging.getLogger("demo").info("hello %s", "world", extra={"epoch": 3})

    record = last_json_line(capsys.readouterr().err)

    assert record["message"] == "hello world"
    assert record["level"] == "INFO"
    assert record["logger"] == "demo"
    assert record["epoch"] == 3
    assert str(record["timestamp"]).endswith("+00:00")


def test_adds_static_fields_without_overriding_extras(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(static_fields={"service": "svc", "environment": "dev"})
    logging.getLogger("demo").info("x", extra={"environment": "explicit"})

    record = last_json_line(capsys.readouterr().err)

    assert record["service"] == "svc"
    assert record["environment"] == "explicit"


def test_includes_exception_traceback(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging()
    try:
        raise ValueError("boom")
    except ValueError:
        logging.getLogger("demo").exception("failed")

    record = last_json_line(capsys.readouterr().err)

    assert "ValueError: boom" in str(record["exception"])


def test_respects_level(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(level="WARNING")
    logging.getLogger("demo").info("hidden")
    assert capsys.readouterr().err == ""


def test_console_format_is_human_readable(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(fmt="console")
    logging.getLogger("demo").warning("careful")
    err = capsys.readouterr().err
    assert "WARNING" in err
    assert "demo: careful" in err


def test_reconfiguring_does_not_duplicate_output(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging()
    configure_logging()
    logging.getLogger("demo").info("once")
    assert len(capsys.readouterr().err.strip().splitlines()) == 1
