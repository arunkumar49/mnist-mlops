import json

import pytest

from mnist_mlops import __version__
from mnist_mlops.entrypoints.cli import EXIT_CONFIG_ERROR, EXIT_OK, main


def test_info_prints_build_info_as_json(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("MNIST_ENVIRONMENT", "dev")

    exit_code = main(["info"])

    out = capsys.readouterr().out
    assert exit_code == EXIT_OK
    assert json.loads(out) == {
        "service_name": "mnist-mlops",
        "version": __version__,
        "environment": "dev",
        "aws_region": "ap-south-1",
        "git_sha": None,
    }


def test_logs_go_to_stderr_not_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    main(["info"])
    captured = capsys.readouterr()
    json.loads(captured.out)  # stdout is pure JSON, no log lines mixed in
    log_lines = [json.loads(line) for line in captured.err.strip().splitlines()]
    assert [line["message"] for line in log_lines] == ["command started", "command finished"]
    assert all(line["environment"] == "local" for line in log_lines)


def test_invalid_configuration_exits_with_code_2(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("MNIST_ENVIRONMENT", "staging")

    assert main(["info"]) == EXIT_CONFIG_ERROR
    assert "Invalid configuration" in capsys.readouterr().err


def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_command_is_required() -> None:
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 2
